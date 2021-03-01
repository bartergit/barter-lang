#include <iostream>
#include <vector>
#include "to_import.h"
using std::vector;
using std::cout;
void f(vector<void*> & stack_trace, vector<int> & stack, int & stack_trace_pointer, int & stack_pointer){
    cout << "calling f";
    // goto *stack_trace[stack_trace_pointer];
    one:
    cout <<"hello";
    first:
    cout << stack[stack_pointer] << " ";
    stack_pointer++;
    stack[stack_pointer] = 15;  
}
// int main(){
//     vector<void*> stack_trace(40);
//     vector<int> stack(40);
//     int stack_trace_pointer = -1;
//     int stack_pointer = -1;
//     f(stack_trace, stack, stack_trace_pointer, stack_pointer);
//     cout << stack[stack_pointer];
// }