import unittest

# 1. Decorator1
    # idea 1 
    # python can return a method
    # idea 2
    # python can nest methods

def parent(num):
    def first_child():
        return "Printing from the first_child() function."

    def second_child():
        return "Printing from the second_child() function."

    # Python Style: Don't afraid of using exceptions
    if num == 10:
        return first_child
    else:
        return second_child
        
# 2. Decorator 2
    # decorator is a pattern to 
    #   1. get a function 
    #   2. returns wrapper (inner function) that wraps the inner function.
def my_decorator2(some_function):
    def wrapper():
        result = some_function()
        return result
    return wrapper
    
def just_some_function2():
    print("Wheee!")
    
# 3. Decorator 3
# syntactic sugar
def my_decorator3(some_function):
    def wrapper(num):
        if num == 10:
            value = "Yes!"
        else:
            value = "No!"
        result = some_function()
        return value + ":" + result
    return wrapper

@my_decorator3
def just_some_function3():
    return "Wheee!"
just_some_function3(10)

# 4. Decorator 4
# syntactic sugar
def outside_decorator(expr):
    def my_decorator4(some_function):
        def wrapper(num):
            if num == 10:
                value = "Yes!"
            else:
                value = "No!"
            result = some_function()
            return expr + ":" + value + ":" + result 
        return wrapper
    return my_decorator4

@outside_decorator("Python decorators")
def just_some_function4():
    return "Wheee!"

class DecoratorTests(unittest.TestCase):

    def test_decorator1(self):
        foo = parent(10)
        bar = parent(11)
        self.assertEqual(foo(), "Printing from the first_child() function.")
        self.assertEqual(bar(), "Printing from the second_child() function.")

    def test_decorator2(self):
        def just_some_function():
            return "Wheee!"
            
        expected_string = "Wheee!"
        just_some_function = my_decorator2(just_some_function)
        self.assertEqual(just_some_function(), expected_string)
        
    def test_decorator3(self):
        def just_some_function():
            return "Wheee!"
            
        expected_string = "Yes!:" + "Wheee!"
        self.assertEqual(just_some_function3(10), expected_string)
    
    def test_decorator4(self):
        @outside_decorator("Python decorators")
        def just_some_function4():
            return "Wheee!"
            
        expected_string = "Python decorators:" \
                          "Yes!:" + "Wheee!"
        self.assertEqual(just_some_function4(10), expected_string)
        
if __name__ == '__main__':
    unittest.main()

