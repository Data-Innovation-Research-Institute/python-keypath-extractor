import dpath


class KeypathExtractor:

    def __init__(self, keypaths, separator='.'):
        if keypaths is None:
            raise ValueError('keypaths cannot be None')
        else:
            self.separator = separator
            self.keypaths = keypaths

    def extract(self, data_object):
        values = {}
        for keypath in self.keypaths:
            if len(keypath) == 2:
                source_keypath, destination_keypath = keypath
                transform_fn = None
            elif len(keypath) == 3:
                source_keypath, destination_keypath, transform_fn = keypath
            if source_keypath:
                if destination_keypath:
                    value = dpath.util.get(data_object, source_keypath, separator=self.separator)
                    if callable(transform_fn):
                        value = transform_fn(value)
                    dpath.util.new(values, destination_keypath, value, separator=self.separator)
                else:
                    raise KeyError('destination keypath cannot be None or empty')
            else:
                raise KeyError('source keypath cannot be None or empty')
        return values
