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

    def test_keypaths(self):
        keypaths = [
            ('car.number_of_doors', 'new data.Door Count'),
            ('car.fuel_type.0', 'new data.Primary Fuel'),
        ]
        extractor = KeypathExtractor(keypaths)
        values = extractor.extract(self.data_object)
        self.assertTrue('new data' in values)
        self.assertEqual(values['new data']['Door Count'], 4)
        self.assertEqual(values['new data']['Primary Fuel'], 'petrol')

    def test_keypath_separator(self):
        keypaths = [
            ('car#number_of_doors', 'new data#Door Count'),
            ('car#fuel_type#0', 'new data#Primary Fuel'),
        ]
        extractor = KeypathExtractor(keypaths, separator='#')
        values = extractor.extract(self.data_object)
        self.assertTrue('new data' in values)
        self.assertEqual(values['new data']['Door Count'], 4)
        self.assertEqual(values['new data']['Primary Fuel'], 'petrol')

    def test_no_source_keypath(self):
        keypaths = [
            (None, 'Doors'),
        ]
        extractor = KeypathExtractor(keypaths)
        self.assertRaises(KeyError, extractor.extract, self.data_object)

    def test_empty_source_keypath(self):
        keypaths = [
            ('', 'Doors'),
        ]
        extractor = KeypathExtractor(keypaths)
        self.assertRaises(KeyError, extractor.extract, self.data_object)

    def test_invalid_source_keypath(self):
        keypaths = [
            ('car.number_of_windows', 'Windows Count'),
        ]
        extractor = KeypathExtractor(keypaths)
        self.assertRaises(KeyError, extractor.extract, self.data_object)

    def test_no_destination_keypath(self):
        keypaths = [
            ('car.number_of_doors', None),
        ]
        extractor = KeypathExtractor(keypaths)
        self.assertRaises(KeyError, extractor.extract, self.data_object)

    def test_empty_destination_keypath(self):
        keypaths = [
            ('car.number_of_doors', ''),
        ]
        extractor = KeypathExtractor(keypaths)
        self.assertRaises(KeyError, extractor.extract, self.data_object)


if __name__ == '__main__':
    unittest.main()
