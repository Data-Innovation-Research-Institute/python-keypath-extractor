import unittest

from keypath_extractor import KeypathExtractor

data_object = {
    'car': {
        'manufacturer': 'Ford',
        'number_of_doors': 4,
        'engine_size': 2.0,
        'fuel_type': [
            'petrol',
            'diesel'
        ]
    }
}


class BadKeypathsTest(unittest.TestCase):

    def test_no_keypaths(self):
        keypaths = None
        self.assertRaises(ValueError, KeypathExtractor, keypaths)

    def test_no_source_keypath(self):
        keypaths = [
            (None, 'Doors'),
        ]
        extractor = KeypathExtractor(keypaths)
        self.assertRaises(KeyError, extractor.extract, data_object)

    def test_empty_source_keypath(self):
        keypaths = [
            ('', 'Doors'),
        ]
        extractor = KeypathExtractor(keypaths)
        self.assertRaises(KeyError, extractor.extract, data_object)

    def test_invalid_source_keypath(self):
        keypaths = [
            ('car.number_of_windows', 'Windows Count'),
        ]
        extractor = KeypathExtractor(keypaths)
        self.assertRaises(KeyError, extractor.extract, data_object)

    def test_no_destination_keypath(self):
        keypaths = [
            ('car.number_of_doors', None),
        ]
        extractor = KeypathExtractor(keypaths)
        self.assertRaises(KeyError, extractor.extract, data_object)

    def test_empty_destination_keypath(self):
        keypaths = [
            ('car.number_of_doors', ''),
        ]
        extractor = KeypathExtractor(keypaths)
        self.assertRaises(KeyError, extractor.extract, data_object)


class KeypathExtractionTest(unittest.TestCase):

    def test_empty_keypaths(self):
        keypaths = []
        extractor = KeypathExtractor(keypaths)
        values = extractor.extract(data_object)
        self.assertEqual(values, {})

    def test_keypaths(self):
        keypaths = [
            ('car.number_of_doors', 'new data.Door Count'),
            ('car.fuel_type.0', 'new data.Primary Fuel'),
        ]
        extractor = KeypathExtractor(keypaths)
        values = extractor.extract(data_object)
        self.assertTrue('new data' in values)
        self.assertEqual(values['new data']['Door Count'], 4)
        self.assertEqual(values['new data']['Primary Fuel'], 'petrol')


class KeypathSeparatorTest(unittest.TestCase):

    def test_keypath_separator(self):
        keypaths = [
            ('car#number_of_doors', 'new data#Door Count'),
            ('car#fuel_type#0', 'new data#Primary Fuel'),
        ]
        extractor = KeypathExtractor(keypaths, separator='#')
        values = extractor.extract(data_object)
        self.assertTrue('new data' in values)
        self.assertEqual(values['new data']['Door Count'], 4)
        self.assertEqual(values['new data']['Primary Fuel'], 'petrol')


def double(value):
    return value * 2


class TransformerFunctionTest(unittest.TestCase):

    @staticmethod
    def triple(value):
        return value * 3

    def test_transformer_function(self):
        keypaths = [
            ('car.number_of_doors', 'new data.Door Count', double),
        ]
        extractor = KeypathExtractor(keypaths)
        values = extractor.extract(data_object)
        self.assertEqual(values['new data']['Door Count'], 8)

    def test_transformer_method(self):
        keypaths = [
            ('car.engine_size', 'new data.Capacity', self.triple),
        ]
        extractor = KeypathExtractor(keypaths)
        values = extractor.extract(data_object)
        self.assertEqual(values['new data']['Capacity'], 6.0)


if __name__ == '__main__':
    unittest.main()
