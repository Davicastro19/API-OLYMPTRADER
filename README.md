# OlympTradeAPI: Biblioteca Python para Olymp Trade

Uma biblioteca Python fácil de usar para integrar-se com a [Olymp Trade](https://olymptrade.com/pt-br).

## Valor

A API está disponível por R$700,00. 

## Contato

Para mais informações ou suporte, entre em contato via [Telegram](https://t.me/reactdavicastro).
## Pré-requisitos
Certifique-se de ter instalado as seguintes dependências:

```bash
pip install 2captcha-python==1.2.1 aiohttp==3.8.5 aiosignal==1.3.1 APScheduler==3.6.3 async-timeout==4.0.3 attrs==23.1.0 Babel==2.13.0 certifi==2023.7.22 cffi==1.16.0 charset-normalizer==3.2.0 cryptography==41.0.4 frozenlist==1.4.0 idna==3.4 multidict==6.0.4 mysql-connector-python==8.0.24 protobuf==4.24.3 pycparser==2.21 python-dateutil==2.8.2 python-telegram-bot==13.5 pytz==2023.3.post1 requests==2.31.0 shortuuid==1.0.11 six==1.16.0 tornado==6.3.3 tzdata==2023.3 tzlocal==5.0.1 urllib3==2.0.5 websocket-client==0.56.0 yarl==1.9.2

Uso
Aqui está um exemplo simples para começar:

python
Copy code
from olymptradeapi.api import OlympTradeAPI

API = OlympTradeAPI('seu_email@example.com', 'sua_senha')

status, motive = API.connect()
print(status, motive)

balance = API.get_balance()
print(balance)

st, teste = API.buy(1, 'BTCUSD', 'call', 1)
print(st, teste)
Conecte-se à Olymp Trade
Esta biblioteca foi desenvolvida para facilitar a integração e automação na plataforma Olymp Trade. Aproveite!

