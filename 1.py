import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import jieba
from collections import Counter
from pyecharts import options as opts
from pyecharts.charts import Bar, Pie, Line, Scatter, Radar, Kline, WordCloud
from pyecharts.commons.utils import JsCode
import chardet  # 导入chardet库用于自动检测编码

# 创建一个文本输入框
url = st.sidebar.text_input("请输入文章URL", "")

# 获取文本内容
def fetch_text_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        # 使用chardet检测编码
        encoding = chardet.detect(response.content)['encoding']
        # 根据检测到的编码解码内容
        return response.content.decode(encoding)
    else:
        return "无法获取内容，URL可能不正确或服务器返回了错误状态码。"

# 使用正则表达式去除HTML标签
def remove_html_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

# 去除文本中的标点符号
def remove_punctuation(text):
    return re.sub(r'[^\w\s]', '', text)

# 对文本进行分词
def segment_text(text):
    words = jieba.cut(text)
    return ' '.join(words)

# 统计词频
def count_word_frequency(words):
    return Counter(words.split())

# 处理文本，包括去除HTML标签和标点符号
def process_text(text):
    text = remove_html_tags(text)
    text = remove_punctuation(text)
    return text

# 分词并统计词频
def tokenize_and_count(text):
    processed_text = process_text(text)
    segmented_text = segment_text(processed_text)
    return count_word_frequency(segmented_text)

# 使用pyecharts绘制词云
def create_wordcloud(word_counts):
    wordcloud = WordCloud()
    wordcloud.add("", list(word_counts.items()), word_size_range=[20, 100])
    wordcloud.set_global_opts(title_opts=opts.TitleOpts(title="词云"))
    return wordcloud

# 使用pyecharts绘制柱状图
def create_bar_chart(word_counts):
    bar = Bar()
    bar.add_xaxis(list(word_counts.keys()))
    bar.add_yaxis("词频", list(word_counts.values()))
    bar.set_global_opts(title_opts=opts.TitleOpts(title="柱状图"))
    return bar

# 使用pyecharts绘制饼图
def create_pie_chart(word_counts):
    pie = Pie()
    pie.add("", [list(z) for z in zip(word_counts.keys(), word_counts.values())])
    pie.set_global_opts(title_opts=opts.TitleOpts(title="饼图"))
    pie.set_series_opts(label_opts=opts.LabelOpts(formatter=JsCode("function(params){return params.name + ': ' + params.value}")))
    return pie

# 使用pyecharts绘制折线图
def create_line_chart(word_counts):
    line = Line()
    line.add_xaxis(list(word_counts.keys()))
    line.add_yaxis("词频", list(word_counts.values()))
    line.set_global_opts(title_opts=opts.TitleOpts(title="折线图"))
    return line

# 使用pyecharts绘制散点图
def create_scatter_chart(word_counts):
    scatter = Scatter()
    scatter.add_xaxis(list(word_counts.keys()))
    scatter.add_yaxis("词频", list(word_counts.values()))
    scatter.set_global_opts(title_opts=opts.TitleOpts(title="散点图"))
    return scatter

# 使用pyecharts绘制雷达图
def create_radar_chart(word_counts):
    radar = Radar()
    radar.add_schema(schema=[opts.RadarItem(name=key, max_=max(value, 10)) for key, value in word_counts.items()])
    radar.add("", [list(value) for value in zip(*word_counts.values())])
    radar.set_global_opts(title_opts=opts.TitleOpts(title="雷达图"))
    return radar

# 使用pyecharts绘制K线图
def create_kline_chart(word_counts):
    kline = Kline()
    kline.add_xaxis(list(word_counts.keys()))
    kline.add_yaxis("词频", list(word_counts.values()))
    kline.set_global_opts(title_opts=opts.TitleOpts(title="K线图"))
    return kline

# 获取网页内容并在网页中显示
content = fetch_text_from_url(url) if url else ""
#st.write("获取的内容如下：")
#st.write(content)

# 处理文本并统计词频
word_counts = tokenize_and_count(content) if content else Counter()

# 选择图表类型
chart_type = st.sidebar.selectbox("选择图表类型", ["词云", "柱状图", "饼图", "折线图", "散点图", "雷达图", "K线图"])

# 过滤低频词
min_freq = st.sidebar.slider("设置最低词频阈值", 1, 100, 10)
filtered_word_counts = {word: count for word, count in word_counts.items() if count >= min_freq}
filtered_word_counts = Counter(filtered_word_counts)  # 转换为Counter对象

# 展示词频排名前20的词汇
top_words = filtered_word_counts.most_common(20)
st.write("词频排名前20的词汇：")
st.table(top_words)  # 使用Streamlit的table组件来显示排名列表

# 根据选择的图表类型展示不同的图表
if chart_type == "词云":
    # 将Pyecharts图表转换为HTML
    wordcloud = create_wordcloud(filtered_word_counts)
    html_content = wordcloud.render_embed()
    # 使用Streamlit的html组件来显示Pyecharts图表
    st.components.v1.html(html_content, height=600)  # 修改height参数为数值\
elif chart_type == "柱状图":
    bar_chart = create_bar_chart(filtered_word_counts)
    html_content = bar_chart.render_embed()
    st.components.v1.html(html_content, height=600)
elif chart_type == "饼图":
    pie_chart = create_pie_chart(filtered_word_counts)
    html_content = pie_chart.render_embed()
    st.components.v1.html(html_content, height=600)
elif chart_type == "折线图":
    line_chart = create_line_chart(filtered_word_counts)
    html_content = line_chart.render_embed()
    st.components.v1.html(html_content, height=600)
elif chart_type == "散点图":
    scatter_chart = create_scatter_chart(filtered_word_counts)
    html_content = scatter_chart.render_embed()
    st.components.v1.html(html_content, height=600)
elif chart_type == "雷达图":
    radar_chart = create_radar_chart(filtered_word_counts)
    html_content = radar_chart.render_embed()
    st.components.v1.html(html_content, height=600)
elif chart_type == "K线图":
    kline_chart = create_kline_chart(filtered_word_counts)
    html_content = kline_chart.render_embed()
    st.components.v1.html(html_content, height=600)
