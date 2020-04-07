import os


class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Environ(metaclass=MetaSingleton):
    env = None

    def get(self):
        if self.env is None:
            self.env = self._readEnv()
        return self.env

    def _readEnv(self):
        with open('config.env', 'r') as fh:
            result = dict(
                tuple(line.split('='))
                for line in fh.read().splitlines()
                if not line.startswith('#')
            )
            # debug
            # print result
            return result
