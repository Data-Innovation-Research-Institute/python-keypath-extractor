import unittest

from keypath_extractor import KeypathExtractor
from keypath_extractor import Keypath

data_object = {
    'car': {
        'manufacturer': 'Ford',
        'number_of_doors': 4,
        'engine_size': 2.0,
        'fuel_type': [
            'petrol',
            'diesel'
        ],
        'no_value': None
    }
}


class BadKeypathsTests(unittest.TestCase):

    def test_no_keypaths(self):
        keypaths = None
        self.assertRaises(ValueError, KeypathExtractor, keypaths)

    def test_no_source_keypath(self):
        self.assertRaises(KeyError, Keypath, None, 'Doors')

    def test_empty_source_keypath(self):
        self.assertRaises(KeyError, Keypath, '', 'Doors')

    def test_invalid_source_keypath(self):
        keypaths = [
            Keypath('car.number_of_windows', 'Windows Count'),
        ]
        extractor = KeypathExtractor(keypaths)
        self.assertRaises(KeyError, extractor.extract, data_object)

    def test_optional_keypath(self):
        keypaths = [
            Keypath('car.number_of_windows', 'Windows Count', is_optional=True),
        ]
        extractor = KeypathExtractor(keypaths)
        extractor.extract(data_object)

    def test_no_destination_keypath(self):
        self.assertRaises(KeyError, Keypath, 'car.number_of_doors', None)

    def test_empty_destination_keypath(self):
        self.assertRaises(KeyError, Keypath, 'car.number_of_doors', '')


class KeypathExtractionTests(unittest.TestCase):

    def test_empty_keypaths(self):
        keypaths = []
        extractor = KeypathExtractor(keypaths)
        values = extractor.extract(data_object)
        self.assertEqual(values, {})

    def test_keypaths(self):
        keypaths = [
            Keypath('car.number_of_doors', 'new data.Door Count'),
            Keypath('car.fuel_type.0', 'new data.Primary Fuel'),
            Keypath('car.no_value', 'new data.No Value'),
        ]
        extractor = KeypathExtractor(keypaths)
        values = extractor.extract(data_object)
        self.assertTrue('new data' in values)
        self.assertEqual(values['new data']['Door Count'], 4)
        self.assertEqual(values['new data']['Primary Fuel'], 'petrol')
        self.assertEqual(values['new data']['No Value'], None)

    def test_has_keypath(self):
        keypaths = [
            Keypath('car.number_of_doors', 'new data.Door Count'),
            Keypath('car.number_of_windows', 'Windows Count'),
        ]
        extractor = KeypathExtractor(keypaths)
        self.assertTrue(extractor.has_keypath(data_object, keypaths[0].source_keypath))
        self.assertFalse(extractor.has_keypath(data_object, keypaths[1].source_keypath))


class ReuseValueObjectTests(unittest.TestCase):

    def test_reuse_value_object(self):
        keypaths1 = [
            Keypath('car.number_of_doors', 'new data.Door Count'),
        ]
        extractor = KeypathExtractor(keypaths1)
        values = extractor.extract(data_object)
        self.assertEqual(values['new data']['Door Count'], 4)

        keypaths2 = [
            Keypath('car.fuel_type.0', 'new data.Primary Fuel'),
        ]
        extractor = KeypathExtractor(keypaths2)
        values = extractor.extract(data_object, values)
        self.assertEqual(values['new data']['Door Count'], 4)
        self.assertEqual(values['new data']['Primary Fuel'], 'petrol')


class KeypathSeparatorTest(unittest.TestCase):

    def test_keypath_separator(self):
        keypaths = [
            Keypath('car#number_of_doors', 'new data#Door Count'),
            Keypath('car#fuel_type#0', 'new data#Primary Fuel'),
        ]
        extractor = KeypathExtractor(keypaths, separator='#')
        values = extractor.extract(data_object)
        self.assertTrue('new data' in values)
        self.assertEqual(values['new data']['Door Count'], 4)
        self.assertEqual(values['new data']['Primary Fuel'], 'petrol')


def double(value):
    return value * 2


class TransformerFunctionTests(unittest.TestCase):

    @staticmethod
    def triple(value):
        return value * 3

    def test_transformer_function(self):
        keypaths = [
            Keypath('car.number_of_doors', 'new data.Door Count', transformer_fn=double),
        ]
        extractor = KeypathExtractor(keypaths)
        values = extractor.extract(data_object)
        self.assertEqual(values['new data']['Door Count'], 8)

    def test_transformer_method(self):
        keypaths = [
            Keypath('car.engine_size', 'new data.Capacity', transformer_fn=self.triple),
        ]
        extractor = KeypathExtractor(keypaths)
        values = extractor.extract(data_object)
        self.assertEqual(values['new data']['Capacity'], 6.0)

    def test_non_callable_transformer(self):
        not_callable = 1
        self.assertRaises(ValueError, Keypath, 'car.engine_size', 'new data.Capacity', transformer_fn=not_callable)


if __name__ == '__main__':
    unittest.main()
