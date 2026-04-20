---
name: "ppt-generator"
description: "Generate beautiful PPT presentations using Python (python-pptx) or HTML. Invoke when user wants to create slides, presentations, or export to WPS."
---

# PPT Generator

Generate beautiful, professional PPT presentations programmatically with multiple output formats.

## When to Use

- User wants to create a PPT presentation
- User needs slides for a meeting or report
- User wants to export presentations to WPS
- User needs data visualization in slides

## Output Formats

| Format | Tool | Best For |
|--------|------|----------|
| `.pptx` | python-pptx | Native PowerPoint/WPS format |
| `.html` | HTML/CSS | Web presentations, easy sharing |
| `.pdf` | WeasyPrint | Print-ready documents |

## Quick Start

### 1. Install Dependencies

```bash
pip install python-pptx Pillow
```

### 2. Basic Usage

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RgbColor
from pptx.enum.text import PP_ALIGN

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

slide_layout = prs.slide_layouts[6]
slide = prs.slides.add_slide(slide_layout)

prs.save('presentation.pptx')
```

## Slide Layout Patterns

| Pattern | Description | Use Case |
|---------|-------------|----------|
| `title-slide` | Large title, centered | Cover slide |
| `title-content` | Title + bullet points | Main content |
| `two-column` | Split view | Comparisons |
| `image-left` | Image + text right | Feature showcase |
| `full-image` | Full background image | Impact slides |
| `data-chart` | Chart + insights | Data presentation |

## Style Themes

### Theme: Business Blue
```python
COLORS = {
    'primary': RgbColor(0, 82, 147),
    'secondary': RgbColor(0, 123, 194),
    'accent': RgbColor(255, 192, 0),
    'text': RgbColor(51, 51, 51),
    'background': RgbColor(255, 255, 255)
}
```

### Theme: Tech Dark
```python
COLORS = {
    'primary': RgbColor(0, 212, 255),
    'secondary': RgbColor(138, 43, 226),
    'accent': RgbColor(255, 107, 107),
    'text': RgbColor(255, 255, 255),
    'background': RgbColor(18, 18, 24)
}
```

### Theme: Nature Green
```python
COLORS = {
    'primary': RgbColor(34, 139, 34),
    'secondary': RgbColor(60, 179, 113),
    'accent': RgbColor(255, 165, 0),
    'text': RgbColor(33, 33, 33),
    'background': RgbColor(250, 250, 245)
}
```

## References

| Topic | File |
|-------|------|
| PPT Templates | `references/templates.md` |
| WPS Import Guide | `references/wps-import.md` |
| Chart Examples | `references/charts.md` |
| Animation Effects | `references/animations.md` |

## Workflow

1. **Understand Requirements**: Ask user about content, style, and slide count
2. **Choose Format**: `.pptx` for WPS/PowerPoint, `.html` for web
3. **Generate Content**: Create slides with proper layout and styling
4. **Export**: Save to specified format
5. **WPS Import**: Guide user on importing to WPS

## WPS Import Methods

### Method 1: Direct Open
1. Open WPS Office
2. File → Open → Select `.pptx` file
3. Edit as needed

### Method 2: Import from PDF
1. WPS → File → Import
2. Select PDF file
3. Convert to editable slides

### Method 3: Online Templates
1. WPS → Templates
2. Search for similar style
3. Replace content

## Example: Complete Slide Generator

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RgbColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_presentation(title, slides_data, theme='business', output='output.pptx'):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    themes = {
        'business': {
            'primary': RgbColor(0, 82, 147),
            'text': RgbColor(51, 51, 51),
            'bg': RgbColor(255, 255, 255)
        },
        'tech': {
            'primary': RgbColor(0, 212, 255),
            'text': RgbColor(255, 255, 255),
            'bg': RgbColor(18, 18, 24)
        }
    }
    
    colors = themes.get(theme, themes['business'])
    
    for slide_info in slides_data:
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        
        if slide_info.get('type') == 'title':
            add_title_slide(slide, slide_info, colors)
        else:
            add_content_slide(slide, slide_info, colors)
    
    prs.save(output)
    return output

def add_title_slide(slide, info, colors):
    title_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(2.5), Inches(12.333), Inches(1.5)
    )
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = info['title']
    p.font.size = Pt(54)
    p.font.bold = True
    p.font.color.rgb = colors['primary']
    p.alignment = PP_ALIGN.CENTER
    
    if 'subtitle' in info:
        subtitle_box = slide.shapes.add_textbox(
            Inches(0.5), Inches(4.2), Inches(12.333), Inches(1)
        )
        tf = subtitle_box.text_frame
        p = tf.paragraphs[0]
        p.text = info['subtitle']
        p.font.size = Pt(24)
        p.font.color.rgb = colors['text']
        p.alignment = PP_ALIGN.CENTER

def add_content_slide(slide, info, colors):
    title_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(0.5), Inches(12.333), Inches(1)
    )
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = info['title']
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = colors['primary']
    
    if 'content' in info:
        content_box = slide.shapes.add_textbox(
            Inches(0.5), Inches(1.8), Inches(12.333), Inches(5)
        )
        tf = content_box.text_frame
        tf.word_wrap = True
        
        for i, item in enumerate(info['content']):
            if i == 0:
                p = tf.paragraphs[0]
            else:
                p = tf.add_paragraph()
            p.text = f"• {item}"
            p.font.size = Pt(24)
            p.font.color.rgb = colors['text']
            p.space_after = Pt(12)

if __name__ == '__main__':
    slides = [
        {'type': 'title', 'title': '项目汇报', 'subtitle': '2024年度总结'},
        {'title': '项目概述', 'content': ['背景介绍', '目标设定', '团队构成']},
        {'title': '主要成果', 'content': ['完成率120%', '用户增长50%', '收入翻倍']}
    ]
    create_presentation('项目汇报', slides, 'business', 'report.pptx')
```
