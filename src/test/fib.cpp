#include <iostream>
int fib(int x){
    return x < 2 ? 1 : fib(x - 1) + fib(x-2);
}
int main(){
//    int array[] = {3,5};
//    std::cout << array[2];
//    int a = 2147483647;
//    a += 1;
//    std::cout << a;
    std::cout << fib(44);
}