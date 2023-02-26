from dora_bora import database


class DatabaseAccessor:
    def __init__(self, dbname=None):
        self._dbname = dbname
        self._klasses = {
            getattr(database, klass).table: getattr(database, klass)
            for klass in database.__all__
        }

    def __getattr__(self, name):
        if not (name in self._klasses.keys()):
            raise AttributeError(name)

        if self._dbname:
            setattr(self, name, self._klasses[name](self._dbname))
        else:
            setattr(self, name, self._klasses[name]())

        return super().__getattribute__(name)
