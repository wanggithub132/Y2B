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
    # Google表格密钥
    google_json = get_gist("029980c14a62bd183c3f759e1013633e", "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")
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
    rows = sheet.get_all_values()
    # print(data_list)
    # 获取第一行数据,确认索引位置
    tab_list = rows[0]
    title_index = tab_list.index("标题")
    video_index = tab_list.index("视频链接")
    video_time_index = tab_list.index("视频时常")
    img_index = tab_list.index("缩略图")
    upload_flag_index = tab_list.index("是否已处理")
    # 构建所需对象
    bean_list = []
    for i, row in enumerate(rows):
        # print("入口",i,row)
        if i == 0:
            continue
        flag = row[upload_flag_index]
        print("flag", flag)
        # 判断数据合法性
        if type(flag) != int:
            continue
            # 判断数据是否已经解析过
        if flag == 1:
            continue
        print(i,row)
        detail = {
            "vid": row[video_index],
            "title": row[title_index],
            "origin": row[video_index],
            "cover_url": row[img_index],
            "tag": "暂时没有"
        }
        bean = {"detail": detail}
        bean_list.append(bean)
        # 更改数据解析标志位

    print(bean_list)


        # 将第一列数据设置为行号，第二列数据设置为新值
        # sheet.update_cell(i + 1, 1, i + 1)
        # sheet.update_cell(i + 1, 2, 'new value')


    # 数据转换成原来上传的形式
# 上传后标记数据，是否已处理字段标记为1，默认为0
# 写入数据
# new_row = ['John', 'Doe', '31']
# sheet.append_row(new_row)

# {
# 'detail': {'vid': 'IRWP1hnS05I', 'title': '如何一拳KO對手 ', 'origin': 'https://www.youtube.com/watch?v=IRWP1hnS05I', 'cover_url': 'https://i2.ytimg.com/vi/IRWP1hnS05I/hqdefault.jpg', 'tag': ['shorts']},
# 'config': {'channel_id': 'UCXdSUUf401UmRw0A9Tt0veQ', 'tid': 238, 'tags': '拳击,教学,Tony Jeffries Mandarin,健身,shorts'}
# }

