print("hee")


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


def fib1(n):
    result = 0
    for i in range(1,n+1):
        if i == 1:
            result

    return result
print(fib(5))
