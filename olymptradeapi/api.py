#SEGUE PARTE DO CODIGO NÃO FUNCIONA SE N COMPRAR A COMPLETO
from olymptradeapi.constants import ACTIVES, REVERSE
from threading import Thread
import ssl, json, time, requests, shortuuid, websocket

class OlympTradeAPI:
    def __init__(self, email, password): 
        self.email = email
        self.password = password
        self.orders, self.orders_close, self.candles, self.alerts_triggered, self.realtime_order = {}, {}, {}, {}, {}
        self.balance, self.session, self.alerts = None, None, None
        self.ssl_Mutual_exclusion, self.ssl_Mutual_exclusion_write = False, False
        self.account_data = {'demo': {}, 'real': {}}
        self.instruments = {'turbo': {},  'binary': {}, 'digital': {}}
        self.balance_type = 'demo'
        self.reconnect_count = 1

    def on_error(self, ws, error):
        print(error)
        self.connectedStatus = False
        self.check_websocket_if_connect = False

    def on_close(self, ws, close_status_code, close_msg):
        print(f'closed {close_status_code} {close_msg}')
    
    def on_open(self, ws):
        self.check_websocket_if_connect = True
        self.check_websocket_if_error = False

    def on_message(self, ws, message):
        self.ssl_Mutual_exclusion = True
        data = json.loads(message)
        for message in data:
            #print(message)
            if message['e'] == 10:
           ctive] = {'open': [locked, 100 - asset['winperc']]}
                    self.instruments['digital'][active] = {'open': [locked, asset['winperc']]}
            elif message['e'] == 72:
                for asset in message['d']:
                    active = REVERSE[asset['pair']] if asset['pair'] in REVERSE else asset['pair']
                    active = active.replace('_', '-')
                    self.instruments['turbo'][active] = {'open': [True, 100 - asset['winperc']]}
                    self.instruments['binary'][active] = {'open': [True, 100 - asset['winperc']]}
                    self.instruments['digital'][active] = {'open': [True, asset['winperc']]}
            elif message['e'] == 312:
                self.alerts = message['d']
            elif message['e'] == 313:
                message = message['d'][0]
                if message['event'] == 'deleted':
                    self.alerts_triggered[message['subs'][0]['price']] = message['subs'][0]['symbol']

        self.ssl_Mutual_exclusion = False

    def check_connect(self):
        return True if self.check_websocket_if_connect == 1 else False

    
    def clear_alerts(self):
        self.alerts = None
       
            self.delete_alert(alert['id'])
            self.alerts.remove(alert)
        
    def check_alert(self, symbol, value):
        return True if value in self.alerts_triggered and self.alerts_triggered[value] == symbol else False
