#include <iostream>
#include <vector>
#include <fstream>
using std::vector;
using std::ofstream;
using std::cout;
vector<void*> stack_trace(40);
vector<int> stack(40);
vector<int> top_pointer_stack(40);
int top_pointer = 0;
int stack_trace_pointer = -1;
int stack_pointer = -1;
inline void push(int x){
    stack[++stack_pointer] = x;
}
inline int pop(){
    return stack[stack_pointer--];
}
inline int get(int n){
    return stack[n];
}
inline void set(int n, int value){
    stack[n] = value;
}
inline int last(){
    return top_pointer_stack[top_pointer];
}
inline void top_pointer_push(int x){
    top_pointer_stack[++top_pointer] = x;
}
inline int top_pointer_pop(){
    return top_pointer_stack[top_pointer--];
}
ofstream myfile;
int main(){
stack_trace[++stack_trace_pointer]=&&$0;
top_pointer_stack[0] = 0;
myfile.open("build/log.txt"); // for debugging
goto main;
_sum:
push(pop() + pop());
goto *stack_trace[stack_trace_pointer--];
_mul:
push(pop() * pop());
goto *stack_trace[stack_trace_pointer--];
_eq:
push(pop() == pop());
goto *stack_trace[stack_trace_pointer--];
_mod:
stack[stack_pointer - 1] = stack[stack_pointer-1] % stack[stack_pointer];
stack_pointer--;
goto *stack_trace[stack_trace_pointer--];
_dif:
stack[stack_pointer - 1] = stack[stack_pointer-1]-stack[stack_pointer];
stack_pointer--;
goto *stack_trace[stack_trace_pointer--];
_div:
stack[stack_pointer - 1] = int(stack[stack_pointer-1]/stack[stack_pointer]);
stack_pointer--;
goto *stack_trace[stack_trace_pointer--];
_lt:
push(pop() > pop());
goto *stack_trace[stack_trace_pointer--];
_bt:
push(pop() < pop());
goto *stack_trace[stack_trace_pointer--];
_le:
push(pop() >= pop());
goto *stack_trace[stack_trace_pointer--];
_be:
push(pop() <= pop());
goto *stack_trace[stack_trace_pointer--];
_ne:
push(pop() == pop());
goto *stack_trace[stack_trace_pointer--];
_not:
push(!pop());
goto *stack_trace[stack_trace_pointer--];
_and:
push(pop() && pop());
goto *stack_trace[stack_trace_pointer--];
_or:
push(pop() || pop());
goto *stack_trace[stack_trace_pointer--];