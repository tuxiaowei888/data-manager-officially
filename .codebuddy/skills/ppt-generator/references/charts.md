# Chart Examples for PPT

如何在 PPT 中添加各种图表。

## 安装依赖

```bash
pip install python-pptx matplotlib pandas
```

## 柱状图

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE

def add_bar_chart(slide, left, top, width, height, categories, values, title=''):
    chart_data = CategoryChartData()
    chart_data.categories = categories
    chart_data.add_series('Series 1', values)
    
    chart = slide.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED,
        left, top, width, height,
        chart_data
    ).chart
    
    if title:
        chart.has_title = True
        chart.chart_title.text_frame.paragraphs[0].text = title
    
    return chart

slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bar_chart(
    slide,
    Inches(1), Inches(1.5), Inches(5), Inches(4),
    ['Q1', 'Q2', 'Q3', 'Q4'],
    [120, 150, 180, 200],
    '季度销售额'
)
```

## 折线图

```python
def add_line_chart(slide, left, top, width, height, categories, series_data, title=''):
    chart_data = CategoryChartData()
    chart_data.categories = categories
    
    for series_name, values in series_data.items():
        chart_data.add_series(series_name, values)
    
    chart = slide.shapes.add_chart(
        XL_CHART_TYPE.LINE,
        left, top, width, height,
        chart_data
    ).chart
    
    if title:
        chart.has_title = True
        chart.chart_title.text_frame.paragraphs[0].text = title
    
    return chart

add_line_chart(
    slide,
    Inches(1), Inches(1.5), Inches(5), Inches(4),
    ['1月', '2月', '3月', '4月', '5月', '6月'],
    {
        '产品A': [10, 15, 12, 18, 22, 25],
        '产品B': [8, 12, 15, 14, 18, 20]
    },
    '月度趋势'
)
```

## 饼图

```python
def add_pie_chart(slide, left, top, width, height, categories, values, title=''):
    chart_data = CategoryChartData()
    chart_data.categories = categories
    chart_data.add_series('Series', values)
    
    chart = slide.shapes.add_chart(
        XL_CHART_TYPE.PIE,
        left, top, width, height,
        chart_data
    ).chart
    
    if title:
        chart.has_title = True
        chart.chart_title.text_frame.paragraphs[0].text = title
    
    chart.plots[0].has_data_labels = True
    
    return chart

add_pie_chart(
    slide,
    Inches(1), Inches(1.5), Inches(5), Inches(4),
    ['直接销售', '渠道销售', '线上销售', '其他'],
    [40, 30, 25, 5],
    '销售渠道分布'
)
```

## 使用 Matplotlib 生成高级图表

```python
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def add_matplotlib_chart(slide, chart_func, left, top, width, height, **kwargs):
    fig, ax = plt.subplots(figsize=(8, 5))
    chart_func(ax, **kwargs)
    
    img_path = '_temp_chart.png'
    fig.savefig(img_path, dpi=150, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close(fig)
    
    slide.shapes.add_picture(img_path, left, top, width, height)
    
    import os
    os.remove(img_path)

def grouped_bar_chart(ax, categories, data, colors=None):
    import numpy as np
    x = np.arange(len(categories))
    width = 0.35
    
    for i, (label, values) in enumerate(data.items()):
        offset = width * i
        bars = ax.bar(x + offset, values, width, label=label)
        if colors:
            bars[0].set_color(colors[i % len(colors)])
    
    ax.set_xticks(x + width / 2)
    ax.set_xticklabels(categories)
    ax.legend()

add_matplotlib_chart(
    slide,
    grouped_bar_chart,
    Inches(1), Inches(1.5), Inches(6), Inches(4),
    categories=['Q1', 'Q2', 'Q3', 'Q4'],
    data={
        '2023': [100, 120, 140, 160],
        '2024': [130, 150, 170, 190]
    },
    colors=['#005293', '#007BC2']
)
```

## 数据表格

```python
def add_data_table(slide, left, top, width, height, headers, rows):
    table = slide.shapes.add_table(
        len(rows) + 1, len(headers),
        left, top, width, height
    ).table
    
    for i, header in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = header
        cell.text_frame.paragraphs[0].font.bold = True
        cell.text_frame.paragraphs[0].font.size = Pt(12)
    
    for row_idx, row_data in enumerate(rows):
        for col_idx, cell_data in enumerate(row_data):
            cell = table.cell(row_idx + 1, col_idx)
            cell.text = str(cell_data)
            cell.text_frame.paragraphs[0].font.size = Pt(11)
    
    return table

add_data_table(
    slide,
    Inches(1), Inches(1.5), Inches(10), Inches(3),
    ['项目', 'Q1', 'Q2', 'Q3', 'Q4'],
    [
        ['销售额', '100万', '120万', '140万', '160万'],
        ['利润', '20万', '25万', '30万', '35万'],
        ['增长率', '10%', '20%', '17%', '14%']
    ]
)
```

## 完整示例：数据报告幻灯片

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.dml.color import RgbColor

def create_data_report_slide(prs, title, data):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    title_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(0.3), Inches(12.333), Inches(0.8)
    )
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = RgbColor(0, 82, 147)
    
    add_bar_chart(
        slide,
        Inches(0.5), Inches(1.5), Inches(5.5), Inches(4),
        ['Q1', 'Q2', 'Q3', 'Q4'],
        [120, 150, 180, 200],
        '季度销售额'
    )
    
    add_pie_chart(
        slide,
        Inches(6.5), Inches(1.5), Inches(5.5), Inches(4),
        ['线上', '线下', '渠道'],
        [45, 35, 20],
        '销售渠道'
    )
    
    add_data_table(
        slide,
        Inches(0.5), Inches(5.8), Inches(11.5), Inches(1.2),
        ['指标', 'Q1', 'Q2', 'Q3', 'Q4'],
        [
            ['收入', '100万', '120万', '140万', '160万'],
            ['利润', '40万', '50万', '60万', '70万']
        ]
    )
    
    return slide

if __name__ == '__main__':
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    create_data_report_slide(prs, '2024年度数据分析', {})
    
    prs.save('data_report.pptx')
    print("数据报告已生成: data_report.pptx")
```

## 图表样式定制

```python
def style_chart(chart, color_scheme='blue'):
    colors = {
        'blue': ['005293', '007BC2', '00A3E0', '7DC8E8'],
        'green': ['2E8B57', '3CB371', '90EE90', '98FB98'],
        'red': ['DC143C', 'FF6347', 'FF7F50', 'FFA07A']
    }
    
    scheme = colors.get(color_scheme, colors['blue'])
    
    plot = chart.plots[0]
    for i, series in enumerate(plot.series):
        color_hex = scheme[i % len(scheme)]
        series.format.fill.solid()
        series.format.fill.fore_color.rgb = RgbColor(
            int(color_hex[0:2], 16),
            int(color_hex[2:4], 16),
            int(color_hex[4:6], 16)
        )
    
    return chart
```
