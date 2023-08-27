import argparse
import socket
import dns.resolver
import datetime
import time

from random import randint

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'

def print_with_timestamp(message, color=None):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if color:
        print(f"{color}[{timestamp}] {message}{Colors.RESET}")
    else:
        print(f"[{timestamp}] {message}")

def check_domains(domain_list, dns_server=None):
    alive_domains = []
    dead_domains = []

    resolver = dns.resolver.Resolver()
    if dns_server:
        resolver.nameservers = [dns_server]

    for domain in domain_list:
        print_with_timestamp(f"Reading domain: {domain}")
        temp_waittime = randint(2, 7)
        print_with_timestamp(f"Waiting {temp_waittime}")
        time.sleep(temp_waittime)
        try:
            resolver.resolve(domain, 'A')  # Try to retrieve the A record of the domain
            alive_domains.append(domain)
            print_with_timestamp(f"Domain {domain} is alive.", Colors.GREEN)
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers):
            dead_domains.append(domain)
            print_with_timestamp(f"Domain {domain} is dead.", Colors.RED)

    return alive_domains, dead_domains

def main():
    parser = argparse.ArgumentParser(description="Check if domains are resolvable by a specified DNS server.")
    parser.add_argument("--input", required=True, help="Path to the input file containing domains.")
    parser.add_argument("--dns", default=None, help="IP address of the DNS server to use for checks.")
    parser.add_argument("--alive", required=True, help="Path to the output file for alive domains.")
    parser.add_argument("--dead", required=True, help="Path to the output file for dead domains.")
    args = parser.parse_args()

    print_with_timestamp("Reading domains from input file ...")
    with open(args.input, 'r') as f:
        domains = [line.strip() for line in f.readlines()]

    print_with_timestamp(f"Checking {len(domains)} domains ...")
    alive, dead = check_domains(domains, args.dns)

    print_with_timestamp(f"Saving alive domains to {args.alive} ...")
    with open(args.alive, 'w') as f:
        for domain in alive:
            f.write(domain + "\n")

    print_with_timestamp(f"Saving dead domains to {args.dead} ...")
    with open(args.dead, 'w') as f:
        for domain in dead:
            f.write(domain + "\n")

    # Printing statistics
    print_with_timestamp(f"Total domains checked: {len(domains)}")
    print_with_timestamp(f"Alive domains: {len(alive)}", Colors.GREEN)
    print_with_timestamp(f"Dead domains: {len(dead)}", Colors.RED)

    print_with_timestamp("Process completed.")

if __name__ == "__main__":
    main()
