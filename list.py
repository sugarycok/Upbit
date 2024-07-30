import requests
import json

server_url = 'https://api.upbit.com'

# 상장된 모든 코인 목록 가져오기
def get_market_list():
    try:
        url = server_url + '/v1/market/all'
        headers = {"Accept": "application/json"}

        res = requests.get(url, headers=headers)
        res.raise_for_status()  # 요청 실패 시 예외 발생
        return res.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching market list: {e}")
        return []

# 특정 코인의 현재 시세 가져오기
def get_ticker(markets):
    try:
        url = server_url + '/v1/ticker'
        headers = {"Accept": "application/json"}
        params = {'markets': ','.join(markets)}

        res = requests.get(url, headers=headers, params=params)
        res.raise_for_status()  # 요청 실패 시 예외 발생
        return res.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching ticker: {e}")
        return []

# 상장된 코인 목록과 현재 시세 가져오기
def get_market_with_price():
    market_list = get_market_list()
    
    # KRW 마켓만 필터링 (원화로 거래되는 코인들)
    krw_markets = [market['market'] for market in market_list if market['market'].startswith('KRW-')]
    
    # 현재 시세 가져오기
    ticker_info = get_ticker(krw_markets)

    # 시장 코드와 코인 이름 매칭
    market_info = {market['market']: market for market in market_list}

    # 결과 출력
    result = []
    for ticker in ticker_info:
        market_code = ticker['market']
        market = market_info.get(market_code, {})
        name = market.get('korean_name', 'Unknown')
        english_name = market.get('english_name', 'Unknown')
        price = ticker.get('trade_price', 0)
        result.append({'name': name, 'english_name': english_name, 'market_code': market_code, 'price': price})
    
    # 코인 이름을 가나다 순으로 정렬
    result_sorted = sorted(result, key=lambda x: x['name'])

    return result_sorted

# JSON 형식으로 출력 (ASCII로 변환)
if __name__ == '__main__':
    try:
        market_with_price = get_market_with_price()
        print(json.dumps(market_with_price, ensure_ascii=True, indent=4))
    except Exception as e:
        print(f"Error in main: {e}")
