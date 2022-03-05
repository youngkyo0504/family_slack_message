import os
import pyupbit
from datetime import datetime
from pytz import timezone





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
def is_bull(maList):
    rank_arr = sorted(maList.keys(),reverse=True, key=lambda x: x[0])
    money = [ maList[ma] for ma in rank_arr]
    limit = 3
    for i in range(limit-1):
        if money[i] < money[i+1] :
            return False
    return True

def make_message(ma,is_bull):
    rank_arr = sorted(ma.items(), reverse=True, key=lambda x: x[1])
    currentTime = datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d %H:%M')
    rank_string = f'높은 가격 순서입니다.({currentTime} 기준)  \n'
    for ma in rank_arr:
        name, price = ma
        price = format(round(price), ',')
        if name == "0":
            rank_string += f'- 현재 가격 : {price} 원 \n'
            continue
        rank_string += f'- {name}일 평균 : {price} 원 \n'
    if is_bull :
        rank_string + "꼭 사야됩니다😁"
    return rank_string

def bull_market(ticker):
    df = pyupbit.get_ohlcv(ticker,count=120)
    close = df['close']
    ma = {
    '120' : close.mean(),
    '20' : close.iloc[-21:-1].mean(),
    '60' : close.iloc[-61:-1].mean(),
    '5' : close.iloc[-6: -1].mean(),
    '0': pyupbit.get_current_price(ticker)
    }
    result = make_message(ma,is_bull(ma))
    return result
