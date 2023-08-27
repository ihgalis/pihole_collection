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

   Now, you can run the script. It will choose a random DNS Server:

   ```
   python main.py --input input.txt --alive alive.txt --dead dead.txt
   ```

   If you like to use just one DNS Server add this argument:

   ```
    --dns <IP>
   ````


## Support

For issues or queries, please contact me here.
