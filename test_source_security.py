import unittest
from internet_source_collector import is_trusted_open_web_source


class TrustedSourceSecurityTests(unittest.TestCase):
    def test_approved_hosts_and_subdomains(self):
        for url in ["https://archive.org/details/book", "https://www.archive.org/", "https://LIBRARY.STANFORD.EDU/", "https://example.gov/", "https://college.ac.uk/", "https://archive.org./"]:
            with self.subTest(url=url):
                self.assertTrue(is_trusted_open_web_source({"url": url}))

    def test_reject_lookalikes_and_non_host_matches(self):
        for url in ["https://attacker.invalid/?reference=archive.org", "https://archive.org.attacker.invalid/document", "https://attacker.invalid/path.edu/article", "https://notarchive.org/", "https://archive.org@attacker.invalid/", "https://attacker.invalid@archive.org/", "https://archive.org:bad/", "https://archive.org:99999/", "https://archive..org/", "https://archive.org../", "https://archive.org\\@attacker.invalid/", "https://archive.org/\n", "https://archive.org%2eattacker.invalid/", "javascript:archive.org", "file://archive.org/book", "//archive.org/book", "archive.org", None, 42]:
            with self.subTest(url=url):
                self.assertFalse(is_trusted_open_web_source({"url": url}))

    def test_missing_url(self):
        self.assertFalse(is_trusted_open_web_source({}))


if __name__ == "__main__":
    unittest.main()
