'''
VALLAKKOTTAI MURUGAN THUNAI
Easy Simple Trading Solutions
Telegram @easysimpletradeupdates
Website https://easysimpletrade.blogspot.com
Youtube https://www.youtube.com/@easysimpletrade
GitHub https://github.com/EasySimpleTrade
'''

#Required Libraries
import hashlib
import hmac
import requests #pip install requests
import time
from datetime import datetime, timezone

#Inputs
api_key = 'RaPOmlQmtfObbBFvAES1pG7c5sFQ0Q' #Change you api Key
api_secret = '37oxt3rOvPu4p83PA0j6yX5x06sQJQO5mlxRySuIZGhrYuch5q8pERkK6UN4' #Change youe api secret

base_url = 'https://api.india.delta.exchange'

def generate_signature(secret, message):
    message = bytes(message, 'utf-8')
    secret = bytes(secret, 'utf-8')
    hash = hmac.new(secret, message, hashlib.sha256)
    return hash.hexdigest()

def get_time_stamp():
    d = datetime.now(timezone.utc)
    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    return str(int((d - epoch).total_seconds()))


method = 'GET'
timestamp = get_time_stamp()
path = '/v2/wallet/balances'
url = f'{base_url}{path}'
query_string = ''
payload = ''
signature_data = method + timestamp + path + query_string + payload
signature = generate_signature(api_secret, signature_data)


headers = {
  'Accept': 'application/json',
  'api-key': api_key,
  'signature': signature,
  'timestamp': timestamp
}

wallet_response = requests.get(url, params={}, headers = headers)
wallet_data = wallet_response.json()
print (wallet_data)

input('Press any key to exit ...')
