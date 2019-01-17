from redis import Redis


_redis = Redis()


def add_review(prod_id, review):
    keys = [int(i.split(':')[-1]) for i in _redis.keys(str(prod_id) + ':review:*')]
    new_id = max(keys)+1 if len(keys) > 0 else 1
    _redis.hmset('%d:review:%d' % (prod_id, new_id), review.as_dict())


def get_reviews(id):
    for key in _redis.keys('%d:review:*' % id):
        yield _redis.hgetall(key)


def get_stars(id):
    stars = [int(_redis.hget(key, 'stars')) for key in _redis.keys('%d:review:*' % id)]
    return sum(stars) / len(stars) if len(stars) > 0 else 0
