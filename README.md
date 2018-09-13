# python-keypath-extractor

![Travis (.org)](https://img.shields.io/travis/DrJeffreyMorgan/python-keypath-extractor.svg)

Extract Python dictionary values with keypaths into a new dictionary.

## Use

Import the ```KeypathExtractor``` class:

```python
from keypath_extractor import KeypathExtractor
```

Create a dictionary to extract values from:

```python
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
```

Keypaths are represented by two-element tuples that contain the keypath for extracting the value, ```car.number_of_doors```, and the keypath for the extracted value in the new dictionary, ```new data.Door Count```:

```python
('car.number_of_doors', 'new data.Door Count')
```

Create a list of keypath tuples to use to extract values:

```python
keypaths = [
    ('car.number_of_doors', 'new data.Door Count'),
    ('car.fuel_type.0', 'new data.Primary Fuel'),
]
```

Create an extractor with the list of keypath tuples and extract the values:

```python
extractor = KeypathExtractor(keypaths)
values = extractor.extract(data_object)
```

After extraction, the ```values``` dictionary contains the following key/value pairs:

```python
{
  'new data': {
    'Door Count': 4,
    'Primary Fuel': 'petrol'
  }
}

```

## Separators

The default separator is a dot. Supply the optional ```separator``` argument to the ```KeypathExtractor``` to use a different separator:

```python
keypaths = [
    ('car#number_of_doors', 'new data#Door Count'),
    ('car#fuel_type#0', 'new data#Primary Fuel'),
]
extractor = KeypathExtractor(keypaths, separator='#')
values = extractor.extract(self.data_object)
```
