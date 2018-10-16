import dpath


class Keypath:

    def __init__(self, source_keypath, destination_keypath, transformer_fn=None, is_optional=False):
        assert source_keypath, 'source keypath cannot be None or empty'
        assert destination_keypath, 'destination keypath cannot be None or empty'
        if transformer_fn:
            assert callable(transformer_fn), 'transformer must be a callable'
        self.source_keypath = source_keypath
        self.destination_keypath = destination_keypath
        self.transformer_fn = transformer_fn
        self.is_optional = is_optional


class KeypathExtractor:
    def __init__(self, keypaths, separator='.'):
        if keypaths is None:
            raise ValueError('keypaths cannot be None')
        else:
            self.separator = separator
            self.keypaths = keypaths

    def has_keypath(self, data_object, source_keypath):
        try:
            dpath.util.get(data_object, source_keypath, separator=self.separator)
            return True
        except KeyError:
            return False

    def extract(self, data_object, values=None):
        if not values:
            values = {}
        for keypath in self.keypaths:
            if not keypath.is_optional:
                value = dpath.util.get(data_object, keypath.source_keypath, separator=self.separator)
            else:
                if self.has_keypath(data_object, keypath.source_keypath):
                    value = dpath.util.get(data_object, keypath.source_keypath, separator=self.separator)
                else:
                    value = None
            if keypath.transformer_fn:
                value = keypath.transformer_fn(value)
            dpath.util.new(values, keypath.destination_keypath, value, separator=self.separator)

        return values
