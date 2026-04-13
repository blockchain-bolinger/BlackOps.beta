import unittest
from tools.recon.social_hunter_v7 import SocialHunter

class TestSocialHunter(unittest.TestCase):
    def test_search_username(self):
        hunter = SocialHunter()
        result = hunter.search("testuser")
        self.assertIsInstance(result, list)