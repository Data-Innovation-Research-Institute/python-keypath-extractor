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
                transformer_fn = None
            elif len(keypath) == 3:
                source_keypath, destination_keypath, transformer_fn = keypath
                if not callable(transformer_fn):
                    raise ValueError('transformer must be a callable')
            if source_keypath:
                if destination_keypath:
                    value = dpath.util.get(data_object, source_keypath, separator=self.separator)
                    if transformer_fn:
                        value = transformer_fn(value)
                    dpath.util.new(values, destination_keypath, value, separator=self.separator)
                else:
                    raise KeyError('destination keypath cannot be None or empty')
            else:
                raise KeyError('source keypath cannot be None or empty')
        return values
