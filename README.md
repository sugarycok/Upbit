
# Crypto Trading Dashboard | 크립토 트레이딩 대시보드

## Overview | 개요
This project provides a comprehensive dashboard for cryptocurrency trading and monitoring using the Upbit API. It includes various features like fetching market data, automated trading, transaction history, asset status, and coin price prediction.

이 프로젝트는 업비트 API를 사용하여 암호화폐 거래 및 모니터링을 위한 종합 대시보드를 제공합니다. 시장 데이터 가져오기, 자동 거래, 거래 내역, 자산 상태, 코인 가격 예측 등 다양한 기능을 포함하고 있습니다.

## Features | 기능
### 1. Market Data and Ticker Information | 시장 데이터 및 티커 정보
- **Fetches the list of all listed coins and their current prices.**
  - 상장된 모든 코인의 목록과 현재 가격을 가져옵니다.
- **Displays coin data including name, market code, and current price.**
  - 코인 이름, 시장 코드, 현재 가격을 포함한 코인 데이터를 표시합니다.

### 2. Automated Trading | 자동 거래
- **Implements an automated trading system using predefined strategies.**
  - 사전 정의된 전략을 사용하여 자동 거래 시스템을 구현합니다.
- **Includes a real-time status update system via WebSocket.**
  - WebSocket을 통한 실시간 상태 업데이트 시스템을 포함합니다.

### 3. Transaction History and Asset Status | 거래 내역 및 자산 상태
- **Provides transaction history including deposits, withdrawals, and trades.**
  - 입출금 및 거래를 포함한 거래 내역을 제공합니다.
- **Displays current asset holdings and their status.**
  - 현재 자산 보유 현황과 상태를 표시합니다.

### 4. Coin Price Prediction | 코인 가격 예측
- **Predicts future coin prices using machine learning models.**
  - 머신러닝 모델을 사용하여 미래 코인 가격을 예측합니다.
- **Generates and displays prediction graphs.**
  - 예측 그래프를 생성하고 표시합니다.

### 5. User Authentication | 사용자 인증
- **Includes login and registration pages for user authentication.**
  - 사용자 인증을 위한 로그인 및 회원가입 페이지를 포함합니다.
- **Users can save their Upbit API keys for personalized usage.**
  - 사용자는 개인화된 사용을 위해 자신의 Upbit API 키를 저장할 수 있습니다.

## Project Structure | 프로젝트 구조
```
project_root
│
├── auto.py
├── graph.py
├── list.py
├── main.js
├── self.py
├── socket.js
├── ui.js
│
├── templates
│   ├── index.html
│   ├── auto.html
│   ├── coin.html
│   ├── self.html
│   ├── login.html
│   └── register.html
│
└── static
    └── ... (static assets)
```

## File Descriptions | 파일 설명
### Python Scripts | 파이썬 스크립트
- **list.py**: Fetches market data and coin prices from Upbit API.
  - 업비트 API에서 시장 데이터와 코인 가격을 가져옵니다.
- **self.py**: Handles user asset status, transaction history, and deposit/withdrawal status using Flask.
  - Flask를 사용하여 사용자 자산 상태, 거래 내역 및 입출금 상태를 처리합니다.
- **auto.py**: Implements the automated trading logic with Flask and SocketIO for real-time updates.
  - Flask와 SocketIO를 사용하여 실시간 업데이트를 위한 자동 거래 로직을 구현합니다.
- **graph.py**: Provides coin price prediction using LSTM models and serves prediction data and graphs via Flask.
  - LSTM 모델을 사용하여 코인 가격 예측을 제공하고 Flask를 통해 예측 데이터와 그래프를 제공합니다.

### JavaScript Files | 자바스크립트 파일
- **socket.js**: Manages WebSocket connections for real-time status updates during automated trading.
  - 자동 거래 중 실시간 상태 업데이트를 위한 WebSocket 연결을 관리합니다.
- **ui.js**: Handles UI interactions, form submissions, and status updates.
  - UI 상호작용, 폼 제출 및 상태 업데이트를 처리합니다.

### HTML Files | HTML 파일
- **index.html**: Main dashboard displaying current coin prices.
  - 현재 코인 가격을 표시하는 메인 대시보드.
- **auto.html**: Interface for starting and monitoring automated trading.
  - 자동 거래 시작 및 모니터링을 위한 인터페이스.
- **coin.html**: Interface for coin price prediction.
  - 코인 가격 예측을 위한 인터페이스.
- **self.html**: User dashboard displaying transaction history, asset status, and deposit/withdrawal information.
  - 거래 내역, 자산 상태 및 입출금 정보를 표시하는 사용자 대시보드.
- **login.html**: User login page.
  - 사용자 로그인 페이지.
- **register.html**: User registration page.
  - 사용자 회원가입 페이지.

## Installation | 설치
1. **Clone the repository | 저장소 복제**
   ```sh
   git clone https://github.com/yourusername/crypto-trading-dashboard.git
   cd crypto-trading-dashboard
   ```

2. **Install dependencies | 종속성 설치**
   ```sh
   pip install -r requirements.txt
   ```

3. **Setup Upbit API keys | Upbit API 키 설정**
   - Create a file named `api.txt` in the root directory with your Upbit API keys:
     - 루트 디렉토리에 `api.txt` 파일을 생성하고 Upbit API 키를 입력합니다:
     ```
     ACCESS_KEY
     SECRET_KEY
     ```

4. **Run the servers | 서버 실행**
   - Start the Flask server for the dashboard:
     - 대시보드용 Flask 서버를 시작합니다:
     ```sh
     python self.py
     ```
   - Start the Flask server for automated trading:
     - 자동 거래용 Flask 서버를 시작합니다:
     ```sh
     python auto.py
     ```
   - Start the Flask server for coin price prediction:
     - 코인 가격 예측용 Flask 서버를 시작합니다:
     ```sh
     python graph.py
     ```

5. **Access the Dashboard | 대시보드 접근**
   Open a web browser and navigate to `http://localhost:5000` to access the main dashboard.
   - 웹 브라우저를 열고 `http://localhost:5000`로 이동하여 메인 대시보드에 접근합니다.

## Usage | 사용법
- **Main Dashboard (`index.html`)**: Displays current coin prices and allows navigation to other features.
  - 현재 코인 가격을 표시하고 다른 기능으로 이동할 수 있는 메인 대시보드.
- **Automated Trading (`auto.html`)**: Start automated trading by entering the coin code.
  - 코인 코드를 입력하여 자동 거래를 시작합니다.
- **Coin Prediction (`coin.html`)**: Enter the coin code to predict future prices.
  - 코인 코드를 입력하여 미래 가격을 예측합니다.
- **User Dashboard (`self.html`)**: View transaction history, asset status, and deposit/withdrawal information.
  - 거래 내역, 자산 상태 및 입출금 정보를 확인합니다.
- **Login (`login.html`)**: Log in to access personalized features.
  - 로그인하여 개인화된 기능에 접근합니다.
- **Register (`register.html`)**: Create a new account and save API keys.
  - 새 계정을 생성하고 API 키를 저장합니다.

## License | 라이센스
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
이 프로젝트는 MIT 라이센스 하에 있습니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.
