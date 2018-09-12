import dpath


class KeypathError(Exception):
    pass


class KeypathExtractor:

    def __init__(self, keypaths):
        if keypaths is None:
            raise Exception('keypaths cannot be None')
        else:
            self.keypaths = keypaths

    def extract(self, data_object):
        values = {}
        for key, keypath in self.keypaths:
            if key:
                if keypath:
                    try:
                        values[key] = dpath.util.get(data_object, keypath, separator='.')
                    except KeyError as e:
                        raise KeypathError(e)
                else:
                    raise KeypathError('keypath cannot be None or empty')
            else:
                raise KeyError('key cannot be None or empty')
        return values
