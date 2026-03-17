from dotenv import load_dotenv, find_dotenv
from web3 import Web3

import os

dotenv_path = find_dotenv()
print("dotenv_path:", dotenv_path)
loaded = load_dotenv(dotenv_path)
print(f".env loaded: {loaded}")
 

# Get the RPC URL from environment variables
rpc_url = os.getenv("ARBITRUM_RPC_URL")

if not rpc_url:
    raise ValueError("ARBITRUM_RPC_URL is not set in the environment variables.")

print("Attempting to connect to RPC endpoint:", rpc_url)

# Create Web3 HTTP provider and client (only once, after validation)
w3 = Web3(Web3.HTTPProvider(rpc_url))

TEST_WALLET_ADDRESS = os.getenv("TEST_WALLET_ADDRESS")

# Check if the connection is successful
if not w3.is_connected():
    raise ConnectionError("Failed to connect to the Arbitrum network.")

# Get the current block number
latest_block_number = w3.eth.block_number

print(f"Current block number on Arbitrum: {latest_block_number}")
print(f"Test wallet address: {TEST_WALLET_ADDRESS}")
