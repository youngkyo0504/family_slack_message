import os
import pyupbit
import requests


# api연결
access = os.environ["UPBIT_ACCESS"]
secret = os.environ["UPBIT_SECRET"]
upbit = pyupbit.Upbit(access, secret)


def calculate_kimchi_premium(kr_price, exchange_rate):
    premium = ((kr_price - exchange_rate) / exchange_rate) * 100
    return round(premium, 2)


def fetch_exchange():
    # 환율 정보 조회
    exchange_rate = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
    usd_to_krw = exchange_rate.json()["rates"]["KRW"]

    return usd_to_krw


def get_tether_premium():
    # USDT/KRW 가격 가져오기 (업비트)
    usdt_krw = pyupbit.get_current_price("KRW-USDT")

    # 현재 환율 가져오기
    exchange_rate = fetch_exchange()

    if not usdt_krw or not exchange_rate:
        return "가격 정보를 가져오는데 실패했습니다."

    # 김치프리미엄 계산
    premium = calculate_kimchi_premium(usdt_krw, exchange_rate)

    # 메시지 작성
    message = f"""
📊 테더 김치프리미엄 현황
- USDT/KRW: {format(round(usdt_krw), ',')}원
- USD/KRW: {format(round(exchange_rate), ',')}원
- 김치프리미엄: {premium}%
    """

    # 프리미엄 수준에 따른 메시지 추가
    if premium > 2.5:
        message += "\n⚠️ 김프가 높습니다. 매수시 주의하세요!"
    elif premium < 0:
        message += "\n💡 김프가 낮습니다. 매수 기회일 수 있습니다."

    return message.strip()
