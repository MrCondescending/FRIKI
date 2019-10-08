#!/usr/bin/python
# http://stackoverflow.com/questions/2708178/python-using-doctests-for-classes

class Test:
    def __init__(self, number):
        self._number=number

    def multiply_by_2(self):
        """
        >>> t.multiply_by_2()
        4
        """
        return self._number*2

if __name__ == "__main__":
    import doctest
    doctest.testmod(extraglobs={'t': Test(2)})