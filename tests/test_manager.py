import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("manager", ROOT / "scripts/manage.py")
manager = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manager)


class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.home = self.base / "home with spaces"
        self.home.mkdir()
        self.package = self.base / "package"
        (self.package / "skills/figma-bro").mkdir(parents=True)
        (self.package / "agents").mkdir()
        (self.package / "skills/figma-bro/SKILL.md").write_text("---\nname: figma-bro\ndescription: Test fixture\n---\nVersion one\n")
        (self.package / "agents/figma-bro.toml").write_text('name = "figma_bro"\n')
        (self.package / "VERSION").write_text("1\n")
        self.m = manager.Manager(self.home, self.package)

    def prior_install(self):
        skill, agent = self.m.targets["skill"], self.m.targets["agent"]
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("Previous personal instructions\n")
        (skill / "notes.txt").write_text("Preserve this user file\n")
        agent.parent.mkdir(parents=True)
        agent.write_text("Previous agent\n")
        return self.m.hashes()

    def test_clean_install_survives_source_move_and_is_idempotent(self):
        self.m.install()
        expected = self.m.hashes()
        self.assertEqual(self.m.install()["result"], "already-current")
        shutil.move(str(self.package), str(self.base / "moved-package"))
        self.assertEqual(self.m.hashes(), expected)
        self.assertFalse(self.m.status()["modified"])
        self.m.uninstall()
        self.assertEqual(self.m.hashes(), {"skill": None, "agent": None})
        self.assertEqual(self.m.uninstall()["result"], "not-installed")

    def test_unmanaged_install_is_refused_without_changes(self):
        original = self.prior_install()
        with self.assertRaisesRegex(ValueError, "unmanaged"):
            self.m.install()
        self.assertEqual(self.m.hashes(), original)
        self.assertFalse(self.m.state_path.exists())

    def test_replace_update_uninstall_restores_initial_baseline(self):
        original = self.prior_install()
        self.m.install(replace=True)
        baseline = self.m.state()["baseline"]
        (self.package / "VERSION").write_text("2\n")
        (self.package / "skills/figma-bro/SKILL.md").write_text("Version two\n")
        self.m.install(update=True)
        self.assertEqual(self.m.state()["baseline"], baseline)
        self.assertEqual(self.m.state()["version"], "2")
        self.m.uninstall()
        self.assertEqual(self.m.hashes(), original)
        self.assertFalse(self.m.state_path.exists())
        self.assertGreaterEqual(len(list((self.m.root / "backups").iterdir())), 3)

    def test_local_edits_added_files_and_missing_files_are_protected(self):
        self.m.install()
        note = self.m.targets["skill"] / "personal-notes.md"
        note.write_text("My changes\n")
        changed = self.m.hashes()
        for action in [lambda: self.m.install(update=True), self.m.uninstall]:
            with self.assertRaisesRegex(ValueError, "edited or removed"):
                action()
            self.assertEqual(self.m.hashes(), changed)
        note.unlink()
        self.m.targets["agent"].unlink()
        with self.assertRaisesRegex(ValueError, "edited or removed"):
            self.m.install(update=True)

    def test_interrupted_second_target_replace_rolls_back_both_and_state(self):
        self.prior_install()
        self.m.install(replace=True)
        original, state = self.m.hashes(), self.m.state_path.read_bytes()
        (self.package / "VERSION").write_text("2\n")
        real_replace = manager.os.replace
        failed = []

        def replace(source, target):
            if Path(source).name == "new" and Path(target) == self.m.targets["agent"] and not failed:
                failed.append(True)
                raise OSError("Simulated disk failure")
            return real_replace(source, target)

        with mock.patch.object(manager.os, "replace", side_effect=replace):
            with self.assertRaisesRegex(OSError, "Simulated"):
                self.m.install(update=True)
        self.assertEqual(self.m.hashes(), original)
        self.assertEqual(self.m.state_path.read_bytes(), state)
        self.assertFalse(list(self.home.rglob(".figma-bro-stage-*")))

    def test_state_write_failure_rolls_back_fresh_install(self):
        real_replace = manager.os.replace

        def replace(source, target):
            if Path(target) == self.m.state_path:
                raise OSError("State write denied")
            return real_replace(source, target)

        with mock.patch.object(manager.os, "replace", side_effect=replace):
            with self.assertRaises(OSError):
                self.m.install()
        self.assertEqual(self.m.hashes(), {"skill": None, "agent": None})
        self.assertFalse(self.m.state_path.exists())

    def test_symlink_targets_and_payloads_are_not_followed(self):
        outside = self.base / "outside"
        outside.mkdir()
        (outside / "sentinel").write_text("Do not change\n")
        self.m.targets["skill"].parent.mkdir(parents=True)
        self.m.targets["skill"].symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            manager.Manager(self.home, self.package)
        self.m.targets["skill"].unlink()
        (self.package / "skills/figma-bro/link").symlink_to(outside)
        with self.assertRaisesRegex(ValueError, "symlink"):
            self.m.install()
        self.assertEqual((outside / "sentinel").read_text(), "Do not change\n")

    def test_backup_tampering_and_unsafe_state_are_refused(self):
        self.prior_install()
        self.m.install(replace=True)
        state = self.m.state()
        (self.m.root / state["baseline"] / "agent").write_text("Altered backup\n")
        current = self.m.hashes()
        with self.assertRaisesRegex(ValueError, "backup was changed"):
            self.m.uninstall()
        self.assertEqual(self.m.hashes(), current)
        state["baseline"] = "../outside"
        self.m.state_path.write_text(json.dumps(state))
        with self.assertRaisesRegex(ValueError, "Unsafe baseline"):
            self.m.uninstall()

    def test_existing_lock_prevents_mutation(self):
        self.m.root.mkdir(parents=True)
        lock = self.m.root / "manager.lock"
        lock.write_text("Another process\n")
        with self.assertRaisesRegex(ValueError, "lock exists"):
            self.m.install()
        self.assertEqual(self.m.hashes(), {"skill": None, "agent": None})
        self.assertTrue(lock.exists())

    def test_update_requires_managed_state_and_uninstall_keeps_unknown_files(self):
        with self.assertRaisesRegex(ValueError, "No managed"):
            self.m.install(update=True)
        original = self.prior_install()
        with self.assertRaisesRegex(ValueError, "Unmanaged"):
            self.m.uninstall()
        self.assertEqual(self.m.hashes(), original)

    def test_duplicate_detection_from_nested_repo_and_legacy_user_scope(self):
        project = self.base / "project"
        project.mkdir()
        subprocess.run(["git", "init", "-q", str(project)], check=True)
        nested = project / "src/feature"
        nested.mkdir(parents=True)
        skill = project / ".agents/skills/renamed-folder/SKILL.md"
        skill.parent.mkdir(parents=True)
        skill.write_text('---\nname: "figma-bro"\n---\n')
        role = project / ".codex/agents/other-name.toml"
        role.parent.mkdir(parents=True)
        role.write_text('name = "figma_bro"\n')
        legacy = self.home / ".codex/skills/old/SKILL.md"
        legacy.parent.mkdir(parents=True)
        legacy.write_text("---\nname: figma-bro\n---\n")
        self.assertEqual(set(manager.duplicates(self.home, [nested])), {str(p.resolve()) for p in (skill, role, legacy)})
        skill.unlink()
        role.unlink()
        legacy.unlink()
        self.assertEqual(manager.duplicates(self.home, [nested]), [])


if __name__ == "__main__":
    unittest.main()
