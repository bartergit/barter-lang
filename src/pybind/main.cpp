#include "pybind11/embed.h" // everything needed for embedding
#include <iostream>
namespace py = pybind11;

int main() {
    py::scoped_interpreter guard{}; // start the interpreter and keep it alive
    // py::print("Hello, World!"); // use the Python API
    // py::module_ sys = py::module_::import("sys");
    py::exec(R"(
        def fib(x):
            return 1 if x < 2 else fib(x-1) + fib(x-2)
        print(fib(35))
        #import random_word
        #print(random_word.RandomWords().get_random_word())
        #kwargs = dict(name="World", number=42)
        #message = "Hello, {name}! The answer is {number}".format(**kwargs)
        #print(message)
    )");
    std::cout << "now we are back";
    // py::module_ random_word = py::module_::import("random_word");
    // py::print(random_word.RandomWords);
}