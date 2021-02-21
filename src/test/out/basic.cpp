
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
inc:
push(stack[stack_pointer - 0]);
R1 = stack_pointer - 1 + 1;
push(get(0) + 1);
set(0, get(1));
goto *stack_trace[stack_trace_pointer--];
is_positive:
push(stack[stack_pointer - 0]);
R1 = stack_pointer - 1 + 1;
if (get(0) < 0){
set(0, 0);
goto *stack_trace[stack_trace_pointer--];
}
set(0, 1);
goto *stack_trace[stack_trace_pointer--];
main:
R1 = stack_pointer - 0 + 1;
stack_trace[++stack_trace_pointer] = &&$0;
push(5);
goto inc;
$0:
push(pop());
cout << get(0) << " " << '\n';
}
