
import redis
import pickle

class Base(object):
    def __init__(self, name, host='127.0.0.1', port=6379):
        self.redis = redis.StrictRedis(host, port)
        self.name = name

    def __len__(self):
        return self.redis.llen(self.name)

    def _dumps(self, item):
        try:
            return pickle.dumps(item)
        except:
            return None

    def _loads(self, item):
        try:
            return pickle.loads(item)
        except:
            return None

    def content(self):
        return [self._loads(item) for item in self.redis.lrange(self.name, 0, -1)]

    def clear(self):
        try:
            self.redis.delete(self.name)
            return True
        except:
            return False

    def addAll(self, collection=[]):
        assert type(collection) == list
        with self.redis.pipeline() as pipe:
            for element in collection:
                try:
                    pipe.lpush(self.name, self._dumps(element))
                except:
                    continue
            pipe.execute()

    def __iter__(self):
        return self

    def next(self):
        try:
            got = self.pop()
            if got:
                return got
            raise StopIteration
        except:
            raise StopIteration
