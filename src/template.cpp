#include <iostream>
#include <vector>
using std::vector;
using std::cout;
int R1 = 0;
vector<void*> stack_trace(40);
vector<long> stack(40);
int stack_trace_pointer = -1;
int stack_pointer = -1;
inline void push(int x){
    stack[++stack_pointer] = x;
}
inline int pop(){
    return stack[stack_pointer--];
}
inline int get(int n){
    return stack[R1 + n];
}
inline void set(int n, int value){
    stack[R1 + n] = value;
}
int main(){
goto main;
sum:
push(0);
push(0);
R1 = stack_pointer - 2 + 1;
push(get(0) + get(1));
set(0,get(2));
cout << get(2);
stack_pointer=R1;
goto *stack_trace[stack_trace_pointer--];

Euclidean_algorithm:
push(0);
push(0);
R1 = stack_pointer - 2 + 1;
while (get(1) != 0) {
if (get(0) > get(1)) {
set(0, get(0) - get(1));
} else {
set(1, get(1) - get(0));
}
}
set(0,get(0));
stack_pointer=R1;
goto *stack_trace[stack_trace_pointer--];

main:
R1 = stack_pointer - 0 + 1;
push(true);
push(13);
push(24);
stack_trace[++stack_trace_pointer] = &&$1;
goto sum;
$1:
push(pop());
// cout << stack[2] << " " << '\n';
}