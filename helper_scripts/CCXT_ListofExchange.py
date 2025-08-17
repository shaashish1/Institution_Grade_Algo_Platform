import ccxt

def list_supported_exchanges():
    return ccxt.exchanges

if __name__ == "__main__":
    exchanges = list_supported_exchanges()
    print("Supported Exchanges by CCXT:")
    for ex in exchanges:
        print("-", ex)
