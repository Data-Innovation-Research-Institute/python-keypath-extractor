# python-keypath-extractor

![Travis (.org)](https://img.shields.io/travis/DrJeffreyMorgan/python-keypath-extractor.svg)

Extract Python dictionary values with keypaths into a new dictionary.

## Use

Import the ```Keypath``` and ```KeypathExtractor``` classes:

```python
from keypath_extractor import Keypath, KeypathExtractor
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

Keypaths are represented by `Keypath` objects that contain a source keypath for extracting the value, ```car.number_of_doors```, and a destination keypath for the extracted value in the new dictionary, ```new data.Door Count```:

```python
Keypath('car.number_of_doors', 'new data.Door Count')
```

Create a list of keypath objects to use to extract values:

```python
keypaths = [
    Keypath('car.number_of_doors', 'new data.Door Count'),
    Keypath('car.fuel_type.0', 'new data.Primary Fuel'),
]
```

Create an extractor with the list of keypath objects and extract the values:

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
    Keypath('car#number_of_doors', 'new data#Door Count'),
    Keypath('car#fuel_type#0', 'new data#Primary Fuel'),
]
extractor = KeypathExtractor(keypaths, separator='#')
values = extractor.extract(data_object)
```

## Value Transformers

`Keypath` objects may contain an optional `transformer_fn` parameter which is a function that will be applied to the extracted value before it is stored at the destination keypath:

```python
def double(value):
    return value * 2

keypaths = [
    Keypath('car.number_of_doors', 'new data.Door Count', transformer_fn=double),
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
