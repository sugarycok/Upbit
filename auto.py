import pyupbit
import datetime
import time
import numpy as np
from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

class AutoTrade:
    def __init__(self, start_cash, ticker, sid):
        self.fee = 0.05
        self.target_price = 0
        self.ma5 = 0
        self.ticker = ticker
        self.buy_yn = False
        self.start_cash = start_cash
        self.sid = sid
        self.timer = 0
        self.prices = []
        self.target_prices = []
        self.get_today_data()

    def start(self):
        now = datetime.datetime.now()
        socketio.emit('status_update', {
                      'message': f"자동 매매 프로그램이 시작되었습니다\n시작 시간: {now}\n매매 대상: {self.ticker}\n시작 자산: {self.start_cash}"}, room=self.sid)
        openTime = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(days=1, hours=9, seconds=10)

        while True:
            try:
                now = datetime.datetime.now()
                current_price = pyupbit.get_current_price(self.ticker)
                self.prices.append(current_price)
                self.target_prices.append(self.target_price)
                self.send_price_update(current_price, self.target_price)

                if self.timer % 60 == 0:
                    status_message = f"{now}\n거래 시작 시간: {openTime}\n목표 매수가: {self.target_price:.2f}\n현재가: {current_price:.2f}\n5일 이동평균: {self.ma5:.2f}\n매수 여부: {'예' if self.buy_yn else '아니오'}"

                    # 상승/하강 추세 결정
                    if len(self.prices) > 1:
                        trend = "상승" if self.prices[-1] > self.prices[-2] else "하락"
                        status_message += f"\n추세: {trend}"

                    print(status_message)
                    socketio.emit('status_update', {'message': status_message}, room=self.sid)

                if openTime < now < openTime + datetime.timedelta(seconds=5):
                    openTime = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(days=1, hours=9, seconds=10)
                    if self.buy_yn:
                        sell_message = "==================== [ 매도 시도 ] ===================="
                        print(sell_message)
                        socketio.emit('status_update', {'message': sell_message}, room=self.sid)
                        self.sell_coin()
                    self.get_today_data()

                if (current_price >= self.target_price) and (current_price >= self.ma5) and not self.buy_yn:
                    buy_message = "==================== [ 매수 시도 ] ===================="
                    print(buy_message)
                    socketio.emit('status_update', {'message': buy_message}, room=self.sid)
                    self.buy_coin()
            except Exception as err:
                error_message = f"!!! 프로그램 오류 발생 !!!\n{err}"
                print(error_message)
                socketio.emit('status_update', {'message': error_message}, room=self.sid)

            self.timer += 1
            time.sleep(1)

    def send_price_update(self, current_price, target_price):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        socketio.emit('price_update', {'time': now, 'current_price': current_price, 'target_price': target_price}, room=self.sid)

    def get_today_data(self):
        print("\n==================== [ 데이터 갱신 시도 ] ====================")
        daily_data = pyupbit.get_ohlcv(self.ticker, count=41)
        daily_data['noise'] = 1 - abs(daily_data['open'] - daily_data['close']) / (daily_data['high'] - daily_data['low'])
        daily_data['noise_ma20'] = daily_data['noise'].rolling(window=20).mean().shift(1)
        daily_data['range'] = daily_data['high'] - daily_data['low']
        daily_data['targetPrice'] = daily_data['open'] + daily_data['range'].shift(1) * daily_data['noise_ma20']
        daily_data['ma5'] = daily_data['close'].rolling(window=5, min_periods=1).mean().shift(1)
        today = daily_data.iloc[-1]
        self.target_price = today.targetPrice
        self.ma5 = today.ma5
        print("==================== [ 데이터 갱신 완료 ] ====================\n")
        socketio.emit('status_update', {'message': "==================== [ 데이터 갱신 완료 ] ===================="}, room=self.sid)

    def buy_coin(self):
        self.buy_yn = True
        balance = upbit.get_balance()
        if balance > 5000:
            upbit.buy_market_order(self.ticker, balance * 0.9995)
            buy_price = pyupbit.get_orderbook(self.ticker)['orderbook_units'][0]['ask_price']
            buy_message = f"====================매수 시도====================\n#매수 주문\n매수 주문 가격: {buy_price:.2f}원"
            print(buy_message)
            socketio.emit('status_update', {'message': buy_message}, room=self.sid)

    def sell_coin(self):
        self.buy_yn = False
        balance = upbit.get_balance(self.ticker)
        upbit.sell_market_order(self.ticker, balance)
        sell_price = pyupbit.get_orderbook(self.ticker)['orderbook_units'][0]['bid_price']
        sell_message = f"====================매도 시도====================\n#매도 주문\n매도 주문 가격: {sell_price:.2f}원"
        print(sell_message)
        socketio.emit('status_update', {'message': sell_message}, room=self.sid)

@app.route('/')
def home():
    return render_template('auto.html')

@app.route('/start', methods=['POST'])
def start():
    data = request.get_json()
    ticker = data['ticker']
    sid = data['sid']
    print('Received data from client - 티커:', ticker, '소켓 ID:', sid)
    with open("api.txt", encoding='utf-8') as f:
        lines = f.readlines()
        access_key = lines[0].strip()
        secret_key = lines[1].strip()

    print(f"Using Access Key: {access_key}")
    print(f"Using Secret Key: {secret_key}")
    try:
        global upbit
        upbit = pyupbit.Upbit(access_key, secret_key)
        start_cash = upbit.get_balance()
        print(f"Start cash: {start_cash}")
        tradingBot = AutoTrade(start_cash, ticker, sid)
        global auto_trade
        auto_trade = tradingBot
        socketio.start_background_task(target=tradingBot.start)
        return 'Trading started!'
    except Exception as e:
        error_message = f"Error: {e}"
        print(error_message)
        socketio.emit('status_update', {'message': error_message}, room=sid)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    global auto_trade
    auto_trade = None
    socketio.run(app, host='0.0.0.0', port=5002)
