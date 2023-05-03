import json
import os

import gspread
import requests
from oauth2client.service_account import ServiceAccountCredentials

VERIFY = os.environ.get("verify", "1") == "1"
PROXY = {
    "https": os.environ.get("https_proxy", None)
}
GOOGLE_FILE = "google_credentials.json"
SHEET_ID = "1u-f9CEMoxQoTK6Beix_4YlmtczlnFJWeQab326LABy0"


def get_gist(_gid, token):
    """通过 gist id 获取已上传数据"""
    rsp = requests.get(
        "https://api.github.com/gists/" + _gid,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer " + token,
        },
        verify=VERIFY,
    )
    if rsp.status_code == 404:
        raise Exception("gist id 错误")
    if rsp.status_code == 403 or rsp.status_code == 401:
        raise Exception("github TOKEN 错误")
    _data = rsp.json()
    g_json = json.loads(_data["files"][GOOGLE_FILE]["content"])
    return g_json


'''
从gist上拉取Google表格密钥->完成Google认证->获取远端表格
json做临时缓存，认证后删除
'''


def get_sheet_from_google():
    # 从远端拉取Google表格密钥
    google_json = get_gist("id", "token")
    # Google认证
    # 服务器认证
    creds = ServiceAccountCredentials.from_json_keyfile_dict(google_json)
    # 本地认证
    # creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)

    # 通过 ID 打开指定的 Google Sheets 文件
    return client.open_by_key(SHEET_ID).sheet1


if __name__ == '__main__':
    # 通过 ID 打开指定的 Google Sheets 文件
    sheet = get_sheet_from_google()

    # 读取整张表格的内容
    data = sheet.get_all_values()
    print(data)

    # 数据转换成原来上传的形式
# 上传后标记数据，是否已处理字段标记为1，默认为0
# 写入数据
# new_row = ['John', 'Doe', '31']
# sheet.append_row(new_row)
