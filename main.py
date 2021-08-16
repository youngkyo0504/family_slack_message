from github_utils import upload_bull_market_issue
import os

access_token = os.environ['MY_GITHUB_TOKEN']

upload_bull_market_issue(access_token,"is_bull_market")


