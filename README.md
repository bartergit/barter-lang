# Manifest
BarterLang is general-purpose programming language. 
It compiles to native C++ code, but it has nothing to do with a translator.
Produced C++ code is very like virtual machine, which can do basic math operations 
and manipulate with a stack.\
Program example:
```
func fib(int x) int {
    if x < 2 {
        return 1
    }
    int arg = x - 1
    int fib1 = fib(arg)
    arg = arg - 1
    int fib2 = fib(arg)
    int res = fib1 + fib2
    return res
}
func main() void {
    int res = fib(5)
    print(res)
}
```

