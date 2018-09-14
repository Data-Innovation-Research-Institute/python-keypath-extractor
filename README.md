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

Keypaths are represented by tuples that contain a source keypath for extracting the value, ```car.number_of_doors```, and a destination keypath for the extracted value in the new dictionary, ```new data.Door Count```:

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

The default separator is a dot. Supply the optional ```separator``` argument to the ```KeypathExtractor``` constructor to use a different separator:

```python
keypaths = [
    ('car#number_of_doors', 'new data#Door Count'),
    ('car#fuel_type#0', 'new data#Primary Fuel'),
]
extractor = KeypathExtractor(keypaths, separator='#')
values = extractor.extract(data_object)
```

## Value Transformers

Keypath tuples may contain a third element which is a function that will be applied to the extracted value before it is stored at the destination keypath:

```python
def double(value):
    return value * 2

keypaths = [
    ('car.number_of_doors', 'new data.Door Count', double),
]
extractor = KeypathExtractor(keypaths)
values = extractor.extract(data_object)
```

After extraction, the destination keypath, ```new data.Door Count```, will have the value 8, which is the value returned by the ```double``` function when given the value at the source keypath, ```car.number_of_doors```, which is 4:

```python
{
  'new data': {
    'Door Count': 8,
  }
}

```
