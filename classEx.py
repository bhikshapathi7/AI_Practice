# Class is a blueprint which contains variables and methods inside it
# Self Keyword is mandatory to call variables
# Instance and class variables have whole different purposes
# Constructor name should be __init__(self)
#new Keyword is not required at the time of object creation


class Nexon:
    name = 'Nexon'  ## class Variables
    color = 'Red'   ## class Variables
    price = 12.75   ## class Variables

    def __init__(self, name, color, price):
        self.name = name
        self.color = color
        self.price = price
        print('Hey I am Constructor, I will be calling at the time of object creation')


    def start(self, fuel):
        print('Hey I am Super class method')
        print('My car is ' + self.name + ' and it starts with ' + fuel)

    def running(self, kmph):
        print('My car is ' + self.name + ' it runs with ' + kmph)



nexon = Nexon('Thar', 'White', 15.67)
print('################################################')
print(Nexon.name)
print(Nexon.color)
print(Nexon.price)
print('#################################################')
print(nexon.name)
print(nexon.color)
print(nexon.price)
nexon.start('Petrol')
nexon.running('175')







