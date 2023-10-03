import argparse
import socket
import dns.resolver
import datetime
import time
import re
import os
import logging
import ipaddress
import socket

from random import randint, choice

# Set a global default timeout for all future socket objects (in seconds)
socket.setdefaulttimeout(10)

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s: %(message)s',
                    handlers=[logging.FileHandler("app.log"),
                              logging.StreamHandler()])

def sanitize_log_message(message):
    # regular expression to strip ANSI escape sequences from a string
    return re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', message)

def escape_meta_chars(message):
    return message.replace("\n", "\\n").replace("\r", "\\r")

def limit_log_length(message, max_length=1000):
    return message[:max_length]

def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def print_with_timestamp(message, level='info'):
    sanitized_message = sanitize_log_message(message)
    escaped_message = escape_meta_chars(sanitized_message)
    limited_message = limit_log_length(escaped_message)

    log_method = getattr(logging, level, logging.info)
    log_method(message)

def is_valid_domain(domain):
    pattern = r'^(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z]{2,}$'
    return re.fullmatch(pattern, domain, re.IGNORECASE) is not None

def confirm_overwrite(filepath):
    if os.path.exists(filepath):
        answer = input(f"The file {filepath} already exists. Do you want to overwrite it? (y/n): ")
        if answer.lower() != 'y':
            print_with_timestamp("Operation cancelled.", 'error')
            exit(1)

def check_domains(args, domain_list, dns_server=None):
    """
    Check the resolvability of a list of domains using DNS.
    
    Parameters:
        args: argparse.Namespace - Parsed command-line arguments.
        domain_list: list - List of domain names to check.
        dns_server: str, optional - Specific DNS server to use for resolution.
        
    Returns:
        tuple: Lists of alive and dead domains.
    """

    total_domains = len(domain_list)
    checked_domains = 0

    alive_domains = []
    dead_domains = []

    # List of known public DNS servers
    public_dns_servers = [
        '8.8.8.8',          # Google DNS
        '8.8.4.4',          # Google DNS
        '1.1.1.1',          # Cloudflare DNS
        '1.0.0.1',          # Cloudflare DNS
        '64.6.64.6'         # Verisign
    ]

    resolver = dns.resolver.Resolver()
    resolver.timeout = 10
    resolver.lifetime = 10

    for domain in domain_list:
        print_with_timestamp(f"Reading domain: {domain}", 'info')
        
        if not is_valid_domain(domain):
            print_with_timestamp(f"Invalid domain: {domain}. Skipping...", 'error')
            continue
        
        if args.wait_level:
            if args.wait_level == 1:
                temp_waittime = randint(2, 4)
            elif args.wait_level == 2:
                temp_waittime = randint(4, 6)
            elif args.wait_level == 3:
                temp_waittime = randint(6, 10)
            else:
                temp_waittime = 1
            print_with_timestamp(f"Waiting {temp_waittime} seconds", 'info')
            time.sleep(temp_waittime)
        
        # Choose a random DNS server from the list if none is provided
        if not dns_server:
            dns_server = choice(public_dns_servers)

            # Check if DNS Server is valid IP
            if not is_valid_ip(dns_server):
                print_with_timestamp(f"Invalid DNS server IP: {dns_server}", 'error')
                return [], []
            else:
                print_with_timestamp(f"Using DNS server: {dns_server}", 'info')
            
        resolver.nameservers = [dns_server]

        try:
            resolver.resolve(domain, 'A')  # Try to retrieve the A record of the domain
            alive_domains.append(domain)
            print_with_timestamp(f"Domain {domain} is alive.", 'info')
        except (dns.exception.Timeout, socket.timeout):
            print_with_timestamp(f"Timeout while querying domain {domain}.", 'error')
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers):
            dead_domains.append(domain)
            print_with_timestamp(f"Domain {domain} is dead.", 'info')
        except dns.name.EmptyLabel:
            print_with_timestamp(f"Invalid domain: {domain}. Contains empty label.", 'error')

        checked_domains += 1
        print_with_timestamp(f"Checked {checked_domains} of {total_domains} domains ({(checked_domains / total_domains) * 100:.2f}% complete).", 'info')
        dns_server = None

    return alive_domains, dead_domains

def main():
    parser = argparse.ArgumentParser(description="Check if domains are resolvable by a specified DNS server.")
    parser.add_argument("--input", required=True, help="Path to the input file containing domains.")
    parser.add_argument("--dns", default=None, help="IP address of the DNS server to use for checks. If not provided, a random public DNS server will be chosen.")
    parser.add_argument("--alive", required=True, help="Path to the output file for alive domains.")
    parser.add_argument("--dead", required=True, help="Path to the output file for dead domains.")
    parser.add_argument("-w", "--wait-level", type=int, choices=[1, 2, 3], default=None, help="Level of randomness for waiting time between DNS queries.")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print_with_timestamp(f"Input file {args.input} does not exist. Exiting.", 'error')
        return

    try:
        print_with_timestamp("Reading domains from input file ...", 'info')
        with open(args.input, 'r') as f:
            domains = [line.strip() for line in f.readlines()]

    except FileNotFoundError:
        print_with_timestamp(f"File {args.input} not found. Exiting...", 'error')
        return
    except PermissionError:
        print_with_timestamp(f"Permission denied when reading {args.input}. Exiting...", 'error')
        return
    except Exception as e:
        print_with_timestamp(f"An error occurred while reading {args.input}: {e}. Exiting...", 'error')
        return

    print_with_timestamp(f"Checking {len(domains)} domains ...", 'info')
    alive, dead = check_domains(args, domains, args.dns)

    try:
        print_with_timestamp(f"Saving alive domains to {args.alive} ...", 'info')
        confirm_overwrite(args.alive)
        with open(args.alive, 'w') as f:
            for domain in alive:
                f.write(domain + "\n")
                
    except PermissionError:
        print_with_timestamp(f"Permission denied when writing to {args.alive}. Exiting...", 'error')
        return
    except Exception as e:
        print_with_timestamp(f"An error occurred while writing to {args.alive}: {e}. Exiting...", 'error')
        return

    try:
        print_with_timestamp(f"Saving dead domains to {args.dead} ...", 'info')
        confirm_overwrite(args.dead)
        with open(args.dead, 'w') as f:
            for domain in dead:
                f.write(domain + "\n")
    except PermissionError:
        print_with_timestamp(f"Permission denied when writing to {args.dead}. Exiting...", 'error')
        return
    except Exception as e:
        print_with_timestamp(f"An error occurred while writing to {args.dead}: {e}. Exiting...", 'error')
        return

    # Printing statistics
    print_with_timestamp(f"Total domains checked: {len(domains)}", 'info')
    print_with_timestamp(f"Alive domains: {len(alive)}", 'info')
    print_with_timestamp(f"Dead domains: {len(dead)}", 'info')

    print_with_timestamp("Process completed.", 'info')

if __name__ == "__main__":
    main()
