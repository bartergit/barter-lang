# Manifest
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

