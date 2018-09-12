# python-keypath-extractor

![Travis (.org)](https://img.shields.io/travis/DrJeffreyMorgan/python-keypath-extractor.svg)

Extract Python dictionary values with keypaths into a new dictionary.

## Use

Import the ```KeypathExtractor``` class:

```python
from keypath_extractor import KeypathExtractor
```

Create a dict to extract values from:

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

Keypaths are represented by two-element tuples that contain the name of the key for the extracted value, ```Doors``` and the keypath for extracting the value, ```car.number_of_doors```:

```python
('Doors', 'car.number_of_doors')
```

Create a list of key/keypaths tuples to use to extract values:

```python
keypaths = [
    ('Doors', 'car.number_of_doors'),
    ('Primary Fuel', 'car.fuel_type.0'),
]
```

Create an extractor with the list of keypath tuples and extract the values:

```python
extractor = KeypathExtractor(keypaths)
values = extractor.extract(data_object)
```

After extraction, the ```values``` dict contains the following key/value pairs:

```python
{
    'Doors': 4, 
    'Primary Fuel': 'petrol'
}

```
