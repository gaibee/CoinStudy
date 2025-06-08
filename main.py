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

class TVMessage(BaseModel):
    type:str


@app.get('/test_buy')
def buy_full_market_order(ticker:str):
    krw_balance = upbit.get_balance("KRW")
    if not krw_balance:
        raise Exception('잔고를 가져올 수 없습니다.')
        
    if not krw_balance > 5000: # 최소 매수 금액 고려
        raise Exception('잔고가 5000원 미만입니다.')
        
    krw_to_use = krw_balance * (1 - FEE_RATE)
    return upbit.buy_market_order(ticker, krw_to_use)

@app.get('/test_sell')
def sell_full_market_order(ticker:str):
    btc_balance = upbit.get_balance(ticker)
    if not btc_balance:
        raise Exception('BTC 잔고를 가져올 수 없습니다.')
        
    return upbit.sell_market_order(ticker, btc_balance)

    
@app.get('/')
def index():
    return '나의 서버에 온걸 환영합니다'

@app.post('/tv_message')
async def tv_message(raw_data: str = Body(..., media_type="text/plain")):
    message = raw_data

    if message == "buy":
        try:
            result = buy_full_market_order("KRW-BTC")
            return {"status": "buy", "result": result}
        except Exception as e:
            return {"status": "failed", "reason": str(e)}

    elif message == "sell":
        try:
            result = sell_full_market_order("KRW-BTC")
            return {"status": "buy", "result": result}
        except Exception as e:
            return {"status": "failed", "reason": str(e)}

    else:
        return {"status": "ignored", "message": message}


if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=5004, reload=True)
