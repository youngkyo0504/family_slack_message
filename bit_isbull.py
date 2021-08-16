import os
import pyupbit

#api연결
access = os.environ['UPBIT_ACCESS']
secret = os.environ['UPBIT_SECRET']
upbit = pyupbit.Upbit(access, secret)

#상승장인지 구분하겠습니다.
# 120일 60일 20일 5일 현재 순이라면 강한 상승장입니다.
# 위 순서대로 배열될 수록 강한 상승장입니다.
# 현재가격이 20일 평균 가격보다 낮다면 사지 않는 것을 추천합니다.
# 현재가격이 120일 20일 60일 위에 있을 때 사는 것을 추천합니다.
# 가격은 원단위입니다.

def bull_market(ticker):
    df = pyupbit.get_ohlcv(ticker,count=120)
    close = df['close']
    ma = {
    '120일 평균' : close.mean(),
    '20일 평균' : close.iloc[-21:-1].mean(),
    '60일 평균' : close.iloc[-61:-1].mean(),
    '5일 평균' : close.iloc[-6: -1].mean(),
    '현재 가격': pyupbit.get_current_price(ticker)
    }
    rank_arr = sorted(ma.items(), key=lambda x: x[1])
    rank_string = ''
    for ma in rank_arr:
        name, price = ma
        rank_string += f'- {name} : {price} \n'
    return rank_string
