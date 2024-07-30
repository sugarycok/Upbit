import requests
import json
import jwt
import uuid
from urllib.parse import urlencode
import hashlib
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from datetime import datetime, timedelta

# API 키를 파일에서 읽어옴
with open("api.txt", encoding='utf-8') as f:
    lines = f.readlines()
    access_key = lines[0].strip()
    secret_key = lines[1].strip()

server_url = 'https://api.upbit.com'

# JWT 토큰 생성 함수
def generate_token(query=None):
    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
    }
    if query:
        query_string = urlencode(query).encode()
        m = hashlib.sha512()
        m.update(query_string)
        query_hash = m.hexdigest()
        payload['query_hash'] = query_hash
        payload['query_hash_alg'] = 'SHA512'
    jwt_token = jwt.encode(payload, secret_key, algorithm='HS256')
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}
    return headers

# 입출금 현황 가져오기
def get_deposit_withdrawal_status():
    url = f"{server_url}/v1/deposits"
    headers = generate_token()
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error in Deposits/Withdrawals API call: {response.json()}")
        return []

# 거래 내역 가져오기
def get_transaction_history():
    url = f"{server_url}/v1/orders"
    headers = generate_token()
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        transactions = response.json()
        for tx in transactions:
            tx['purchase_amount'] = float(tx['price']) * float(tx['volume'])
            tx['sale_amount'] = float(tx['price']) * float(tx['volume'])
            tx['fee'] = float(tx['paid_fee'])
            tx['profit_loss'] = tx['sale_amount'] - tx['purchase_amount'] - tx['fee']
            tx['profit_rate'] = (tx['profit_loss'] / tx['purchase_amount']) * 100
        return transactions
    else:
        print(f"Error in Transaction History API call: {response.json()}")
        return []

# 자산 현황 가져오기
def get_asset_status():
    url = f"{server_url}/v1/accounts"
    headers = generate_token()
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error in Assets API call: {response.json()}")
        return []

# Flask 애플리케이션 설정
app = Flask(__name__, static_folder='public', template_folder='public')
CORS(app)

@app.route('/')
def home():
    return send_from_directory('public', 'self.html')

@app.route('/api/profile_data')
def profile_data():
    from_date = request.args.get('from', (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'))
    to_date = request.args.get('to', datetime.now().strftime('%Y-%m-%d'))
    deposits_withdrawals = get_deposit_withdrawal_status()
    transactions = get_transaction_history()
    assets = get_asset_status()

    # 날짜 필터링
    filtered_deposits_withdrawals = [dw for dw in deposits_withdrawals if from_date <= dw['created_at'][:10] <= to_date]
    filtered_transactions = [tx for tx in transactions if from_date <= tx['created_at'][:10] <= to_date]

    return jsonify({
        'deposits_withdrawals': filtered_deposits_withdrawals,
        'transactions': filtered_transactions,
        'assets': assets
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
