import unittest

from keypath_extractor import KeypathExtractor


class KeypathExtractorTest(unittest.TestCase):

    data_object = {
        'car': {
            'manufacturer': 'Ford',
            'number_of_doors': 4,
            'fuel_type': [
                'petrol',
                'diesel'
            ]
        }
    }

    def test_no_keypaths(self):
        keypaths = None
        self.assertRaises(ValueError, KeypathExtractor, keypaths)

    def test_empty_keypaths(self):
        keypaths = []
        extractor = KeypathExtractor(keypaths)
        values = extractor.extract(self.data_object)
        self.assertEqual(values, {})

    def test_keypath(self):
        keypaths = [
            ('Doors', 'car.number_of_doors'),
            ('Primary Fuel', 'car.fuel_type.0'),
        ]
        extractor = KeypathExtractor(keypaths)
        values = extractor.extract(self.data_object)
        self.assertTrue('Doors' in values)
        self.assertEqual(values['Doors'], 4)
        self.assertTrue('Primary Fuel' in values)
        self.assertEqual(values['Primary Fuel'], 'petrol')

    def test_no_key(self):
        keypaths = [
            (None, 'car.number_of_doors'),
        ]
        extractor = KeypathExtractor(keypaths)
        self.assertRaises(ValueError, extractor.extract, self.data_object)

    def test_empty_key(self):
        keypaths = [
            ('', 'car.number_of_doors'),
        ]
        extractor = KeypathExtractor(keypaths)
        self.assertRaises(ValueError, extractor.extract, self.data_object)

    def test_no_keypath(self):
        keypaths = [
            ('Doors', None),
        ]
        extractor = KeypathExtractor(keypaths)
        self.assertRaises(KeyError, extractor.extract, self.data_object)

    def test_empty_keypath(self):
        keypaths = [
            ('Doors', ''),
        ]
        extractor = KeypathExtractor(keypaths)
        self.assertRaises(KeyError, extractor.extract, self.data_object)

    def test_invalid_keypath(self):
        keypaths = [
            ('Doors', 'car.number_of_windows'),
        ]
        extractor = KeypathExtractor(keypaths)
        self.assertRaises(KeyError, extractor.extract, self.data_object)


if __name__ == '__main__':
    unittest.main()
