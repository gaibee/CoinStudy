from fastapi import FastAPI, Request, Body
import uvicorn
from pydantic import BaseModel
import pyupbit
from dotenv import load_dotenv
import os

load_dotenv() # .env 파일을 불러온다.

app = FastAPI()

# 환경변수 또는 직접 입력
ACCESS_KEY = os.getenv('UPBIT_ACCESS_KEY')
SECRET_KEY = os.getenv('UPBIT_SECRET_KEY')

upbit = pyupbit.Upbit(ACCESS_KEY, SECRET_KEY) # 업비트를 다룰 수 있는 모델 초기화 

FEE_RATE = 0.0005 # 업비트 수수료 0.05%


# 일반 함수들 #################################################

def _buy_full_market_order(ticker:str):
    krw_balance = upbit.get_balance("KRW") # 내 업비트 계정에서 원화 잔고를 가져옴
    if not krw_balance:
        raise Exception('잔고를 가져올 수 없습니다.')
        
    if not krw_balance > 5000: # 최소 매수 금액 고려
        raise Exception('잔고가 5000원 미만입니다.')
        
    krw_to_use = krw_balance * (1 - FEE_RATE) # 잔고에서 수수류를 뺀 나머지를 계산
    return upbit.buy_market_order(ticker, krw_to_use) # 시장가 주문으로 전체 원화만큼 매수

def _sell_full_market_order(ticker:str):
    ticker_balance = upbit.get_balance(ticker) # 내 업비트 계정에서 코인 잔고를 가져옴
    if not ticker_balance:
        raise Exception(f'{ticker} 잔고를 가져올 수 없습니다.')
        
    return upbit.sell_market_order(ticker, ticker_balance) # 시장가 주문으로 코인 전체를 매도함

####################################################################







# 서버 접속 주소들 정의 ###############################################

@app.get('/') # http://내주소:포트/ 로 GET 요청이 오면 아래 함수를 실행함
def index():
    return '나의 서버에 온걸 환영합니다'

@app.get('/test_buy') # http://내주소:포트/test_buy로 GET 요청이 오면 아래 함수를 실행함
def test_buy(ticker:str): # http://내주소:포트/test_buy?ticker=매수할코인 링크로 요청이 오면 매수할코인을 ticker 변수에 저장
    try:
        return _buy_full_market_order(ticker)
    except Exception as e:
        return {"status":"failed", "reason":str(e)}

@app.get('/test_sell') # http://내주소:포트/test_sell로 GET 요청이 오면 아래 함수를 실행함
def test_sell(ticker:str): # http://내주소:포트/test_buy?ticker=매수할코인 링크로 요청이 오면 매수할코인을 ticker 변수에 저장
    try:
        return _sell_full_market_order(ticker)
    except Exception as e:
        return {"status":"failed", "reason":str(e)}
    
@app.post('/tv_message') # http://내주소:포트/tv_message로 POST 요청이 오면 아래 함수를 실행함
async def tv_message(raw_data: str = Body(..., media_type="text/plain")): # POST 요청이 오면 전송된 데이터를 raw_data에 저장함
    message = raw_data # raw_data를 message 변수에 저장함

    if message == "buy": # 만약 전송된 데이터가 "buy"라는 문자열이라면
        try:
            result = _buy_full_market_order("KRW-BTC") # buy_full_market_morder 함수를 실행
            return {"status": "buy", "result": result}
        except Exception as e:
            return {"status": "failed", "reason": str(e)}

    elif message == "sell": # 만약 전송된 데이터가 "sell"라는 문자열이라면
        try:
            result = _sell_full_market_order("KRW-BTC") # sell_full_market_morder 함수를 실행
            return {"status": "buy", "result": result}
        except Exception as e:
            return {"status": "failed", "reason": str(e)}

    else:
        return {"status": "ignored", "message": message}

#####################################################################3



if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=5004, reload=True)
