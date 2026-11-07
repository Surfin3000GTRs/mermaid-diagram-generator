import contextlib
import io
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import watch_mermaid as watch


class WatchTests(unittest.TestCase):
    def setUp(self):
        baseline = patch.object(watch, "VERSION_FILE")
        self.addCleanup(baseline.stop)
        baseline.start().read_text.return_value = "12.3.0\n"

    def test_versions_are_strict_and_numeric(self):
        self.assertGreater(watch.version("12.10.0"), watch.version("12.9.9"))
        for invalid in ("v12.3.0", "12.3.0-rc.1", "12.03.0", "12.3"):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                watch.version(invalid)

    def test_latest_release_checks_exact_package_and_stability(self):
        release = {"draft": False, "prerelease": False, "tag_name": "mermaid@12.3.0",
                   "html_url": "https://example.test/release"}
        with patch.object(watch, "request", side_effect=[{"version": "12.3.0"}, release]):
            self.assertEqual(watch.latest_release("token")[0], "12.3.0")
        release["prerelease"] = True
        with patch.object(watch, "request", side_effect=[{"version": "12.3.0"}, release]):
            with self.assertRaises(ValueError):
                watch.latest_release("token")

    def test_changelog_includes_all_intervening_versions(self):
        text = "# mermaid\n\n## 12.5.0\n\nlatest\n\n## 12.4.0\n\nintermediate\n\n## 12.3.0\n\nold\n"
        result = watch.changelog_excerpt(text, "12.3.0", "12.5.0")
        self.assertIn("intermediate", result)
        self.assertIn("latest", result)
        self.assertNotIn("old", result)
        with self.assertRaises(ValueError):
            watch.changelog_excerpt(text, "12.2.0", "12.5.0")

    def test_find_issue_paginates_and_ignores_pull_requests(self):
        marker = "<!-- marker -->"
        first = [{"body": marker, "user": {"login": "someone"}}] * 99
        first.append({"body": marker, "user": {"login": "github-actions[bot]"}, "pull_request": {}})
        expected = {"body": marker, "number": 123, "user": {"login": "github-actions[bot]"}}
        with patch.object(watch, "request", side_effect=[first, [expected]]) as request:
            self.assertEqual(watch.find_issue("owner/repo", marker, "token"), expected)
            self.assertEqual(request.call_count, 2)

    def test_request_uses_registry_accept_header_without_leaking_token(self):
        response = unittest.mock.MagicMock()
        response.__enter__.return_value = io.BytesIO(b'{"version":"12.3.0"}')
        with patch.object(watch, "urlopen", return_value=response) as urlopen:
            watch.request("https://registry.npmjs.org/mermaid/latest", "secret")
            request = urlopen.call_args.args[0]
            self.assertEqual(request.get_header("Accept"), "application/json")
            self.assertIsNone(request.get_header("Authorization"))

    def test_catalog_reports_both_missing_and_removed_documents(self):
        with patch.object(watch, "syntax_files", return_value={"flowchart", "new"}), \
             patch.object(watch, "catalog_files", return_value={"flowchart", "old"}):
            self.assertEqual(watch.catalog_difference("12.3.0", "token"), (["new"], ["old"]))

    @patch.dict(os.environ, {"GITHUB_REPOSITORY": "owner/repo", "GH_TOKEN": "token"}, clear=True)
    def test_missing_token_creates_issue_then_existing_issue_can_be_assigned(self):
        issue = {"state": "open", "html_url": "https://example.test/1", "number": 1, "assignees": []}
        log = "# mermaid\n\n## 12.4.0\n\nnew\n\n## 12.3.0\n\nold\n"
        with patch.object(watch, "latest_release", return_value=("12.4.0", "https://example.test/release")), \
             patch.object(watch, "catalog_difference", return_value=([], [])), \
             patch.object(watch, "find_issue", return_value=None), \
             patch.object(watch, "read_changelog", return_value=log), \
             patch.object(watch, "request", return_value=issue) as request, \
             contextlib.redirect_stdout(io.StringIO()) as output:
            watch.run()
            self.assertIn("remains unassigned", output.getvalue())
            self.assertIn("## 12.4.0", request.call_args.args[2]["body"])
        with patch.dict(os.environ, {"COPILOT_ASSIGN_TOKEN": "assignment-token"}), \
             patch.object(watch, "latest_release", return_value=("12.4.0", "https://example.test/release")), \
             patch.object(watch, "catalog_difference", return_value=([], [])), \
             patch.object(watch, "find_issue", return_value=issue), \
             patch.object(watch.subprocess, "run") as assign:
            watch.run()
            self.assertIn("@copilot", assign.call_args.args[0])
            self.assertEqual(assign.call_args.kwargs["env"]["GH_TOKEN"], "assignment-token")
            self.assertTrue(assign.call_args.kwargs["check"])

    @patch.dict(os.environ, {"GITHUB_REPOSITORY": "owner/repo", "GH_TOKEN": "token"}, clear=True)
    def test_up_to_date_and_closed_issue_never_create(self):
        with patch.object(watch, "latest_release", return_value=("12.3.0", "https://example.test")), \
             patch.object(watch, "catalog_difference", return_value=([], [])), \
             patch.object(watch, "request") as request:
            watch.run()
            request.assert_not_called()
        issue = {"state": "closed", "html_url": "https://example.test/1"}
        with patch.object(watch, "latest_release", return_value=("12.3.0", "https://example.test")), \
             patch.object(watch, "catalog_difference", return_value=(["new"], [])), \
             patch.object(watch, "find_issue", return_value=issue), \
             patch.object(watch, "request") as request:
            watch.run()
            request.assert_not_called()

    @patch.dict(os.environ, {"GITHUB_REPOSITORY": "owner/repo", "GH_TOKEN": "token",
                             "COPILOT_ASSIGN_TOKEN": "assignment-token"}, clear=True)
    def test_assignment_failure_propagates_and_existing_assignment_is_not_repeated(self):
        issue = {"state": "open", "html_url": "https://example.test/1", "number": 1, "assignees": []}
        with patch.object(watch, "latest_release", return_value=("12.3.0", "https://example.test")), \
             patch.object(watch, "catalog_difference", return_value=(["new"], [])), \
             patch.object(watch, "find_issue", return_value=issue), \
             patch.object(watch.subprocess, "run", side_effect=watch.subprocess.CalledProcessError(1, "gh")):
            with self.assertRaises(watch.subprocess.CalledProcessError):
                watch.run()
        issue["assignees"] = [{"login": "copilot-swe-agent[bot]"}]
        with patch.object(watch, "latest_release", return_value=("12.3.0", "https://example.test")), \
             patch.object(watch, "catalog_difference", return_value=(["new"], [])), \
             patch.object(watch, "find_issue", return_value=issue), \
             patch.object(watch.subprocess, "run") as assign:
            watch.run()
            assign.assert_not_called()


if __name__ == "__main__":
    unittest.main()
