from bs4 import BeautifulSoup

import workbook_util


# 需要解析的内容 title 视频链接 封面图 视频时常
def get_video_list(video_soup):
    div_list = video_soup.find_all("div", id="contents", class_="style-scope ytd-rich-grid-row")
    v_list = []

    for tag in div_list:
        v_bean = {}
        title = tag.find("yt-formatted-string", id="video-title")
        video_url = tag.find("a", id="video-title-link")
        video_time = tag.find("span", id="text", class_="style-scope ytd-thumbnail-overlay-time-status-renderer")
        img = tag.find("img",
                       class_="yt-core-image--fill-parent-height yt-core-image--fill-parent-width yt-core-image yt-core-image--content-mode-scale-aspect-fill yt-core-image--loaded")
        if img is not None:
            img_src = img.get("src")
        else:
            img_src = "空"
        v_bean["标题"] = title.text
        v_bean["视频链接"] = video_url.get("href")
        v_bean["视频时常"] = video_time.text.strip()
        v_bean["缩略图"] = img_src
        print(v_bean)
        v_list.append(v_bean)
    return v_list


if __name__ == '__main__':
    # 使用 BeautifulSoup解析网络请求数据，这个工具是保存在电脑本地的，生成的表格信息，到时候手动拷贝到远端表格即可
    with open('test.html', 'r', encoding="utf-8") as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    video_list = get_video_list(soup)
    workbook_util.write_to_excel(video_list, "youtobe.xlsx")

