class Computer:

    def __init__(self):
        self.__maxprice = 1350

    def sell(self):
        print("Selling Price: {}".format(self.__maxprice))

    def setMaxPrice(self, price):
        self.__maxprice = price

c = Computer()
c.sell()

c.__maxprice = 1500
c.sell()

c.setMaxPrice(1650)
c.sell()