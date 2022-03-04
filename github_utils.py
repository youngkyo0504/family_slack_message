from github import Github
from datetime import datetime
from pytz import timezone
from bull_market import bull_market

def get_today():
    seoul_timezone = timezone('Asia/Seoul')
    today = datetime.now(seoul_timezone)
    today_data = today.strftime("%Y년 %m월 %d일")
    return today_data

def get_title():
    return get_today() + "비트코인 가격"

def get_github_repo(access_token, repository_name):
    """
    github repo object를 얻는 함수
    :param access_token: Github access token
    :param repository_name: repo 이름
    :return: repo object
    """
    g = Github(access_token)
    repo = g.get_user().get_repo(repository_name)
    return repo


def upload_github_issue(repo, title, body):
    """
    해당 repo에 title 이름으로 issue를 생성하고, 내용을 body로 채우는 함수
    :param repo: repo 이름
    :param title: issue title
    :param body: issue body
    :return: None
    """
    repo.create_issue(title=title, body=body)

def upload_bull_market_issue(access_token, repository_name,body):
    repo = get_github_repo(access_token,repository_name)
    title = get_title()
    upload_github_issue(repo,title, body)