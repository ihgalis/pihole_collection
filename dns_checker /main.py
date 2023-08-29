import argparse
import socket
import dns.resolver
import datetime
import time

from random import randint, choice

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

def check_domains(args, domain_list, dns_server=None):
    alive_domains = []
    dead_domains = []

    # List of known public DNS servers
    public_dns_servers = [
        '8.8.8.8',          # Google DNS
        '8.8.4.4',          # Google DNS
        '1.1.1.1',          # Cloudflare DNS
        '1.0.0.1',          # Cloudflare DNS
        '208.67.222.222',   # OpenDNS
        '208.67.220.220',   # OpenDNS
        '9.9.9.9',          # Quad9
        '149.112.112.112',  # Quad9
        '64.6.64.6',        # Verisign
        '76.76.2.0',        # Control D
        '76.76.10.0',       # Control D
        '94.140.14.14',     # AdGuard DNS
        '94.140.15.15',     # AdGuard DNS
        '8.26.56.26',       # Comodo Secure DNS
        '8.20.247.20'       # Comodo Secure DNS
    ]

    resolver = dns.resolver.Resolver()
    resolver.timeout = 10
    resolver.lifetime = 10

    for domain in domain_list:
        print_with_timestamp(f"Reading domain: {domain}")
        
        if ".." in domain:
            print_with_timestamp(f"Invalid domain: {domain}. Skipping...", Colors.RED)
            continue
        
        if args.wait_level:
            if args.wait_level == 1:
                temp_waittime = randint(2, 4)
            elif args.wait_level == 2:
                temp_waittime = randint(4, 6)
            elif args.wait_level == 3:
                temp_waittime = randint(6, 10)
            print_with_timestamp(f"Waiting {temp_waittime} seconds")
            time.sleep(temp_waittime)
        
        # Choose a random DNS server from the list if none is provided
        if not dns_server:
            dns_server = choice(public_dns_servers)
            print_with_timestamp(f"Using DNS server: {dns_server}")
            
        resolver.nameservers = [dns_server]
        try:
            resolver.resolve(domain, 'A')  # Try to retrieve the A record of the domain
            alive_domains.append(domain)
            print_with_timestamp(f"Domain {domain} is alive.", Colors.GREEN)
        except dns.exception.Timeout:
            print_with_timestamp(f"Timeout while querying domain {domain}.", Colors.RED)
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers):
            dead_domains.append(domain)
            print_with_timestamp(f"Domain {domain} is dead.", Colors.RED)
        except dns.name.EmptyLabel:
            print_with_timestamp(f"Invalid domain: {domain}. Contains empty label.", Colors.RED)

    return alive_domains, dead_domains

def main():
    parser = argparse.ArgumentParser(description="Check if domains are resolvable by a specified DNS server.")
    parser.add_argument("--input", required=True, help="Path to the input file containing domains.")
    parser.add_argument("--dns", default=None, help="IP address of the DNS server to use for checks. If not provided, a random public DNS server will be chosen.")
    parser.add_argument("--alive", required=True, help="Path to the output file for alive domains.")
    parser.add_argument("--dead", required=True, help="Path to the output file for dead domains.")
    parser.add_argument("-w", "--wait-level", type=int, choices=[1, 2, 3], default=None, help="Level of randomness for waiting time between DNS queries.")
    args = parser.parse_args()

    print_with_timestamp("Reading domains from input file ...")
    with open(args.input, 'r') as f:
        domains = [line.strip() for line in f.readlines()]

    print_with_timestamp(f"Checking {len(domains)} domains ...")
    alive, dead = check_domains(args, domains, args.dns)

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
