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
sum:
push(pop() + pop());
goto *stack_trace[stack_trace_pointer--];
eq:
push(pop() == pop());
goto *stack_trace[stack_trace_pointer--];
mod:
stack[stack_pointer - 1] = stack[stack_pointer-1] % stack[stack_pointer];
stack_pointer--;
goto *stack_trace[stack_trace_pointer--];
dif:
stack[stack_pointer - 1] = stack[stack_pointer-1]-stack[stack_pointer];
stack_pointer--;
goto *stack_trace[stack_trace_pointer--];
lt:
push(pop() > pop());
goto *stack_trace[stack_trace_pointer--];
bt:
push(pop() < pop());
goto *stack_trace[stack_trace_pointer--];
cout:
cout << pop() << ", ";
goto *stack_trace[stack_trace_pointer--];