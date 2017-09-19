class Test:
    amount = 10

    def __init__(self, value):
        self.value = value

t1 = Test(100)
t2 = Test(200)
Test.amount = 20
print(t1.value, t1.amount)
print(t2.value, t2.amount)