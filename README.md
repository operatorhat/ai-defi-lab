# ai-defi-lab: Arbitrum Wallet Inspector

Small Python lab for inspecting Arbitrum wallets with Web3.py.  
It connects to an Arbitrum RPC endpoint, loads a burner wallet from `.env`, and prints the current block number, native ETH balance, selected ERC‑20 token balances, and a structured JSON snapshot.

## Why this exists

This repo is my first brick toward a personal, automated DeFi “bank” that actually understands my on‑chain life.  
I’m using it to train the muscle of reading networks, wallets, and tokens from code instead of relying on dashboards, so future systems like PersonalBank can see and act on my positions in real time.

## Who this is for

This is for anyone who wants to stop treating DeFi as a black box and start scripting it — especially builders who are comfortable with Python but new to Web3.py and Arbitrum.  
If you want a tiny, boring‑reliable starting point for on‑chain automation and portfolio tooling, this is it.

## Overview

This repo is a minimal starting point for DeFi scripting in Python: a clean virtualenv, `.env`‑based config, and a Web3.py client wired to Arbitrum One.  
It’s meant as a foundation for more serious DeFi automations and portfolio tooling, not a one‑off script.

You get:

- Isolated virtual environment using `venv`
- Environment variables via `.env` (RPC URL and test wallet)
- Web3.py client configured for Arbitrum One
- Config‑driven token registry in `config/tokens.json`
- JSON balance snapshots written to `snapshots/`
- Three scripts:
  - `check_block_number.py` – quick network connectivity check
  - `balances.py` – read wallet ETH and ERC‑20 balances and write a JSON snapshot
  - `debug_rpc.py` – minimal raw RPC connectivity check without Web3

## Setup

### Requirements

- Python 3.10+
- Git
- An Arbitrum RPC URL (public endpoint or provider like Alchemy/Infura)
- A test EVM wallet address (burner / low‑risk)

### Clone and create the virtualenv

```bash
git clone https://github.com/<your-username>/ai-defi-lab.git
cd ai-defi-lab

python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .\.venv\Scripts\Activate.ps1  # Windows PowerShell
```

### Install dependencies

```bash
pip install -r requirements.txt
# or:
# pip install web3 eth-account python-dotenv requests
```

### Configure environment

Create a `.env` file in the project root:

```env
ARBITRUM_RPC_URL=https://arb1.arbitrum.io/rpc
TEST_WALLET_ADDRESS=0xYourBurnerAddressHere
```

`.env` is already in `.gitignore`; don’t commit secrets.

## Usage

### Check RPC connectivity

Verify that the Web3 connection works and print the latest Arbitrum block:

```bash
python check_block_number.py
```

### Fetch balances and write a snapshot

Fetch the wallet’s native ETH and ERC‑20 token balances, and write a JSON snapshot to `snapshots/`:

```bash
python balances.py
```

Running `python balances.py` will:

- Print the current block number, wallet address, and per‑token balances
- Write a JSON snapshot file to `snapshots/` using the config in `config/tokens.json`

Each snapshot includes:

- `timestamp` (ISO 8601, UTC)
- `block_number`
- `wallet_address`
- `balances`: an array of per‑token objects with `symbol`, `address`, `decimals`, `risk_tier`, `coingecko_id`, `raw_balance` (string), and `human_balance` (float)

### Configure tracked tokens

To change which tokens are checked, edit `config/tokens.json` and add or remove token entries.  
Each entry needs:

- `symbol` – token symbol, e.g. `"WETH"`
- `address` – token contract address on Arbitrum
- `decimals` – ERC‑20 decimals (e.g. 18 for WETH, 6 for USDC)
- `risk_tier` – informal risk label such as `"low"`, `"medium"`, `"high"`
- `coingecko_id` – CoinGecko asset ID for future price lookups (e.g. `"weth"`, `"usd-coin"`)

### Debug raw RPC connectivity

Optionally, debug raw RPC connectivity (no Web3 dependency):

```bash
python debug_rpc.py
```

## Example output

### Example `check_block_number.py` run

```text
dotenv_path: /Users/.../ai-defi-lab/.env
.env loaded: True
Attempting to connect to RPC endpoint: https://arb1.arbitrum.io/rpc
Current block number on Arbitrum: 442570471
Test wallet address: 0x...
```

### Example `balances.py` run

```text
Connected to Arbitrum at block: 442570471
Wallet: 0x...
ETH balance: 0.0123 ETH
WETH balance: 0.0000 WETH
USDC balance: 0.00 USDC
ARB balance: 42.00 ARB
Snapshot written to snapshots/snapshot_442570471.json
```

## Tech stack

- Python 3.x  
- [Web3.py](https://github.com/ethereum/web3.py) for Arbitrum JSON‑RPC calls  
- `python-dotenv` for `.env` loading  
- `requests` for raw RPC debugging
```
