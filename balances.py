import os
from dotenv import load_dotenv
from web3 import Web3
import json
from datetime import datetime
from pathlib import Path

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

# 4) Load token config from config/tokens.json
CONFIG_PATH = Path(__file__).parent / "config" / "tokens.json"

with CONFIG_PATH.open() as f:
    TOKENS = json.load(f)


# 5) Query ERC20 balances and build snapshot data
balances = []

for token_cfg in TOKENS:
    symbol = token_cfg["symbol"]
    token_address = token_cfg["address"]
    decimals = token_cfg["decimals"]
    risk_tier = token_cfg.get("risk_tier", "unknown")

    token = w3.eth.contract(
        address=Web3.to_checksum_address(token_address),
        abi=ERC20_ABI,
    )

    try:
        raw_balance = token.functions.balanceOf(ADDRESS).call()
        human_balance = raw_balance / (10 ** decimals)
        print(f"{symbol} balance: {human_balance} {symbol}")

        balances.append(
            {
                "symbol": symbol,
                "address": token_address,
                "decimals": decimals,
                "risk_tier": risk_tier,
                "raw_balance": str(raw_balance),
                "human_balance": human_balance,
            }
        )
    except Exception as e:
        print(f"Error reading {symbol} at {token_address}: {e}")

# 6) Build snapshot payload
snapshot = {
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "block_number": w3.eth.block_number,
    "wallet_address": ADDRESS,
    "balances": balances,
}

# 7) Write snapshot file
SNAPSHOTS_DIR = Path(__file__).parent / "snapshots"
SNAPSHOTS_DIR.mkdir(exist_ok=True)

filename = f"snapshot_{snapshot['block_number']}.json"
output_path = SNAPSHOTS_DIR / filename

with output_path.open("w") as f:
    json.dump(snapshot, f, indent=2)

print(f"Snapshot written to {output_path}")
