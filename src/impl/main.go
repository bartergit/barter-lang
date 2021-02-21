package main

import (
	"github.com/goccy/go-yaml"
	"fmt"
	"io/ioutil"
)
// functions:
//   -
//     name: "main"
//     args: []
//     body:
//       -
//       call:
//         name: "fib"
//         args:
//           - 12
type call struct{
	name string
	args []int
}

type arg struct{
	name string
	typeof string
}

type function struct{
	name string
	args []int
	body []int
}

type T struct {
	functions function
}

func check(e error) {
	if e != nil {
			panic(e)
	}
}

func main() {
	fun := function{name:"some", args: []int{3,5}, body: []int{3,9}}
	fmt.Println(fun)
	bytes, err := yaml.Marshal(fun)
	check(err)
	fmt.Println(string(bytes))
	ioutil.ReadFile("test.yaml")
	// check(err)
	// if err := yaml.Unmarshal([]byte(data), &t); err != nil {
	// 	check(err)
	// } else{
	// 	fmt.Printf("%+v\n", t)
	// }
}