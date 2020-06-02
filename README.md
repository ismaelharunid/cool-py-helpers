# cool_py_helpers
A collection of common support functions, things and examples.


## proxy.py

    from proxy import proxy

    d = {'a': 1, 'b': 2, 'c': 3}
    p = proxy(d)
    print(d['a'], p['a'])
    p['a'] = 10
    print(d['a'], p['a'])
    d['a'] = 100
    print(d['a'], p['a'])


prints

    1  1
    10  10
    100 100


## unique.py

    from unique import uniques, uniquem

    print(uniques((1,2,3,4,5,4,3,2,1)))
    print(uniquem({'a': 1, 'b': 2, 'c': 3}, {'b': 4}))

prints

        (1, 2, 3, 4, 5)
        {'a': 1, 'b': 2, 'c': 3}


## installation?

The usual download or clone.  Just make sure it's in your PATH.

## documentation?

it's in the code.

