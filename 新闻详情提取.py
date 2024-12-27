import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


# 新闻列表页面的URL
NEWS_LIST_URL = 'https://chinaus-maker.cscse.edu.cn/chinaus-maker/dsxw90/index.html'  # 请替换为实际的URL

# 发送GET请求获取新闻列表页面的内容
response = requests.get(NEWS_LIST_URL)

# 检查响应状态码
if response.status_code == 200:
    # 尝试使用网站指定的编码，通常是UTF-8
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找所有的新闻条目
    news_items = soup.find_all('div', class_='box clearfix')

    # 控制生成文档的数量
    max_documents = 3
    document_count = 0

    # 存储新闻信息
    for item in news_items:
        if document_count >= max_documents:
            break  # 达到最大文档数量，停止处理

        # 提取标题和链接
        title_tag = item.find('p', class_='title').find('a')
        title = title_tag.text.strip() if title_tag else '无标题'
        relative_link = title_tag['href'] if title_tag and title_tag.has_attr('href') else '#'

        # 将相对链接转换为绝对链接
        link = urljoin(NEWS_LIST_URL, relative_link)
        print(link)

        # 访问新闻详情页面
        detail_response = requests.get(link)
        if detail_response.status_code == 200:
            detail_response.encoding = 'utf-8'
            detail_soup = BeautifulSoup(detail_response.text, 'html.parser')

            # 提取新闻内容
            content_div = detail_soup.find('div', class_='wzZW') .find('p') # 根据实际的class名称调整
            content = content_div.text.strip() if content_div else '无内容'

            print(content_div)

            保存为txt文件
            file_name = f"{title}.txt"  # 从标题生成文件名
            with open(file_name, 'w', encoding='utf-8') as file:
               file.write(content)

            print(f"新闻 '{title}' 的详情已保存为 '{file_name}'")
            document_count += 1  # 增加文档计数
        else:
            print(f"无法获取新闻详情页面: {link}")
else:
    print(f"请求新闻列表页面失败，状态码：{response.status_code}")