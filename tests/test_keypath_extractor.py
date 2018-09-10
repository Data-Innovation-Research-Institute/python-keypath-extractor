import unittest

from keypath_extractor import KeypathExtractor


class KeypathExtractorTest(unittest.TestCase):

    def test_keypath_extractor(self):
        extractor = KeypathExtractor()
        self.assertIsInstance(extractor, KeypathExtractor)


if __name__ == '__main__':
    unittest.main()

