# barter-lang
## Iteration 2
Some example
```
func return_5()->int{
    return 5
}
func do_nothing()->void{
    print('did nothing')
}
func return_self(int a) -> int {
    return a
}
func plus_one(int a) -> int {
    return add(a,1)
}
func main()->void{
    str str1 = 'something' //only single-quoted supported!
    log(str1)
    int a = return_self(19)
    log(to_str(div(15,10)))
    log(to_str(sub(19, mult(2, div(15, 10)))))
    //do_nothing()
    bool b = true
    bool b2 = false
    if or(false, true) {
        int i2 = 35
        log('hello world')
    }
    int three = 3
    int eight = add(three, 5)
    int five = return_5()
    int six = plus_one(five)
}
```
Variables declaration is supported (int, str and bool). 4 basic operations for int expressions are supported: +, -, /, *  
The program is compiled to yaml format and then executed. 
The expressions are not supported yet (only built-in functions, you can see them in built-in.yaml).\
Overload is not supported yet.\
Recursion demonstration:
```
func factorial(int n) -> int {
  if eq(n, 0) {
    return 1
  }
  if not(eq(n,0)) {
    return mult(n,factorial(sub(n,1)))
  }
}
func fib(int n) -> int {
    if eq(n, 0){
        return 0 // базовый случай (условие завершения)
    }
    if eq(n, 1) {
        return 1 // базовый случай (условие завершения)
    }
    return add(fib(sub(n,1)),fib(sub(n,2)))
}
func main() -> void {
    log(to_str(factorial(5)))
    log(to_str(fib(12))) // perfomance is pretty slow for now, for fib(30) for example
}
```