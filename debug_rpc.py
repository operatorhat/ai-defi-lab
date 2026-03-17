import requests

def debug_rpc(rpc_url):
    """
    Debugs the connection to an RPC endpoint by sending a basic JSON-RPC request.
    """
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_blockNumber",
        "params": [],
        "id": 1
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        print(f"Attempting to connect to RPC endpoint: {rpc_url}")
        response = requests.post(rpc_url, json=payload, headers=headers)
        
        if response.status_code == 200:
            print("Connection successful!")
            print("Response:")
            print(response.json())
        else:
            print(f"Connection failed with status code: {response.status_code}")
            print("Response:")
            print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while connecting to the RPC endpoint: {e}")

if __name__ == "__main__":
    # Replace with your RPC endpoint URL
    rpc_url = "http://localhost:8545"
    debug_rpc(rpc_url)