# syntactic sugar

def my_decorator(some_function):
    def wrapper(num):
        if num == 10:
            print("Yes!")
        else:
            print("No!")
        some_function()
        print("Something is happening after some_function() is called.")
    return wrapper

@my_decorator
def just_some_function():
    print("Wheee!")

just_some_function(10)
just_some_function(1)