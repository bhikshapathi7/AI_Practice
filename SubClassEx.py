from classEx import Nexon

class SubClass(Nexon):

    def __init__(self, name, color, price):         # Line 1 - Fixed: accept same params as Nexon
        Nexon.__init__(self, name, color, price)    # Line 2 - Fixed: pass all args to parent

    def travel(self, speed):
        print('Hey I am ' + self.name + ' I am running with ' + speed)   # Line 3 - Fixed: added space before 'I'

    def start(self, fuel):                          # Line 4 - Overrides Nexon's start()
        print('Hey I am subclass method')
        print('Hey I am ' + self.name + ' I am running with ' + fuel)    # Line 5 - Fixed: added space


subclass = SubClass('Thar', 'White', 15.67)        # Line 6 - Fixed: pass all 3 arguments
print(subclass.name)
print(subclass.price)
subclass.start('Diesel')                           # Line 7 - Fixed: removed print() wrapper
subclass.travel('123.45')                          # Line 8 - Fixed: removed print() wrapper