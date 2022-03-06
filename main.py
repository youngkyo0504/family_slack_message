from bull_market import bull_market
from github_utils import upload_bull_market_issue
from slack import post_message
import os

access_token = os.environ['MY_GITHUB_TOKEN']
slack_token = os.environ['SLACK_TOKEN']
body = bull_market("KRW-BTC")
upload_bull_market_issue(access_token,"is_bull_market",body)
post_message(slack_token,'#알람',body)


