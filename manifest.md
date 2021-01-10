# Manifest
```
create_from_type = {type:func}
for line in program:
    type = define_type(preprocess(line))
    if type not in expected:
        sad()
    create_from_type[type]
    
```

```
dec return_5() -> int {
    return 5
}

return_six => (int a, int b) {
    return return_5() + 1
}

add => (a, b){
    return a + b;
}
//entry point is main function
func main(){
    str s1 = "string" // this a comment
    str s2 = "string  variable"
    bool b1 = true
    bool b2 = b1 and b1 or false
    int i1 = 35
    int i2 = 35 + 29 * i1
    int i3 = 35 + i2 * i1 - ( 15 + i1) *2
    int i4 = (35 + (return_5())*0 * i1 - ( 15 + i1) *2)
}
```


