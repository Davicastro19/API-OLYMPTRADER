from olymptradeapi.api import OlympTradeAPI

API = OlympTradeAPI('', '')

status, motive = API.connect()
print(status, motive)

balance = API.get_balance()
print(balance)
st, teste = API.buy(1, 'BTCUSD', 'call', 1)
print(st,teste)