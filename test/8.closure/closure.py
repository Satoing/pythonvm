def func1():
    a=1
    def func2():
        print a
    a = a+1
    return func2

f = func1()
f()