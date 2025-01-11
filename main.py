from bull_market import bull_market
from kimp import get_tether_premium
from github_utils import upload_bull_market_issue
from slack import post_message
from read_exchange_rate import read_exchange_rate
import os

access_token = os.environ["MY_GITHUB_TOKEN"]
slack_token = os.environ["SLACK_TOKEN"]
body = bull_market("KRW-BTC")
tether_premium_message = get_tether_premium()
exchange_rate = read_exchange_rate()
post_message(slack_token, "#알람", body + "\n" + tether_premium_message + '\n' + '환율은 :' exchange_rate)
