#!/usr/bin/python3

import argparse
import tldextract
import pandas as pd 
from urllib.parse import urlparse

from pyspark import F

class Url():
    kind = 'url'

    def __init__(self, protocol=None, subdomain=None, domain=None, tld=None, path=None, params=None):
        self.protocol = protocol
        self.subdomain = subdomain
        self.domain = domain
        self.tld = tld
        self.path = path
        self.params = params

    def get_top_domain(self):
        return f"{self.domain}.{self.tld}"
    
    def get_subdomain(self):
        if self.subdomain:
            return f"{self.subdomain}.{self.domain}.{self.tld}"
        return None


# ARGUMENTS
parser = argparse.ArgumentParser(add_help = True, description = '%(prog)s hunts all forms and inputs found in a list of urls.')

parser.add_argument('-f','--file', 
                    help = 'Files to compare or merge', nargs='+')

def read_file(filename):
    f = open(filename, 'r')
    data = f.read()
    data = data.split('\n')
    f.close()

    output = list(filter(None, data))
    return output

if __name__=="__main__":
    args = parser.parse_args()
    data = read_file(args.file[0])

    tld_df = pd.read_csv('../wordlists/Enumeration/Subdomains/top_249_tld_domains.txt', sep='\t')

    tld_data_list = tld_df['TLD'].tolist()
    
    for url in data:
        url_info = urlparse(url)
        tld_info = tldextract.extract(url_info.netloc)
        
        print(url_info)
        url_data = Url(protocol=url_info.scheme, subdomain=tld_info.subdomain, domain=tld_info.domain, tld=tld_info.suffix, path=url_info.path, params=url_info.params)
        print(url_data.get_top_domain())
        print(url_data.get_subdomain())

        print(tld_info)
    