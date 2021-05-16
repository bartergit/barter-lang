from brand_new_ast import parse_program
from fancy_compiler import create_source
import argh
import os
import time
from util import print_tree


def build(filename, path, if_print_ast=True):
    build_path = os.path.join(path, 'build')
    with open(os.path.join(path, filename + ".barter"), "r") as listing:
        listing_text = listing.read()
    ast = parse_program(listing_text)
    if if_print_ast:
        print_tree(ast)
    res = create_source(ast)
    if not os.path.exists(build_path):
        os.makedirs(build_path)
    with open(f'{build_path}/{filename}.cpp', 'w') as f:
        f.write(res)


# g++ test/$1.cpp -o build/$1.exe -fsanitize=undefined  && ./build/$1.exe
def run(filename, build_path):
    if not os.name == 'nt':
        os.system(f'g++ {build_path}/{filename}.cpp -o {build_path}/{filename}')
        os.system(os.path.join(build_path,filename))
    else:
        os.system(f'g++ {build_path}/{filename}.cpp -o {build_path}/{filename}.exe')
        os.system(rf".\\{build_path}\\{filename}.exe")


def main(filename, output=False, timer=False, ast=False):
    path = os.path.dirname(filename)
    filename = os.path.basename(filename)
    build_path = os.path.join(path, 'build')
    if filename.endswith(".barter"):
        filename = filename[:-len(".barter")]
    if timer:
        start = time.time()
        build(filename, path, ast)
        print(f"Build time: {time.time() - start}")
        start = time.time()
        run(filename, build_path)
        print(f"Execution time: {time.time() - start}")
    else:
        build(filename, path, ast)
        run(filename, build_path)
    if not output:
        os.remove(f"{build_path}/{filename}.cpp")
        if os.name == 'nt':
            os.remove(f"{build_path}/{filename}.exe")
        else:
            os.remove(f"{build_path}/{filename}")
        # os.remove(f"{build_path}/log.txt")
        if len(os.listdir(build_path)) == 0:
            os.rmdir(build_path)


if __name__ == '__main__':
    argh.dispatch_command(main)
