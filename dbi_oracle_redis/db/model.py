from formencode import Schema
from formencode.validators import String, Number

import oracle_con as orcl
import redis_con as redis
from datetime import date, datetime


class Root(dict):
    _instance = None

    def __init__(self):
        super(Root, self).__init__()
        self.load_products()
        self.customers = []
        self.load_customers()

    @staticmethod
    def get_instance():
        if not Root._instance:
            Root._instance = Root()
        return Root._instance

    @orcl.transaction
    def load_products(self):
        cur = orcl.conn.cursor()
        cur.execute('SELECT * FROM stemaa14.PRODUCT')

        for row in cur:
            self[str(row[0])] = Product(*row)

    @orcl.transaction
    def load_customers(self):
        cur = orcl.conn.cursor()
        cur.execute('SELECT * FROM stemaa14.CUSTOMER')

        for row in cur:
            self.customers.append(Customer(*row))


class Product:
    def __init__(self, *args):
        if args and len(args) == 6:
            self.id, self.price, self.price_date, self.product_name, self.image, self.color = args
            self._stars = self._get_stars()

    def add_review(self, review):
        redis.add_review(self.id, review)
        self._stars = self._get_stars()

    def _get_stars(self):
        return redis.get_stars(self.id)

    @property
    def reviews(self):
        for r in redis.get_reviews(self.id):
            yield Review.from_redis(r)

    @property
    def stars(self):
        res = []
        for _ in range(int(self._stars)):
            res.append('fas fa-star')
        rem = self._stars % 1
        if rem > .8:
            res.append('fas fa-star')
        elif rem > .2:
            res.append('fas fa-star-half-alt')
        else:
            res.append('far fa-star')
        for _ in range(4 - int(self._stars)):
            res.append('far fa-star')
        return res


class Review:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.stars = kwargs.get('stars', 0)
        self.statement = kwargs.get('statement', '')
        self.date_of_creation = kwargs.get('date_of_creation', date.today())
        self.description = kwargs.get('description', '')

    def as_dict(self):
        return {'name': self.name,
                'stars': self.stars,
                'statement': self.statement,
                'date_of_creation': str(self.date_of_creation),
                'description': self.description}

    @staticmethod
    def from_redis(data):
        return Review(name=data['name'],
                      stars=int(data['stars']),
                      statement=data['statement'],
                      date_of_creation=datetime.strptime(data['date_of_creation'], '%Y-%m-%d').date(),
                      description=data['description'])

    @property
    def star_classes(self):
        res = []
        for _ in range(int(self.stars)):
            res.append('fas fa-star')
        for _ in range(5 - int(self.stars)):
            res.append('far fa-star')
        return res


class Customer:
    def __init__(self, *args):
        if args and len(args) == 13:
            self.id, self.city, self.company, self.date_of_birth, self.phone, self.ssn, self.state, self.street, \
                self.zip, self.email, self.first_name, self.gender, self.last_name = args


def root_factory(request):
    return Root.get_instance()


class ReviewSchema(Schema):
    filter_extra_fields = True
    allow_extra_fields = True

    name = String(not_empty=True)
    stars = Number(not_empty=True)
    statement = String(not_empty=True)
    description = String(not_empty=True)
