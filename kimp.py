import os
from avg_price import read_avg_price
import pyupbit

from read_exchange_rate import read_exchange_rate


# api연결
access = os.environ["UPBIT_ACCESS"]
secret = os.environ["UPBIT_SECRET"]
upbit = pyupbit.Upbit(access, secret)


def calculate_kimchi_premium(kr_price, exchange_rate):
    premium = ((kr_price - exchange_rate) / exchange_rate) * 100
    return round(premium, 2)


def fetch_exchange():
    # 환율 정보 조회
    exchange_rate = float(read_exchange_rate())

    return exchange_rate


def fetch_avg_price():
    # 평균 매수가 조회
    avg_price, quantity = read_avg_price()

    return float(avg_price), float(quantity)


def get_tether_premium():
    # USDT/KRW 가격 가져오기 (업비트)
    usdt_krw = pyupbit.get_current_price("KRW-USDT")

    # 현재 환율 가져오기
    exchange_rate = fetch_exchange()

    if not usdt_krw or not exchange_rate:
        return "가격 정보를 가져오는데 실패했습니다."

    # 김치프리미엄 계산
    premium = calculate_kimchi_premium(usdt_krw, exchange_rate)
    avg_price, quantity = fetch_avg_price()

    # 메시지 작성
    message = f"""
📊 테더 김치프리미엄 현황
- USDT/KRW: {format(round(usdt_krw), ',')}원
- USD/KRW: {format(round(exchange_rate), ',')}원
- 김치프리미엄: {premium}%
- 현재 수익률: { (round(usdt_krw) - round(avg_price)) / round(usdt_krw) * 100:.2f}%
- 실현 가능 차익: {  (round(usdt_krw) - round(avg_price)) *  quantity:.2f}원
    """

    # 프리미엄 수준에 따른 메시지 추가
    if premium > 2.5:
        message += "\n⚠️ 김프가 높습니다. 매수시 주의하세요!"
    elif premium < 1:
        message += "\n💡 김프가 낮습니다. 매수 기회일 수 있습니다."

    return message.strip()
