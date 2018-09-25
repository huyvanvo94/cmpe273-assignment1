def call_counter(func):
    def helper(x):
        helper.calls += 1
        return func(x)

    helper.calls = 0

    return helper


@call_counter
def succ(x):
    return x + 1


print(succ.calls)
for i in range(10):
    succ(i)

print(succ.calls)


@call_counter
def mul1(x, y=1):
    return x * y + 1

print( succ(10).helper.calls)
class Foo:
    def __init__(self): pass

    @call_counter
    def succ(self, x):
        return x + 1

