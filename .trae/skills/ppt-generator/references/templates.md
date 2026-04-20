# PPT Templates Reference

Complete templates for common presentation types.

## Template 1: Title Slide

```python
def create_title_slide(prs, title, subtitle='', author='', date=''):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    title_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(2.5), Inches(12.333), Inches(1.5)
    )
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(54)
    p.font.bold = True
    p.font.color.rgb = RgbColor(0, 82, 147)
    p.alignment = PP_ALIGN.CENTER
    
    if subtitle:
        sub_box = slide.shapes.add_textbox(
            Inches(0.5), Inches(4.2), Inches(12.333), Inches(0.8)
        )
        tf = sub_box.text_frame
        p = tf.paragraphs[0]
        p.text = subtitle
        p.font.size = Pt(28)
        p.font.color.rgb = RgbColor(100, 100, 100)
        p.alignment = PP_ALIGN.CENTER
    
    if author:
        author_box = slide.shapes.add_textbox(
            Inches(0.5), Inches(5.5), Inches(12.333), Inches(0.5)
        )
        tf = author_box.text_frame
        p = tf.paragraphs[0]
        p.text = f"{author} | {date}"
        p.font.size = Pt(16)
        p.font.color.rgb = RgbColor(150, 150, 150)
        p.alignment = PP_ALIGN.CENTER
    
    return slide
```

## Template 2: Content Slide with Bullets

```python
def create_bullet_slide(prs, title, bullets, icon_color=None):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    title_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(0.5), Inches(12.333), Inches(1)
    )
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RgbColor(0, 82, 147)
    
    content_box = slide.shapes.add_textbox(
        Inches(0.8), Inches(1.8), Inches(11.733), Inches(5)
    )
    tf = content_box.text_frame
    tf.word_wrap = True
    
    for i, bullet in enumerate(bullets):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        
        if isinstance(bullet, dict):
            p.text = f"● {bullet['text']}"
            p.font.size = Pt(bullet.get('size', 24))
            if bullet.get('highlight'):
                p.font.color.rgb = RgbColor(0, 123, 194)
            else:
                p.font.color.rgb = RgbColor(51, 51, 51)
        else:
            p.text = f"● {bullet}"
            p.font.size = Pt(24)
            p.font.color.rgb = RgbColor(51, 51, 51)
        
        p.space_after = Pt(16)
    
    return slide
```

## Template 3: Two Column Layout

```python
def create_two_column_slide(prs, title, left_content, right_content):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    title_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(0.5), Inches(12.333), Inches(1)
    )
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RgbColor(0, 82, 147)
    
    left_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(1.8), Inches(5.9), Inches(5)
    )
    tf = left_box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(left_content):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = f"● {item}"
        p.font.size = Pt(20)
        p.space_after = Pt(12)
    
    right_box = slide.shapes.add_textbox(
        Inches(6.9), Inches(1.8), Inches(5.9), Inches(5)
    )
    tf = right_box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(right_content):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = f"● {item}"
        p.font.size = Pt(20)
        p.space_after = Pt(12)
    
    return slide
```

## Template 4: Image with Text

```python
def create_image_text_slide(prs, title, image_path, text_items, image_left=True):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    title_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(0.5), Inches(12.333), Inches(1)
    )
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RgbColor(0, 82, 147)
    
    if image_left:
        img_left, img_top = Inches(0.5), Inches(1.8)
        text_left = Inches(6.5)
    else:
        img_left, img_top = Inches(6.5), Inches(1.8)
        text_left = Inches(0.5)
    
    slide.shapes.add_picture(image_path, img_left, img_top, width=Inches(5.8))
    
    text_box = slide.shapes.add_textbox(
        text_left, Inches(1.8), Inches(5.8), Inches(5)
    )
    tf = text_box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(text_items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = f"● {item}"
        p.font.size = Pt(20)
        p.space_after = Pt(12)
    
    return slide
```

## Template 5: Data/Stats Slide

```python
def create_stats_slide(prs, title, stats):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    title_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(0.5), Inches(12.333), Inches(1)
    )
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RgbColor(0, 82, 147)
    
    num_stats = len(stats)
    box_width = 12.333 / num_stats
    
    for i, stat in enumerate(stats):
        stat_box = slide.shapes.add_textbox(
            Inches(0.5 + i * box_width), Inches(2.5), Inches(box_width - 0.3), Inches(3)
        )
        tf = stat_box.text_frame
        
        p = tf.paragraphs[0]
        p.text = stat['value']
        p.font.size = Pt(48)
        p.font.bold = True
        p.font.color.rgb = RgbColor(0, 123, 194)
        p.alignment = PP_ALIGN.CENTER
        
        p = tf.add_paragraph()
        p.text = stat['label']
        p.font.size = Pt(18)
        p.font.color.rgb = RgbColor(100, 100, 100)
        p.alignment = PP_ALIGN.CENTER
    
    return slide
```

## Template 6: Timeline Slide

```python
def create_timeline_slide(prs, title, events):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    title_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(0.5), Inches(12.333), Inches(1)
    )
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RgbColor(0, 82, 147)
    
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0.5), Inches(3.5), Inches(12.333), Inches(0.05)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = RgbColor(0, 82, 147)
    line.line.fill.background()
    
    num_events = len(events)
    spacing = 12.333 / (num_events + 1)
    
    for i, event in enumerate(events):
        x_pos = Inches(0.5 + (i + 1) * spacing)
        
        dot = slide.shapes.add_shape(
            MSO_SHAPE.OVAL,
            x_pos - Inches(0.1), Inches(3.4), Inches(0.2), Inches(0.2)
        )
        dot.fill.solid()
        dot.fill.fore_color.rgb = RgbColor(0, 123, 194)
        dot.line.fill.background()
        
        date_box = slide.shapes.add_textbox(
            x_pos - Inches(0.5), Inches(2.8), Inches(1), Inches(0.5)
        )
        tf = date_box.text_frame
        p = tf.paragraphs[0]
        p.text = event['date']
        p.font.size = Pt(14)
        p.font.bold = True
        p.alignment = PP_ALIGN.CENTER
        
        desc_box = slide.shapes.add_textbox(
            x_pos - Inches(0.8), Inches(3.8), Inches(1.6), Inches(2)
        )
        tf = desc_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = event['description']
        p.font.size = Pt(12)
        p.alignment = PP_ALIGN.CENTER
    
    return slide
```

## Template 7: Comparison Table

```python
def create_comparison_slide(prs, title, headers, rows):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    title_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(0.5), Inches(12.333), Inches(1)
    )
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RgbColor(0, 82, 147)
    
    num_cols = len(headers)
    num_rows = len(rows) + 1
    col_width = 12.333 / num_cols
    row_height = 5.5 / num_rows
    
    for col_idx, header in enumerate(headers):
        cell = slide.shapes.add_textbox(
            Inches(0.5 + col_idx * col_width),
            Inches(1.5),
            Inches(col_width),
            Inches(row_height)
        )
        tf = cell.text_frame
        p = tf.paragraphs[0]
        p.text = header
        p.font.size = Pt(18)
        p.font.bold = True
        p.font.color.rgb = RgbColor(255, 255, 255)
        p.alignment = PP_ALIGN.CENTER
        
        bg = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(0.5 + col_idx * col_width),
            Inches(1.5),
            Inches(col_width),
            Inches(row_height)
        )
        bg.fill.solid()
        bg.fill.fore_color.rgb = RgbColor(0, 82, 147)
        bg.line.fill.background()
        
    for row_idx, row in enumerate(rows):
        for col_idx, cell_text in enumerate(row):
            cell = slide.shapes.add_textbox(
                Inches(0.5 + col_idx * col_width),
                Inches(1.5 + (row_idx + 1) * row_height),
                Inches(col_width),
                Inches(row_height)
            )
            tf = cell.text_frame
            p = tf.paragraphs[0]
            p.text = str(cell_text)
            p.font.size = Pt(14)
            p.alignment = PP_ALIGN.CENTER
    
    return slide
```

## Template 8: Quote Slide

```python
def create_quote_slide(prs, quote, author, title=''):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    quote_box = slide.shapes.add_textbox(
        Inches(1), Inches(2), Inches(11.333), Inches(3)
    )
    tf = quote_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = f'"{quote}"'
    p.font.size = Pt(32)
    p.font.italic = True
    p.font.color.rgb = RgbColor(51, 51, 51)
    p.alignment = PP_ALIGN.CENTER
    
    author_box = slide.shapes.add_textbox(
        Inches(1), Inches(5.2), Inches(11.333), Inches(0.8)
    )
    tf = author_box.text_frame
    p = tf.paragraphs[0]
    p.text = f"— {author}"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = RgbColor(0, 82, 147)
    p.alignment = PP_ALIGN.CENTER
    
    if title:
        title_box = slide.shapes.add_textbox(
            Inches(1), Inches(5.8), Inches(11.333), Inches(0.5)
        )
        tf = title_box.text_frame
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.color.rgb = RgbColor(150, 150, 150)
        p.alignment = PP_ALIGN.CENTER
    
    return slide
```

## Template 9: Thank You Slide

```python
def create_thank_you_slide(prs, contact_info=None):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    thanks_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(2.5), Inches(12.333), Inches(1.5)
    )
    tf = thanks_box.text_frame
    p = tf.paragraphs[0]
    p.text = "谢谢！"
    p.font.size = Pt(60)
    p.font.bold = True
    p.font.color.rgb = RgbColor(0, 82, 147)
    p.alignment = PP_ALIGN.CENTER
    
    if contact_info:
        contact_box = slide.shapes.add_textbox(
            Inches(0.5), Inches(4.5), Inches(12.333), Inches(2)
        )
        tf = contact_box.text_frame
        for i, (key, value) in enumerate(contact_info.items()):
            if i == 0:
                p = tf.paragraphs[0]
            else:
                p = tf.add_paragraph()
            p.text = f"{key}: {value}"
            p.font.size = Pt(18)
            p.font.color.rgb = RgbColor(100, 100, 100)
            p.alignment = PP_ALIGN.CENTER
    
    return slide
```

## Complete Example: Business Report

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RgbColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_business_report():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    create_title_slide(prs, 
        "2024年度业务报告", 
        "数据驱动增长",
        "数据团队",
        "2024年12月"
    )
    
    create_bullet_slide(prs,
        "执行摘要",
        [
            "年度收入增长45%，达到1.2亿元",
            "用户规模突破100万",
            "客户满意度达到95%",
            "新产品线贡献30%收入"
        ]
    )
    
    create_stats_slide(prs,
        "关键指标",
        [
            {"value": "1.2亿", "label": "年度收入"},
            {"value": "100万+", "label": "活跃用户"},
            {"value": "95%", "label": "客户满意度"},
            {"value": "45%", "label": "同比增长"}
        ]
    )
    
    create_timeline_slide(prs,
        "年度里程碑",
        [
            {"date": "Q1", "description": "产品2.0发布"},
            {"date": "Q2", "description": "用户破50万"},
            {"date": "Q3", "description": "B轮融资"},
            {"date": "Q4", "description": "用户破100万"}
        ]
    )
    
    create_thank_you_slide(prs, {
        "邮箱": "contact@company.com",
        "网站": "www.company.com"
    })
    
    prs.save('business_report.pptx')
    print("PPT已生成: business_report.pptx")

if __name__ == '__main__':
    create_business_report()
```
