import dpath


class KeypathExtractor:

    def __init__(self, keypaths):
        if keypaths is None:
            raise ValueError('keypaths cannot be None')
        else:
            self.keypaths = keypaths

    def extract(self, data_object):
        values = {}
        for key, keypath in self.keypaths:
            if key:
                if keypath:
                    values[key] = dpath.util.get(data_object, keypath, separator='.')
                else:
                    raise KeyError('keypath cannot be None or empty')
            else:
                raise ValueError('key cannot be None or empty')
        return values
