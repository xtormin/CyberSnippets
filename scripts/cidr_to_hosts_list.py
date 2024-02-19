import sys
import argparse
import ipaddress

parser = argparse.ArgumentParser(
    add_help=True,
    description='%(prog)s reads a list of network ranges from a file, calculates the list of hosts within each network range, and writes the resulting list of hosts for each network range to an output file.')

parser.add_argument('-f', '--file',
                    help='List of network with CIDR.',
                    nargs='?',
                    type=str)

parser.add_argument('-o', '--output',
                    help='List of hosts from network list.',
                    nargs='?',
                    type=str)



def get_hosts_from_network(network_range):
    network = ipaddress.ip_network(network_range)
    hosts = [str(ip) for ip in network.hosts()]
    return "\n".join(hosts)

if __name__ == "__main__":
    # Get arguments
    args = parser.parse_args()

    # Declare variables
    input_file_name = args.file
    output_file_name = args.output

    # Read input file, get hosts and write that in an output file
    with open(input_file_name, "r") as input_file, open(output_file_name, "w") as output_file:
        networks = input_file.readlines()
        for i, network in enumerate(networks):
            network = network.strip()  # Remove whitespace and line breaks
            hosts_list = get_hosts_from_network(network)
            if i > 0:  # Add newline before the list of hosts from the second network
                output_file.write("\n")
            # Write
            output_file.write(hosts_list)
