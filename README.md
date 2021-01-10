# barter-lang
## Iteration 1
Minimal valid program
```
func do_nothing ( int a , int b ) void 
{
}
func main ( ) void 
{
   int i = 6
   int a = - ( i + 3 ) * 2 + ( 15 - ( 9 ) * 0 )
   str str_val = 'value'
   bool flag = true 
}
```
Variables declaration is supported (int, str and bool). 4 basic operations for int expressions are supported: +, -, /, * 
There is no actual preprocessor for now, so all those spaces are required.  
Function declaration is supported, function call is not.
The program is compiled to yaml format and then executed. 
