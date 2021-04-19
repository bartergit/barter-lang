# barter-lang
BarterLang is general-purpose programming language. It compiles to native C++ code, but it has nothing to do with a translator. Produced C++ code is very like virtual machine, which can do basic math operations and manipulate with a stack.
Program example:
```
dec_func('fib', 'int',
    block(
        set_arg('x', 'int')
    ),
    block(
        cond(lt(x,2), block(
            ret(1)
        )),
        ret(sum(fib(dif(x,1)),fib(dif(x,2))))
    )
);
dec_func('main', 'void',
    block(),
    block(
        cout(fib(8))
    )
);
```
