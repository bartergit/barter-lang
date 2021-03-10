#include <iostream>
#include <vector>
#include <fstream>
using std::vector;
using std::ofstream;
using std::cout;
// int R1 = 0;
vector<void*> stack_trace(40);
vector<int> stack(40);
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
ofstream myfile;
int main(){
stack_trace[++stack_trace_pointer]=&&$0;
myfile.open("build/log.txt");
goto main;
