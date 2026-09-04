class myClass:

    __privateVar = 46

    def __privMeth(self):
        print("I'm inside class myClass")

    def hello(self):
        print("Private Variable value: ",myClass.__privateVar)

foo = myClass()
foo.hello()
foo.__privMeth