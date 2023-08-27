# DNS Domain Checker

A simple tool to check if domains can be resolved by a specified DNS server.

## Requirements

- Python 3.x
- Conda (Anaconda or Miniconda)

## Installation and Setup

1. **Clone the Repository**

   Clone the repository to your local system:
   
   ```
   git clone https://github.com/YourGithubUsername/DNSDomainChecker.git
   cd DNSDomainChecker
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

   Now, you can run the script:

   ```
   python main.py --input input.txt --alive alive.txt --dead dead.txt --dns 8.8.8.8
   ```


## Support

For issues or queries, please contact me here.
