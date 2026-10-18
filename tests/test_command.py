import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
NODE = shutil.which("node")


@unittest.skipUnless(NODE, "Node.js required for npx entrypoint tests")
class CommandTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.home = self.base / "isolated home"
        self.project = self.base / "active project"
        self.project.mkdir()
        self.skill = self.home / ".agents/skills/figma-bro"
        self.agent = self.home / ".codex/agents/figma-bro.toml"

    def run_cli(self, *args, expected=0, cwd=None, env=None):
        result = subprocess.run([NODE, str(ROOT / "bin/cli.cjs"), *args],
                                cwd=cwd or self.project, env=env,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def managed(self, *args, **kwargs):
        return self.run_cli(*args, "--home-root", str(self.home), **kwargs)

    def test_default_command_installs_both_notices_and_displays_connection_guide(self):
        result = self.managed()
        expected = ROOT / "skills/figma-bro"
        for source in expected.rglob("*"):
            if source.is_file():
                self.assertEqual((self.skill / source.relative_to(expected)).read_bytes(), source.read_bytes())
        self.assertEqual(self.agent.read_bytes(), (ROOT / "agents/figma-bro.toml").read_bytes())
        self.assertIn("Figma connection: NOT CHECKED", result.stdout)
        self.assertIn("/plugins", result.stdout)
        self.assertIn("Verification prompt", result.stdout)
        self.assertIn("Do not create or edit", result.stdout)

    def test_repeat_and_explicit_update_are_idempotent_then_uninstall_cleans_both(self):
        self.managed()
        state = self.home / ".codex/figma-bro-codex/install.json"
        original = state.read_bytes()
        for args in [(), ("update",)]:
            result = self.managed(*args)
            self.assertEqual(json.JSONDecoder().raw_decode(result.stdout)[0]["result"], "already-current")
            self.assertEqual(state.read_bytes(), original)
        status = self.managed("status")
        self.assertFalse(json.loads(status.stdout)["modified"])
        self.assertNotIn("Connect Figma", status.stdout)
        removal = self.managed("uninstall")
        self.assertEqual(json.loads(removal.stdout)["result"], "uninstalled")
        self.assertFalse(self.skill.exists())
        self.assertFalse(self.agent.exists())
        self.assertFalse(state.exists())

    def test_unmanaged_refusal_and_explicit_replace_restore_initial_files(self):
        self.skill.mkdir(parents=True)
        (self.skill / "notes.md").write_text("Preserve this custom note\n")
        self.agent.parent.mkdir(parents=True)
        self.agent.write_text("Previous custom agent\n")
        result = self.managed(expected=1)
        self.assertIn("unmanaged", result.stderr)
        self.assertNotIn("Connect Figma", result.stdout)
        self.managed("--replace")
        self.managed("uninstall")
        self.assertEqual((self.skill / "notes.md").read_text(), "Preserve this custom note\n")
        self.assertEqual(self.agent.read_text(), "Previous custom agent\n")

    def test_modified_managed_files_are_protected(self):
        self.managed()
        self.agent.write_text("Local changes\n")
        result = self.managed("update", expected=1)
        self.assertIn("edited or removed", result.stderr)
        self.assertNotIn("custom agent are installed", result.stdout)
        self.assertEqual(self.agent.read_text(), "Local changes\n")

    def test_default_project_check_uses_callers_git_root_from_nested_directory(self):
        subprocess.run(["git", "init", "-q", str(self.project)], check=True)
        duplicate = self.project / ".agents/skills/old-name/SKILL.md"
        duplicate.parent.mkdir(parents=True)
        duplicate.write_text("---\nname: figma-bro\n---\n")
        nested = self.project / "src/nested"
        nested.mkdir(parents=True)
        result = self.managed(expected=1, cwd=nested)
        self.assertIn("Duplicate definitions", result.stderr)
        self.assertFalse(self.skill.exists())
        self.assertFalse(self.agent.exists())

    def test_invalid_option_fails_before_installation(self):
        self.managed("--unknown-option", expected=2)
        self.assertFalse(self.home.exists())

    def test_help_version_and_connection_guide_do_not_need_python_or_mutate_home(self):
        environment = dict(os.environ, PATH=str(self.base / "no-executables"))
        self.run_cli("--help", env=environment)
        version = self.run_cli("--version", env=environment)
        self.assertEqual(version.stdout.strip(), (ROOT / "VERSION").read_text().strip())
        connection = self.run_cli("connect", env=environment)
        self.assertIn("NOT CHECKED", connection.stdout)
        self.assertFalse(self.home.exists())

    def test_missing_python_fails_before_modifying_targets(self):
        environment = dict(os.environ, PATH=str(self.base / "no-executables"))
        result = self.managed(expected=1, env=environment)
        self.assertIn("Python 3.9+", result.stderr)
        self.assertFalse(self.home.exists())


if __name__ == "__main__":
    unittest.main()
