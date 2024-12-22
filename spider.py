from requests import get
from re import search
from urllib.parse import unquote
from json import load, loads, dump
from objprint import op

FOLDER = "./cf_on_luogu"
PROBLEM_PER_PAGE = 50

def get_luogu_problem(page, retry = 5):
    try:
        content = get(
            f"https://www.luogu.com.cn/problem/list?type=CF&page={page}",
            headers = {
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:65.0) Gecko/20100101 Firefox/65.0"
            }
        ).content.decode()

        obj = loads(unquote(
            search(r"JSON\.parse\(decodeURIComponent\(\"(.*)\"\)\)", content).group(1)
        ))['currentData']['problems']['result']
        # op(content)
        return obj
    except KeyboardInterrupt:
        raise KeyboardInterrupt
    except:
        print(f"get {page} failed, retry = {retry}")
        if not retry:
            return ["error!"]
        else:
            return get_luogu_problem(page, retry-1)

def has_download(page):
    try:
        obj = load(open(f"{FOLDER}/page_{page}.json", "r"))
        return len(obj) == PROBLEM_PER_PAGE
    except:
        return False

page = 1

while True:
    if not has_download(page):
        obj = get_luogu_problem(page)
        if len(obj) != PROBLEM_PER_PAGE:
            break
        dump(obj, open(f"{FOLDER}/page_{page}.json", "w"))
        print(f"get page {page}.")
    else:
        print(f"page {page} cached.")
    page += 1