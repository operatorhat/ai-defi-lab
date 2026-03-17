import os
from dotenv import load_dotenv
from web3 import Web3

# 1) Load env
load_dotenv()

RPC_URL = os.getenv("ARBITRUM_RPC_URL")
ADDRESS = os.getenv("TEST_WALLET_ADDRESS")

if not RPC_URL:
    raise ValueError("ARBITRUM_RPC_URL not set")
if not ADDRESS:
    raise ValueError("TEST_WALLET_ADDRESS not set")

w3 = Web3(Web3.HTTPProvider(RPC_URL))

if not w3.is_connected():
    raise ConnectionError("Web3 is not connected")

print("Connected to Arbitrum at block:", w3.eth.block_number)
print("Wallet:", ADDRESS)

# 2) Native ETH balance
eth_balance_wei = w3.eth.get_balance(ADDRESS)
eth_balance = w3.from_wei(eth_balance_wei, "ether")
print(f"ETH balance: {eth_balance} ETH")

# 3) Minimal ERC20 ABI
ERC20_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function",
    },
]

# 4) Known token contracts on Arbitrum (fill in with real addresses)
TOKENS = {
    "WETH": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",  # put real WETH contract address here
    "USDC": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",  # real USDC
    "ARB":  "0x912CE59144191C1204E64559FE8253a0e49E6548",  # real ARB token
}

for symbol, token_address in TOKENS.items():
    if token_address == "0x...":
        # skip placeholders until you put real addresses in
        continue

    token = w3.eth.contract(address=Web3.to_checksum_address(token_address), abi=ERC20_ABI)

    try:
        decimals = token.functions.decimals().call()
        raw_balance = token.functions.balanceOf(ADDRESS).call()
        human = raw_balance / (10 ** decimals)
        print(f"{symbol} balance: {human} {symbol}")
    except Exception as e:
        print(f"Error reading {symbol} at {token_address}: {e}")
