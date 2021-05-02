# from argcomplete.completers import EnvironCompleter
# from argh import arg
from brand_new_ast import parse_program
from fancy_compiler import create_source
import argh
import os
import time


def build(filename):
    with open(f"test/{filename}.barter", "r") as listing:
        listing_text = listing.read()
    ast = parse_program(listing_text)
    res = create_source(ast)
    with open(f'build/{filename}.cpp', 'w') as f:
        f.write(res)


# g++ test/$1.cpp -o build/$1.exe -fsanitize=undefined  && ./build/$1.exe
def run(filename):
    os.system(f'g++ build/{filename}.cpp -o build/{filename}.exe')
    os.system(rf".\\build\\{filename}.exe")


def main(filename, output=True, timer=True):
    if timer:
        start = time.time()
        build(filename)
        print(f"Build time: {time.time() - start}")
        start = time.time()
        run(filename)
        print(f"Execution time: {time.time() - start}")


if __name__ == '__main__':
    argh.dispatch_command(main)
