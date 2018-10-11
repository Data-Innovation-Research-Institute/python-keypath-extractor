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
        ],
        'no_value': None
    }
}


class BadKeypathsTests(unittest.TestCase):

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

    def test_too_few_tuple_elements(self):
        keypaths = [
            'one',
        ]
        extractor = KeypathExtractor(keypaths)
        self.assertRaises(ValueError, extractor.extract, data_object)

    def test_too_many_tuple_elements(self):
        keypaths = [
            ('one', 'two', 'three', 'four'),
        ]
        extractor = KeypathExtractor(keypaths)
        self.assertRaises(ValueError, extractor.extract, data_object)


class KeypathExtractionTests(unittest.TestCase):

    def test_empty_keypaths(self):
        keypaths = []
        extractor = KeypathExtractor(keypaths)
        values = extractor.extract(data_object)
        self.assertEqual(values, {})

    def test_keypaths(self):
        keypaths = [
            ('car.number_of_doors', 'new data.Door Count'),
            ('car.fuel_type.0', 'new data.Primary Fuel'),
            ('car.no_value', 'new data.No Value'),
        ]
        extractor = KeypathExtractor(keypaths)
        values = extractor.extract(data_object)
        self.assertTrue('new data' in values)
        self.assertEqual(values['new data']['Door Count'], 4)
        self.assertEqual(values['new data']['Primary Fuel'], 'petrol')
        self.assertEqual(values['new data']['No Value'], None)

    def test_has_keypath(self):
        keypaths = [
            ('car.number_of_doors', 'new data.Door Count'),
            ('car.number_of_windows', 'Windows Count'),
        ]
        extractor = KeypathExtractor(keypaths)
        self.assertTrue(extractor.has_keypath(data_object, keypaths[0]))
        self.assertFalse(extractor.has_keypath(data_object, keypaths[1]))


class ReuseValueObjectTests(unittest.TestCase):

    def test_reuse_value_object(self):
        keypaths1 = [
            ('car.number_of_doors', 'new data.Door Count'),
        ]
        extractor = KeypathExtractor(keypaths1)
        values = extractor.extract(data_object)
        self.assertEqual(values['new data']['Door Count'], 4)

        keypaths2 = [
            ('car.fuel_type.0', 'new data.Primary Fuel'),
        ]
        extractor = KeypathExtractor(keypaths2)
        values = extractor.extract(data_object, values)
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


class TransformerFunctionTests(unittest.TestCase):

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

    def test_no_transformer(self):
        keypaths = [
            ('car.engine_size', 'new data.Capacity', None),
        ]
        extractor = KeypathExtractor(keypaths)
        self.assertRaises(ValueError, extractor.extract, data_object)

    def test_non_callable_transformer(self):
        not_callable = 1
        keypaths = [
            ('car.engine_size', 'new data.Capacity', not_callable),
        ]
        extractor = KeypathExtractor(keypaths)
        self.assertRaises(ValueError, extractor.extract, data_object)


if __name__ == '__main__':
    unittest.main()
