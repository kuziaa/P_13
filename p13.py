import logging
import random
from collections import Iterable

log = logging.basicConfig(filename='p13_log.txt', filemode='w', level=logging.INFO)


class Store(object):

    def __init__(self, name, supported_product_types):
        self.name = name
        self.__assortment = []
        self.__supported_product_types = set()
        self.add_supported_product_types(supported_product_types)

    @property
    def assortment(self):
        return self.__assortment

    @property
    def supported_product_types(self):
        return self.__supported_product_types

    def add_item(self, item):
        assert isinstance(item, tuple(self.supported_product_types)), (
            'Product type {} is not supported in {} store'.format(type(item), self.name))
        self.__assortment.append(item)
        logging.info('{} was added in {} store'.format(item, self.name))

    def add_items(self, items):
        assert isinstance(items, Iterable), 'items must be iterable'
        for item in items:
            self.add_item(item)

    def remove_items_by_type(self, removable_type):
        assert issubclass(removable_type, Goods), "removable_type must be Goods' subclass"
        will_be_removed = filter(lambda x: isinstance(x, removable_type), self.__assortment)
        self.__assortment = filter(lambda x: not isinstance(x, removable_type), self.__assortment)
        logging.info('{} were removed from {} store'.format(will_be_removed, self.name))

    def remove_items_by_types(self, removable_types):
        assert isinstance(removable_types, Iterable), 'removable_types must be iterable'
        for removable_type in removable_types:
            self.remove_items_by_type(removable_type)

    def remove_all_items(self):
        self.__assortment = []
        logging.info('all goods were removed from {} store'.format(self.name))

    def add_supported_product_type(self, product_type):
        assert issubclass(product_type, Goods), "Product type must be Goods' subclass"
        self.__supported_product_types.add(product_type)
        logging.info('{} store supports new type of goods: {}'.format(self.name, product_type))

    def add_supported_product_types(self, product_types):
        assert isinstance(product_types, Iterable), 'product_types must be iterable'
        for product_type in product_types:
            self.add_supported_product_type(product_type)

    @property
    def total_cost_without_discount(self):
        return sum([item.price for item in self.__assortment])

    @property
    def total_cost_with_discount(self):
        return sum([item.price * (1 - item.discount / 100.0) for item in self.__assortment])


class GroceryStore(Store):
    def __init__(self, name):
        super(GroceryStore, self).__init__(name, supported_product_types={Food})


class HardwareStore(Store):

    def __init__(self, name):
        super(HardwareStore, self).__init__(name, supported_product_types={Tools})


class Goods(object):

    def __init__(self, price, name):
        self.__freeze_price = False
        self.__discount = 0
        self.__price = price
        self.name = name

    def __repr__(self):
        return '{} - {}$'.format(self.name, self.price)

    @property
    def is_price_frozen(self):
        return self.__freeze_price

    def freeze_price_on(self):
        self.__freeze_price = True
        logging.info('price for {} is frozen'.format(self))

    def freeze_price_off(self):
        self.__freeze_price = False
        logging.info('price for {} is unfrozen'.format(self))

    @property
    def discount(self):
        return self.__discount

    def set_discount(self, discount):
        if self.is_price_frozen:
            print('discount can not be set. Price was frozen')
            return
        assert isinstance(discount, (int, float, long)), ('discount must be a number, '
                                                          'but now {}'.format(type(discount)))
        assert 0 <= discount <= 100, 'discount must be within "0 <= discount <= 100"'
        self.__discount = discount
        logging.info('discount for {} was changed. Now it is {} percents'.format(self, self.discount))

    def reset_discount(self):
        self.set_discount(0)

    def change_discount(self, change_discount_for):
        assert isinstance(change_discount_for, (int, float, long)), ('"change_discount_for" must be a number, '
                                                                     'but now {}'.format(type(change_discount_for)))
        self.set_discount(self.discount + change_discount_for)

    @property
    def price(self):
        return self.__price

    def set_price(self, price):
        if self.is_price_frozen:
            print('Price can not be set. Price was frozen')
            return
        assert isinstance(price, (int, float, long)), '"price" must be a number, but now {}'.format(type(price))
        assert price >= 0, '"price" must be >= 0'
        self.__price = price
        logging.info('price for {} was changed. Now it is {}'.format(self.name, self))

    def change_price(self, change_price_for):
        assert isinstance(change_price_for, (int, float, long)), ('"change_price_for" must be a number, '
                                                                  'but now {}'.format(type(change_price_for)))
        self.set_price(self.__price + change_price_for)


class Food(Goods):
    def __init__(self, price, name):
        super(Food, self).__init__(price, name)


class Tools(Goods):
    def __init__(self, price, name):
        super(Tools, self).__init__(price, name)


class Banana(Food):
    def __init__(self, price=0):
        super(Banana, self).__init__(price, name='Banana')


class Apple(Food):
    def __init__(self, price=0):
        super(Apple, self).__init__(price, name='Apple')
    pass


class Ham(Food):
    def __init__(self, price=0):
        super(Ham, self).__init__(price, name='Ham')


class Bread(Food):
    def __init__(self, price=0):
        super(Bread, self).__init__(price, name='Bread')


class Nail(Tools):
    def __init__(self, price=0):
        super(Nail, self).__init__(price, name='Nail')


class Axe(Tools):
    def __init__(self, price=0):
        super(Axe, self).__init__(price, name='Axe')


class Saw(Tools):
    def __init__(self, price=0):
        super(Saw, self).__init__(price, name='Saw')


class Shovel(Tools):
    def __init__(self, price=0):
        super(Shovel, self).__init__(price, name='Shovel')


grocery_1 = GroceryStore('Riga')
hardware_1 = HardwareStore('Oma')
hardware_2 = HardwareStore('Materik')

grocery_1.add_item(Banana(3))
hardware_1.add_item(Shovel(7))
hardware_2.add_item(Axe(5))

grocery_1.add_items([random.choice([Banana(3), Apple(2), Ham(7), Bread(1)]) for _ in xrange(20)])
hardware_1.add_items([random.choice([Nail(1), Axe(5), Saw(4), Shovel(3)]) for _ in xrange(20)])
hardware_2.add_items([random.choice([Nail(1), Axe(5), Saw(4), Shovel(3)]) for _ in xrange(20)])

for item in grocery_1.assortment:
    item.set_discount(random.randint(0, 50))
    item.change_price(random.randint(0, 7))

for item in hardware_1.assortment:
    item.set_discount(random.randint(0, 50))
    item.change_price(random.randint(0, 7))

for item in hardware_2.assortment:
    item.set_discount(random.randint(0, 50))
    item.change_price(random.randint(0, 7))

logging.info('{} store; value of all goods without discount = {}'.format(grocery_1.name,
                                                                         grocery_1.total_cost_without_discount))
logging.info('{} store; value of all goods without discount = {}'.format(hardware_1.name,
                                                                         hardware_1.total_cost_without_discount))
logging.info('{} store; value of all goods without discount = {}'.format(hardware_2.name,
                                                                         hardware_2.total_cost_without_discount))

logging.info('{} store; value of all goods with discount = {}'.format(grocery_1.name,
                                                                      grocery_1.total_cost_with_discount))
logging.info('{} store; value of all goods with discount = {}'.format(hardware_1.name,
                                                                      hardware_1.total_cost_with_discount))
logging.info('{} store; value of all goods with discount = {}'.format(hardware_2.name,
                                                                      hardware_2.total_cost_with_discount))

logging.info("{} store's assortment: {}".format(grocery_1.name, grocery_1.assortment))
logging.info("{} store's assortment: {}".format(hardware_1.name, hardware_1.assortment))
logging.info("{} store's assortment: {}".format(hardware_2.name, hardware_2.assortment))
