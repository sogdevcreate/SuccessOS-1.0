from __future__ import annotations

import unittest

from infrastructure.browser.browser_policy_manager import (
    BrowserPolicyError,
    BrowserPolicyManager,
)


class BrowserPolicyManagerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.confirmations: list[str] = []
        self.manager = BrowserPolicyManager(
            allowed_domains=("example.com", "youtube.com"),
            confirmation_provider=self.confirmations.append,
        )

    def test_normalizes_allowed_web_url(self) -> None:
        url = self.manager.authorize_navigation(
            " HTTPS://WWW.Example.COM/Path?x=1#section "
        )

        self.assertEqual(url, "https://www.example.com/Path?x=1#section")

    def test_allows_subdomains_but_not_domain_lookalikes(self) -> None:
        self.assertEqual(
            self.manager.authorize_navigation("https://api.example.com"),
            "https://api.example.com/",
        )

        with self.assertRaises(BrowserPolicyError):
            self.manager.authorize_navigation("https://example.com.attacker.test")

    def test_blocks_disallowed_domain(self) -> None:
        with self.assertRaises(BrowserPolicyError):
            self.manager.authorize_navigation("https://attacker.test/")

    def test_blocks_unsafe_and_missing_schemes_by_default(self) -> None:
        for url in (
            "javascript:alert(1)",
            "data:text/html,test",
            "file:///C:/secret.txt",
            "https://user:password@example.com/",
            "example.com/path",
        ):
            with self.subTest(url=url):
                with self.assertRaises(BrowserPolicyError):
                    self.manager.authorize_navigation(url)

    def test_explicitly_allowed_non_web_scheme_is_accepted(self) -> None:
        manager = BrowserPolicyManager(
            allowed_schemes=("file",),
        )

        self.assertEqual(
            manager.authorize_navigation("file:///C:/approved.txt"),
            "file:///C:/approved.txt",
        )

    def test_upload_requires_confirmation(self) -> None:
        with self.assertRaises(BrowserPolicyError):
            self.manager.authorize_upload("C:\\secret.txt")

        self.assertEqual(self.confirmations, ["Upload local file 'C:\\secret.txt'"])

    def test_form_submission_with_local_path_requires_confirmation(self) -> None:
        with self.assertRaises(BrowserPolicyError):
            self.manager.authorize_form_submission(("C:\\secret.txt",))

        self.assertEqual(
            self.confirmations,
            ["Submit a form containing a local file path"],
        )

    def test_form_submission_without_local_path_does_not_confirm(self) -> None:
        self.manager.authorize_form_submission(("ordinary text", "42"))

        self.assertEqual(self.confirmations, [])

    def test_local_path_detection_supports_windows_unc_and_posix_paths(self) -> None:
        for value in ("C:\\file.txt", "\\\\server\\share", "/tmp/file.txt"):
            with self.subTest(value=value):
                self.assertTrue(self.manager.contains_local_file_path(value))


if __name__ == "__main__":
    unittest.main()
