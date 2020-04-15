# 读取数据
import pandas as pd
world_data = pd.read_csv('today_world_2020_04_03.csv')
import pyecharts
# 调整配置项
import pyecharts.options as opts
# Map类用于绘制地图
from pyecharts.charts import Map

#饼图绘制包
from pyecharts.charts import Pie

###############用于生成静态图#################
from pyecharts.render import make_snapshot
# 使用snapshot-selenium 渲染图片
from snapshot_selenium import snapshot
############################################

#接下来使用datetime模块生成时间数据，构造时间列表；用于例四，3月世界国家累计确诊人数动态条形图
from datetime import datetime,timedelta

#载入Matplotlib库，并设置正常显示中文字体；用于例四，3月世界国家累计确诊人数动态条形图
import matplotlib.pyplot as plt
#用于ipython设置动态显示 %matplotlib inline

#定义绘图函数；用于例四，3月世界国家累计确诊人数动态条形图
import matplotlib.ticker as ticker

#绘图；用于例四，3月世界国家累计确诊人数动态条形图
import matplotlib.animation as animation
from IPython.display import HTML

#确定现存确诊
world_data['today_storeConfirm'] = world_data['total_confirm'] - world_data['total_heal'] - world_data['total_dead']
print(world_data.head())

#导入国家名中英文对照集
contry_name = pd.read_csv('county_china_english.csv', encoding='GB2312')
print(contry_name.head())

#将数据世界数据的中文名换成英文
world_data['eg_name'] = world_data['name'].replace(contry_name['中文'].values ,contry_name['英文'].values)
print(world_data['eg_name'].head())

#将国家和现存人数转换成一个矩阵（嵌套列表）
heatmap_data = world_data[['eg_name','today_storeConfirm']].values.tolist()
print(heatmap_data[:10])

'''
#开始绘图准备
map_ = Map().add(series_name = "现存确诊人数", # 设置提示框标签
                 data_pair = heatmap_data, # 输入数据
                 maptype = "world", # 设置地图类型为世界地图
                 is_map_symbol_show = False # 不显示标记点
                )
# 设置系列配置项
map_.set_series_opts(label_opts=opts.LabelOpts(is_show=False))  # 不显示国家（标签）名称
# 设置全局配置项
map_.set_global_opts(title_opts = opts.TitleOpts(title="世界各国家现存确诊人数地图"), # 设置图标题
                     # 设置视觉映射配置项
                     visualmap_opts = opts.VisualMapOpts(pieces=[ # 自定义分组的分点和颜色
                                                               {"min": 10000,"color":"#800000"}, # 栗色
                                                               {"min": 5000, "max": 9999, "color":"#B22222"}, # 耐火砖
                                                               {"min": 999, "max": 4999,"color":"#CD5C5C"}, # 印度红
                                                               {"min": 100, "max": 999, "color":"#BC8F8F"}, # 玫瑰棕色
                                                               {"max": 99, "color":"#FFE4E1"}, # 薄雾玫瑰
                                                              ],
                     is_piecewise = True))  # 显示分段式图例

# 在notebook中进行渲染(生成动态图)
map_.render_notebook()

#直接在指定位置输出静态图
make_snapshot(snapshot, map_.render(), r"F:\COVID-19\pic1.png")
'''

'''
##################玫瑰图###########################
#首先筛选出累计死亡人数超过500人的世界国家，并按人数进行降序排序
need_data = world_data[['name','total_dead']][world_data['total_dead'] >500]
rank = need_data[['name','total_dead']].sort_values(by='total_dead',ascending=False).values

#基本配置信息
pie = Pie().add("累计死亡人数", # 添加提示框标签
                rank, # 输入数据
                radius = ["20%", "80%"],  # 设置内半径和外半径
                center = ["60%", "60%"],  # 设置圆心位置
                rosetype = "radius")   # 玫瑰图模式，通过半径区分数值大小，角度大小表示占比
#全局和系列配置信息
pie.set_global_opts(title_opts = opts.TitleOpts(title="世界国家累计死亡人数玫瑰图",  # 设置图标题
                                                pos_right = '40%'),  # 图标题的位置
                    legend_opts = opts.LegendOpts( # 设置图例
                                                orient='vertical', # 垂直放置图例
                                                pos_right="85%", # 设置图例位置
                                                pos_top="15%"))

pie.set_series_opts(label_opts = opts.LabelOpts(formatter="{b} : {d}%")) # 设置标签文字形式为（国家：占比（%））

# 在notebook中进行渲染
pie.render_notebook()

#直接在指定位置输出静态图
make_snapshot(snapshot, pie.render(), r"F:\COVID-19\pic2.png")
'''


#3月美国单日新增确诊人数与股票指数涨跌幅折线图
#先读取股指数据
stock = pd.read_csv('stockindex.csv',encoding='GB2312')
print(stock)
#读取全球疫情历史数据
alltime_data = pd.read_csv('alltime_world_2020_04_04.csv')
'''
#筛选出与股票开盘日期对应的美国单日新增确诊人数：
import warnings
warnings.filterwarnings('ignore')
alltime_us = alltime_data[alltime_data['name'] == '美国']
#print(alltime_us)
use_data = alltime_us[alltime_data['date'].isin(stock['日期'].values)][['date','today_confirm']]
#print(use_data)


#导入绘制折线图的Line类和绘制组合图形的Grid类：
from pyecharts.charts import Line, Grid
#定义美国单日新增确诊人数折线图的相关设置
l1 = Line().add_xaxis(# 配置x轴
                      xaxis_data = use_data['date'].values   # 输入x轴数据
                      )

l1.add_yaxis(# 配置y轴
             series_name = "单日新增人数",  # 设置图例名称
             y_axis = use_data['today_confirm'].values.tolist(),  # 输入y轴数据
             symbol_size = 10, # 设置点的大小
             label_opts = opts.LabelOpts(is_show=False), # 标签设置项：显示标签
             linestyle_opts = opts.LineStyleOpts(width=1.5, type_='dotted'), # 线条宽度和样式
             is_smooth = True, # 绘制平滑曲线
             )

# 设置全局配置项
l1.set_global_opts(title_opts = opts.TitleOpts(title = "3月美国单日新增人数与股票指数涨幅对比折线图",
                                               pos_left = "center"), # 设置图标题和位置
                   axispointer_opts = opts.AxisPointerOpts(is_show = True,
                                                           link = [{"xAxisIndex": "all"}]),  # 坐标轴指示器配置
                   # x轴配置项
                   xaxis_opts = opts.AxisOpts(type_ = "category",
                                              boundary_gap = True), # 坐标轴两边是否留白
                   # y轴配置项
                   yaxis_opts = opts.AxisOpts(name = "单日新增人数"), # 轴标题
                   # 图例配置项
                   legend_opts = opts.LegendOpts(pos_left  ='7%') # 图例的位置
                   )


#定义三支股票指数变化的折线图设置：
l2 = Line().add_xaxis(xaxis_data = use_data['date'].values)

l2.add_yaxis(series_name = "上证指数",
             y_axis = stock['SSEC'].values,  # 添加上证指数数据
             symbol_size = 10,
             label_opts = opts.LabelOpts(is_show = False),
             linestyle_opts = opts.LineStyleOpts(width = 1.5), # 设置线宽
             is_smooth = True)

l2.add_yaxis(series_name = "日经225指数",
             y_axis = stock['N225'].values,  # 添加日经225指数数据
             symbol_size = 10,
             label_opts = opts.LabelOpts(is_show = False),
             linestyle_opts = opts.LineStyleOpts(width = 1.5),
             is_smooth = True)

l2.add_yaxis(series_name = "纳斯达克综合指数",
             y_axis = stock['NASDAQ'].values, # 添加纳斯达克综合指数数据
             symbol_size = 10,
             label_opts = opts.LabelOpts(is_show = False),
             linestyle_opts = opts.LineStyleOpts(width = 1.5),
             is_smooth = True)

l2.set_global_opts(axispointer_opts = opts.AxisPointerOpts(  # 设置坐标轴指示器
                                                           is_show = True,
                                                           link = [{"xAxisIndex": "all"}]),  # 对x轴所有索引进行联动

                   xaxis_opts = opts.AxisOpts(grid_index = 1,  # x轴开始的索引
                                             type_ = "category", # 类型
                                             boundary_gap = True,
                                             position = "top", # 坐标轴位置
                                             axisline_opts = opts.AxisLineOpts(is_on_zero=True)),  # x轴或y轴的轴线是否在另一个轴的0刻度上

                   yaxis_opts = opts.AxisOpts(is_inverse = False, name = "涨跌幅（%）",name_gap = 25), # 轴线设置
                   legend_opts = opts.LegendOpts(pos_bottom = '50%',pos_right = '70') # 图例设置
                   )


#将两幅图按照上下位置进行组合：
# 绘制组合图形
grid = Grid(init_opts = opts.InitOpts(width = "1024px", height = "768px")) # 设置图形的长和宽

grid.add(chart=l1,  # 添加第一个图表
         grid_opts = opts.GridOpts(pos_left = 50, pos_right = 50, height = "35%"))  # 直角坐标系网格配置项

grid.add(chart = l2, # 添加第二个图表
         grid_opts = opts.GridOpts(pos_left = 50, pos_right = 50, pos_top = "55%", height = "35%"))

# 利用notebook进行渲染
grid.render_notebook()

make_snapshot(snapshot,grid.render(), r"F:\COVID-19\pic3.png")
'''

#3月世界国家累计确诊人数动态条形图
#首先挑选出疫情最为严重的10个国家，并筛选出这些国家的历史疫情数据：
country_list = ['美国', '意大利', '中国', '西班牙', '德国', '伊朗', '法国', '英国', '瑞士','比利时']
need_data = alltime_data[alltime_data['name'].isin(country_list)]

#构造时间列表
time_list = [(datetime(2020, 3, 1) + timedelta(i)).strftime('%Y-%m-%d') for i in range(31)]

#并设置正常显示中文字体：
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['figure.dpi'] = 100

#为每个国家设置一种颜色：
color_list = ['brown','peru','orange','blue','green',
              'red','yellow','teal','pink','orchid']
country_color = pd.DataFrame()
country_color['country'] = country_list
country_color['color'] = color_list


#定义绘图函数
def barh_draw(day):
    # 提取每一天的数据
    draw_data = need_data[need_data['date'] == day][['name', 'total_confirm']].sort_values(by='total_confirm',
                                                                                           ascending=True)

    # 清空当前的绘图
    ax.clear()

    # 绘制条形图
    ax.barh(draw_data['name'], draw_data['total_confirm'],
            color=[country_color[country_color['country'] == i]['color'].values[0] for i in draw_data['name']])

    # 数值标签的间距
    dx = draw_data['total_confirm'].max() / 200

    # 添加数值标签
    for j, (name, value) in enumerate(zip(draw_data['name'], draw_data['total_confirm'])):
        ax.text(value + dx, j, f'{value:,.0f}', size=10, ha='left', va='center')

    # 添加日期标签
    ax.text(draw_data['total_confirm'].max() * 0.75, 0.4, day, color='#777777', size=40, ha='left')

    # 设置刻度标签的格式
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))

    # 设置刻度的位置
    ax.xaxis.set_ticks_position('top')

    # 设置刻度标签的颜色和大小
    ax.tick_params(axis='x', colors='#777777', labelsize=15)

    # 添加网格线
    ax.grid(which='major', axis='x', linestyle='-')

    # 添加图标题
    ax.text(0, 11, '3月世界各国家累计确诊人数动态条形图', size=20, ha='left')

    # 去除图边框
    plt.box(False)

    # 关闭绘图框
    plt.close()

#动态绘图
fig, ax = plt.subplots(figsize=(12, 8))
animator = animation.FuncAnimation(fig, barh_draw, frames=time_list, interval=200)
HTML(animator.to_jshtml())






















