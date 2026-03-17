# ai-defi-lab: Arbitrum Wallet Inspector

Small Python lab for inspecting Arbitrum wallets with Web3.py.  
It connects to an Arbitrum RPC endpoint, loads a burner wallet from `.env`, and prints the current block number, native ETH balance, and selected ERC‑20 token balances.

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
- Two scripts:
  - `check_block_number.py` – quick network connectivity check
  - `balances.py` – read wallet ETH and ERC‑20 balances

## Setup

Requirements:

- Python 3.10+
- Git
- An Arbitrum RPC URL (public endpoint or provider like Alchemy/Infura)
- A test EVM wallet address (burner / low‑risk)

Clone and create the virtualenv:

```bash
git clone https://github.com/<your-username>/ai-defi-lab.git
cd ai-defi-lab

python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .\.venv\Scripts\Activate.ps1  # Windows PowerShell
Install dependencies:
```
```bash
pip install -r requirements.txt
# or:
# pip install web3 eth-account python-dotenv requests
Create a .env file in the project root:

ARBITRUM_RPC_URL=https://arb1.arbitrum.io/rpc
TEST_WALLET_ADDRESS=0xYourBurnerAddressHere
.env is already in .gitignore; don’t commit secrets.

Usage
Check that the Web3 connection works and print the latest Arbitrum block:
```
```bash
python check_block_number.py
Fetch the wallet’s ETH and selected ERC‑20 token balances:
```
```bash
python balances.py
To change which tokens are checked, edit the TOKENS mapping in balances.py and plug in real token contract addresses.

Example output
Example check_block_number.py run:

dotenv_path: /Users/.../ai-defi-lab/.env
.env loaded: True
Attempting to connect to RPC endpoint: https://arb1.arbitrum.io/rpc
Current block number on Arbitrum: 442570471
Test wallet address: 0x...
Example balances.py run:

Connected to Arbitrum at block: 442570471
Wallet: 0x...
ETH balance: 0.0123 ETH
WETH balance: 0.0000 WETH
USDC balance: 0.00 USDC
ARB balance: 42.00 ARB
Tech stack
Python 3.x

[Web3.py](navigational_search:web3.py GitHub) for Arbitrum JSON‑RPC calls

python-dotenv for .env loading
```