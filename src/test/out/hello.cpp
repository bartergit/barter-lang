#include <iostream>
#include <vector>
#include "to_import.h"
using std::vector;
using std::cout;

void f2(vector<void*> & stack_trace, vector<int> & stack, int & stack_trace_pointer, int & stack_pointer){
    stack_pointer++;
    stack[stack_pointer] = 19;
}
int main(){
    first:
    one:
    vector<void*> stack_trace(40);
    vector<int> stack(40);
    int stack_trace_pointer = -1;
    int stack_pointer = -1;
    f2(stack_trace, stack, stack_trace_pointer, stack_pointer);
    cout << stack[stack_pointer] << "!";
    stack_trace[++stack_trace_pointer] = &&first;
    cout << "here2";
    f(stack_trace, stack, stack_trace_pointer, stack_pointer);
    cout << "here";
    cout << stack[stack_pointer];
}