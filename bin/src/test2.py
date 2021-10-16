"""
a bunch of pairwise distinct integer numbers a[0], a[1], ..., a[n - 1] placed on a circle in the same order.
There are n pairs of neighboring numbers: (a[0], a[1]), (a[1], a[2]), ..., (a[n - 2], a[n - 1]), (a[n - 1], a[0]).
You tried to encode the circle of numbers by recording the pairs, but unfortunately the numbers in these pairs got shuffled,
so now each pair (x, y) could be represented either as (x, y) or (y, x).

You are given an array pairs of these shuffled pairs,
your task is to return the initial state of the numbers on the circle.
Please, note that any cyclic rotation of the initial state is also considered to be a correct answer, and either direction is acceptable. Return any of the multiple possible answers.
Example
For pairs = [[3, 5], [1, 4], [2, 4], [1, 5], [2, 3]], the output can be restoreNumbersOnCircle(pairs) = [3, 5, 1, 4, 2].
3,5,  1,4,2


"""
def restoreNumbersOnCircle(pairs):
    result = list()
    firstArr = pairs[0]
    x = firstArr[0] #3
    y = firstArr[1] #5
    result.append(x)
    result.append(y)
    for arr in pairs:
        # arr =  [2, 3]         =====>>> // x[1, 4] | [2, 4]
        if y in arr or x in arr:
            if x != arr[0] and y == [1]:
                result.append(arr[0])
            if y != arr[0] and x == [1]:
                result.append(arr[1])
    print(result)
        # result = [3, 5, 1]
pairs = [[3, 5], [1, 4], [2, 4], [1, 5], [2, 3]]
restoreNumbersOnCircle(pairs)