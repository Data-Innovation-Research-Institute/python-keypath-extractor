import dpath


class KeypathExtractor:

    separator = '.'

    def __init__(self, keypaths):
        if keypaths is None:
            raise ValueError('keypaths cannot be None')
        else:
            self.keypaths = keypaths

    def extract(self, data_object):
        values = {}
        for source_keypath, destination_keypath in self.keypaths:
            if source_keypath:
                if destination_keypath:
                    value = dpath.util.get(data_object, source_keypath, separator=self.separator)
                    dpath.util.new(values, destination_keypath, value, separator=self.separator)
                else:
                    raise KeyError('destination keypath cannot be None or empty')
            else:
                raise KeyError('source keypath cannot be None or empty')
        return values
