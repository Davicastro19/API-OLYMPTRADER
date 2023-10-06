from olymptradeapi.get_session import get_session
from olymptradeapi.expiration import get_expiration_time
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
        self.check_websocket_if_error = True
        self.websocket_error_reason = error

    def on_close(self, ws, close_status_code, close_msg):
        print(f'closed {close_status_code} {close_msg}')
        self.check_websocket_if_connect = False
        self.connectedStatus = False
        self.reconnect()
    
    def on_open(self, ws):
        self.check_websocket_if_connect = True
        self.check_websocket_if_error = False

    def on_message(self, ws, message):
        self.ssl_Mutual_exclusion = True
        data = json.loads(message)
        for message in data:
            #print(message)
            if message['e'] == 10:
                id = message['uuid']
                self.candles[id] = None if 'err' in message else message['d'][0]['candles']
            elif message['e'] == 21:
                for realtime_order in message['d']:
                    id = realtime_order['id']
                    self.realtime_order[id] = realtime_order
            elif message['e'] == 23:
                uuid = message['uuid']
                message = message['d'][0] if not 'err' in message else message['err'][0]
                self.orders[uuid] = message
            elif message['e'] == 26:
                for orders_close in message['d']:
                    self.orders_close[orders_close['id']] = orders_close
            elif message['e'] == 54:
                self.balance = message['d']
            elif message['e'] == 74:
                for asset in message['d']:
                    locked = True if asset['locked'] == False else False
                    active = REVERSE[asset['id']] if asset['id'] in REVERSE else asset['id']
                    active = active.replace('_', '-')
                    self.instruments['turbo'][active] = {'open': [locked, 100 - asset['winperc']]}
                    self.instruments['binary'][active] = {'open': [locked, 100 - asset['winperc']]}
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
        data = [{"t":2,"e":98,"uuid":"LAJXEI79ZPT0FBH2Q","d":[310,311,312,313]}]
        self.send_websocket_request(data)

        data = [{"t":2,"e":312,"uuid":"LAJXL94BNIT0GQXOB6"}]
        self.send_websocket_request(data)

        while self.alerts is None:
            pass
        
        for alert in self.alerts:
            self.delete_alert(alert['id'])
            self.alerts.remove(alert)
        
    def check_alert(self, symbol, value):
        return True if value in self.alerts_triggered and self.alerts_triggered[value] == symbol else False