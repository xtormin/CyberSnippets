import argparse
import re
from xml.dom.pulldom import parseString
import requests

# ARGUMENTS
parser = argparse.ArgumentParser(add_help = True, description = '%(prog)s hunts all forms and inputs found in a list of urls.')

parser.add_argument('-w','--wordlistslist', 
                    help = 'List of wordlists to merge', nargs="+")
parser.add_argument('-u','--urlwordlistslist', 
                    help = 'List of wordlists to merge', nargs="+")
parser.add_argument('-m','--mode', 
                    help = '''
                    MODE:
                        > a: Merge 'wordlistslist'
                        > b: Merge 'urlwordlistslist'
                        > c: Merge 'wordlistslist' and 'urlwordlistslist' wordlists
                        > d: Diff between second list with firts list (wordlistslist[1] - wordlistslist[0])
                    ''',  nargs=1, default='a') 
parser.add_argument('-o','--output', 
                    help = 'Outputfile',  nargs=1) 

# GENERAL FUNCTIONS

def read_from_file(filename):
    f = open(filename, 'r')
    data = f.read()
    data = data.split('\n')
    f.close()
    return list(filter(None, data))

def write_to_file(filename, data):
    with open(filename, 'w') as output:
        for row in data:
            output.write(str(row) + '\n')

def read_from_url(url):
    output = []
    info = requests.get(url).text
    return info.split('\n')

# SCRIPT FUNCTIONS

def merge_wordlists(wordlists_list):
    output = []
    # Merge all wordlists
    for i in wordlists_list:
        output = output + read_from_file(i)
    
    output = list(filter(None, output))
    output = set(output)
    return output

def merge_urlwordlistslist(urlwordlists_list):
    output = []

    # Download and merge a list of wordlists by url
    for i in read_from_file(urlwordlists_list):
        output = output + read_from_url(i)

    output = list(filter(None, output))
    output = set(output)
    return output


if __name__=="__main__":

    args = parser.parse_args()

    mode = args.mode[0]
    filename_output = args.output[0]
    if args.wordlistslist: wordlists_list = args.wordlistslist
    if args.urlwordlistslist: urlwordlists_list = args.urlwordlistslist[0]

    # OPTIONS
    def a():
        # Merge 'wordlistslist'
        output = merge_wordlists(wordlists_list)
        print(f"|+| Word count: {len(output)}")
        write_to_file(filename_output, output)

    def b():
        # Merge 'urlwordlistslist'
        output = merge_urlwordlistslist(urlwordlists_list)
        print(f"|+| Word count: {len(output)}")
        write_to_file(filename_output, output)

    def c():
        # Merge 'wordlistslist' and 'urlwordlistslist' wordlists
        output = list(merge_urlwordlistslist(urlwordlists_list)) + list(merge_wordlists(wordlists_list))
        output = set(output)
        print(f"|+| Word count: {len(output)}")
        write_to_file(filename_output, output)

    def d():
        # Diff between second list with firts list (wordlistslist[1] - wordlistslist[0])
        output = set(read_from_file(wordlists_list[1])) - set(read_from_file(wordlists_list[0]))
        print(f"|+| Word count: {len(output)}")
        write_to_file(filename_output, output)

    def error():
        print("\n|-| [ERROR] Choose an option...\n")
    
    switch_mode = {
        'a': a,
        'b': b,
        'c': c,
        'd': d
    }

    switch_mode.get(mode, error)()