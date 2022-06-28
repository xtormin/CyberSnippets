import sys
import argparse

# ARGUMENTS
parser = argparse.ArgumentParser(add_help = True, description = '%(prog)s hunts all forms and inputs found in a list of urls.')

parser.add_argument('-f','--files', 
                    help = 'Files to compare or merge', nargs=2)
parser.add_argument('-o','--option', 
                    help = '''
                        MODES:
                            > a : file1 - file2
                            > b : file2 - file1
                            > c : file1 + file2
                    ''',  nargs=1, default='b')                         

def get_list_from_file(filename):
    f = open(filename, 'r')
    data = f.read()
    data = data.split('\n')
    f.close()

    output = list(filter(None, data))
    return output

if __name__ == '__main__':
    args = parser.parse_args()

    option = args.option[0]

    first_file = args.files[0]
    second_file = args.files[1]
    first_list = get_list_from_file(first_file)
    second_list = get_list_from_file(second_file)

    # OPTIONS
    def a():
        for i in list(set(first_list) - set(second_list)): print(i)

    def b():
        for i in list(set(second_list) - set(first_list)): print(i)

    def c():
        for i in set(first_list + second_list): print(i)

    def error():
        print("\n|-| [ERROR] Choose an option...\n")
    
    switch_option = {
        'a': a,
        'b': b,
        'c': c,
    }

    switch_option.get(option, error)()
