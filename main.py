def handler(func):
    def foo(x):
        foo.calls += 1
        print(foo.calls)
        if foo.calls % 2 == 0:
            print("cannot call")
        else:
            func(x)

    foo.calls = 0
    return foo

@handler
def tester(n):
    print(n)

for j in range(10):
    tester(j)