# decorator is a pattern to 
#   1. get a function 
#   2. returns wrapper (inner function) that wraps the inner function.

def my_decorator(some_function):
    def wrapper(x):
        print("Something is happening before some_function() is called.")
        some_function(x)
        print("Something is happening after some_function() is called.")

    return wrapper

def just_some_function(x):
    print("Wheee!" + str(x))

just_some_function(10)
    
just_some_function = my_decorator(just_some_function)
just_some_function(10)