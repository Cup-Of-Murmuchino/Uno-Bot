class A(object):
    def __init__(self):
        self._field = 3

    def equal(self, value: int):
        if self._field == value:
            return True
        else:
            return False

b = A()
print(b.equal(value=3))