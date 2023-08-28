# DNS Domain Checker

A simple tool to check if domains can be resolved by a specified DNS server.

## Requirements

- Python 3.x
- Conda (Anaconda or Miniconda)

## Installation and Setup

1. **Clone the Repository**

   Clone the repository to your local system:
   
   ```
   git clone https://github.com/ihgalis/pihole_collection.git
   cd pihole_collection/dns_checker
   ```

2. **Create Conda Environment**

   Create a new virtual Conda environment:
   
   ```
   conda create --name dnschecker python=3.8
   ```

   Activate the Conda environment:

   ```
   conda activate dnschecker
   ```

3. **Install Dependencies**

   Install the required packages from the `requirements.txt` file:

   ```
   pip install -r requirements.txt
   ```

4. **Run the Script**

4.1. ***Default settings***

   Now, you can run the script. In the following example the arguments do this:

   * `--input` the list domains to be checked
   * `--alive` the output list with all alive hosts
   * `--dead` the list with all dead - not resolvable - hosts
   * `--dns` usage of one specific DNS server to resolve all hosts

   ```
   python main.py --input input.txt --alive alive.txt --dead dead.txt --dns 8.8.8.8
   ```

4.2. ***Advanced usage***

   You can do even more which might help you get better results, like choose random DNS resolving hosts for each DNS request, or add some random waiting time in order to not get blocked:

   ```
   # Waits 1 second between every DNS request, chooses random DNS Servers
   python main.py --input input.txt --alive alive.txt --dead dead.txt

   # Waits 2-4 seconds between DNS requests (randomly choosen)
   python main.py --input input.txt --alive alive.txt --dead dead.txt -w 1

   # Waits 4-6 seconds between DNS requests (randomly choosen)
   python main.py --input input.txt --alive alive.txt --dead dead.txt -w 2

   # Waits 6-10 seconds between DNS requests (randomly choosen)
   python main.py --input input.txt --alive alive.txt --dead dead.txt -w 3
   ```

## Support

For issues or queries, please contact me here.
