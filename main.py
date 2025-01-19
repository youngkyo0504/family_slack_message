from bull_market import bull_market
from kimp import get_tether_premium
from slack import post_message
from risk import get_risk_info
import os

access_token = os.environ["MY_GITHUB_TOKEN"]
slack_token = os.environ["SLACK_TOKEN"]
body = bull_market("KRW-BTC")
tether_premium_message = get_tether_premium()
risk_info = get_risk_info("BTC")


post_message(
    slack_token,
    "#알람",
    body
    + "\n\n"
    + tether_premium_message
    + "\n\n"
    + "현재 리스크는"
    + risk_info["current_risk"]
    + "입니다.",
)
