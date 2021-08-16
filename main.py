import pyupbit

#api연결
with open("id.txt") as f:
    lines = f.readlines()
    access = lines[0].strip()
    secret = lines[1].strip()
    upbit = pyupbit.Upbit(access, secret)

# #비트코인의 고가/시가/저가/종가/거래량을 DataFrame(오름차순)으로 변환한다.
# df = pyupbit.get_ohlcv("KRW-BTC")
# #tail은 기본이 5개의 이고 매개값으로 일자를 쓸 수 있습니다.
# print(df.tail())

# close = df['close']
# window = close.rolling(5) #윈도우: 5일씩 그룹화한다.이 윈도우로도 계산이 된다.
# ma5 = window.mean() # mean() 메서드는 그룹화된 값의 평균을 구합니다.
# print(ma5) #즉 이동평균선을 구할 수 있다.


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

    return sorted(ma.items(), key = lambda  x: x[1])

print(bull_market("KRW-BTC"))



