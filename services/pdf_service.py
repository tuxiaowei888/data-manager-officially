"""
PDF报告生成服务 - 数维数据管家系统
"""
from io import BytesIO
from datetime import datetime
import re


def generate_pdf_filename(org_name: str, report_id: int, ext: str = 'pdf') -> str:
    """
    生成统一的PDF文件名
    
    格式: 数据资产评估报告_{企业名称}_{YYYYMMDD}_ID{报告ID}.pdf
    示例: 数据资产评估报告_某某科技公司_20260315_ID123.pdf
    
    Args:
        org_name: 企业名称
        report_id: 报告ID
        ext: 文件扩展名，默认pdf
    
    Returns:
        标准化的文件名
    """
    safe_org_name = sanitize_filename(org_name or '未命名企业')
    date_str = datetime.now().strftime('%Y%m%d')
    return f"数据资产评估报告_{safe_org_name}_{date_str}_ID{report_id}.{ext}"


def sanitize_filename(name: str) -> str:
    """
    清理文件名中的非法字符
    
    Args:
        name: 原始文件名
    
    Returns:
        清理后的安全文件名
    """
    name = str(name).strip()
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = re.sub(r'\s+', '_', name)
    return name[:50]


from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import platform

CHINESE_FONT = 'Helvetica'
CHINESE_FONT_BOLD = 'Helvetica-Bold'

def register_chinese_font():
    """注册中文字体"""
    global CHINESE_FONT, CHINESE_FONT_BOLD
    system = platform.system()
    
    # 尝试注册常规字体
    if system == 'Windows':
        # Windows字体路径 - 优先使用支持emoji的字体
        regular_fonts = [
            ('C:/Windows/Fonts/arialuni.ttf', 'arialuni'),  # Arial Unicode MS，支持中文和emoji
            ('C:/Windows/Fonts/msyh.ttc', 'msyh'),  # 微软雅黑常规，支持中文
            ('C:/Windows/Fonts/simhei.ttf', 'simhei'),  # 黑体
            ('C:/Windows/Fonts/simsun.ttc', 'simsun'),  # 宋体
        ]
        bold_fonts = [
            ('C:/Windows/Fonts/arialuni.ttf', 'arialuni'),  # Arial Unicode MS也可作为粗体（通过加粗样式）
            ('C:/Windows/Fonts/msyhbd.ttc', 'msyhbd'),  # 微软雅黑粗体
            ('C:/Windows/Fonts/simhei.ttf', 'simhei'),  # 黑体本身比较粗
        ]
    elif system == 'Darwin':
        regular_fonts = [
            ('/System/Library/Fonts/PingFang.ttc', 'pingfang'),
            ('/System/Library/Fonts/STHeiti Light.ttc', 'heiti'),
        ]
        bold_fonts = []
    else:
        regular_fonts = [
            ('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 'wqy'),
            ('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', 'wqy'),
        ]
        bold_fonts = []
    
    # 先尝试注册常规字体
    for font_path, font_name in regular_fonts:
        if os.path.exists(font_path):
            try:
                if font_path.endswith('.ttc'):
                    pdfmetrics.registerFont(TTFont('ChineseFont', font_path, subfontIndex=0))
                else:
                    pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                CHINESE_FONT = 'ChineseFont'
                print(f"成功注册中文字体: {font_path}")
                
                # 尝试注册粗体字体
                for bold_path, bold_name in bold_fonts:
                    if os.path.exists(bold_path):
                        try:
                            if bold_path.endswith('.ttc'):
                                pdfmetrics.registerFont(TTFont('ChineseFont-Bold', bold_path, subfontIndex=0))
                            else:
                                pdfmetrics.registerFont(TTFont('ChineseFont-Bold', bold_path))
                            CHINESE_FONT_BOLD = 'ChineseFont-Bold'
                            print(f"成功注册中文字体粗体: {bold_path}")
                            break
                        except Exception as e:
                            print(f"注册粗体字体失败 {bold_path}: {e}")
                            continue
                
                # 如果没有找到粗体字体，使用常规字体加粗效果
                if CHINESE_FONT_BOLD == 'Helvetica-Bold':
                    CHINESE_FONT_BOLD = CHINESE_FONT
                    print("警告: 未找到粗体中文字体，使用常规字体加粗效果")
                
                return
            except Exception as e:
                print(f"注册字体失败 {font_path}: {e}")
                continue
    
    print("警告: 未找到中文字体，使用默认字体")

register_chinese_font()


def safe_text(text):
    """安全处理文本，避免HTML标签和特殊字符导致的问题"""
    if not text:
        return ''
    text = str(text)
    text = text.replace('<', '&lt;').replace('&lt;strong>', '<strong>').replace('&lt;/strong>', '</strong>')
    text = text.replace('>', '&gt;')
    text = text.replace('\n', ' ')
    # 保留emoji，使用arialuni.ttf字体应该支持
    # 如果仍然显示为方框，可以在这里添加字体检测逻辑
    return text.strip()


def get_maturity_level(score):
    if score >= 90:
        return 'A级 (卓越)'
    elif score >= 75:
        return 'B级 (良好)'
    elif score >= 60:
        return 'C级 (合格)'
    return 'D级 (原始态)'


def get_risk_text(risk_level):
    risk_map = {
        'P0': '高',
        'P1': '中',
        'P2': '低',
        'high': '高',
        'medium': '中',
        'low': '低'
    }
    return risk_map.get(risk_level, '未知')


def generate_report_pdf(report_data):
    buffer = BytesIO()
    
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.5*cm,
        leftMargin=1.5*cm,
        topMargin=1.5*cm,
        bottomMargin=1.5*cm
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Title'],
        fontName=CHINESE_FONT,
        fontSize=22,
        textColor=colors.HexColor('#1B3A57'),
        spaceAfter=12,
        alignment=TA_CENTER
    )
    
    subtitle_style = ParagraphStyle(
        'SubtitleStyle',
        parent=styles['Normal'],
        fontName=CHINESE_FONT,
        fontSize=12,
        textColor=colors.HexColor('#666666'),
        alignment=TA_CENTER,
        spaceAfter=6
    )
    
    section_style = ParagraphStyle(
        'SectionStyle',
        parent=styles['Heading2'],
        fontName=CHINESE_FONT,
        fontSize=14,
        textColor=colors.white,
        backColor=colors.HexColor('#1B3A57'),
        borderPadding=5,
        spaceBefore=10,
        spaceAfter=6
    )
    
    normal_style = ParagraphStyle(
        'NormalStyle',
        parent=styles['Normal'],
        fontName=CHINESE_FONT,
        fontSize=12,
        leading=16,
        spaceAfter=6
    )
    
    issue_title_style = ParagraphStyle(
        'IssueTitleStyle',
        parent=styles['Normal'],
        fontName=CHINESE_FONT_BOLD,
        fontSize=13,
        leading=16,
        spaceAfter=4,
        textColor=colors.HexColor('#1B3A57')
    )
    
    issue_detail_style = ParagraphStyle(
        'IssueDetailStyle',
        parent=styles['Normal'],
        fontName=CHINESE_FONT,
        fontSize=11,
        leading=14,
        spaceAfter=3,
        textColor=colors.HexColor('#5A6C7D'),
        leftIndent=10
    )
    
    table_cell_style = ParagraphStyle(
        'TableCellStyle',
        parent=styles['Normal'],
        fontName=CHINESE_FONT,
        fontSize=11,
        leading=16,
        wordWrap='CJK' if CHINESE_FONT != 'Helvetica' else None,
        spaceBefore=0,
        spaceAfter=0
    )
    
    path_title_style = ParagraphStyle(
        'PathTitleStyle',
        parent=styles['Heading3'],
        fontName=CHINESE_FONT_BOLD,
        fontSize=13,
        textColor=colors.HexColor('#1B3A57'),
        spaceBefore=10,
        spaceAfter=6
    )
    
    story = []
    
    story.append(Paragraph('数据资产全链路智能诊断与价值实现报告', title_style))
    story.append(Paragraph('Data Asset Full-Link Intelligent Diagnosis & Value Realization Report', subtitle_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph('智规分析引擎驱动', ParagraphStyle(
        'EngineStyle',
        parent=styles['Normal'],
        fontName=CHINESE_FONT,
        fontSize=11,
        textColor=colors.HexColor('#666666'),
        alignment=TA_CENTER
    )))
    story.append(Spacer(1, 12))
    
    org_name = safe_text(str(report_data.get('org_name', '未命名企业') or '未命名企业'))
    total_score = round(float(report_data.get('total_score', 0) or 0), 1)
    if isinstance(total_score, tuple):
        total_score = total_score[0]
    maturity_level = safe_text(report_data.get('maturity_level') or get_maturity_level(total_score))
    risk_level = report_data.get('risk_level', 'P2') or 'P2'
    generated_at = safe_text(str(report_data.get('generated_at', '') or datetime.now().strftime('%Y-%m-%d %H:%M')))
    report_id = report_data.get('id', 'N/A') or 'N/A'
    
    basic_data = [
        ['报告编号', f'DA-{report_id}'],
        ['生成时间', generated_at],
        ['被测主体', org_name],
        ['风险等级', get_risk_text(risk_level)],
    ]
    
    basic_table = Table(basic_data, colWidths=[3*cm, 12*cm])
    basic_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f5f5f5')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), CHINESE_FONT),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dddddd')),
    ]))
    story.append(basic_table)
    story.append(Spacer(1, 12))
    
    score_style_big = ParagraphStyle(
        'ScoreBigStyle',
        parent=styles['Normal'],
        fontName=CHINESE_FONT,
        fontSize=42,
        textColor=colors.HexColor('#1B3A57'),
        alignment=TA_CENTER,
        leading=45
    )
    score_style_small = ParagraphStyle(
        'ScoreSmallStyle',
        parent=styles['Normal'],
        fontName=CHINESE_FONT,
        fontSize=14,
        textColor=colors.HexColor('#666666'),
        alignment=TA_CENTER,
        leading=20
    )
    score_style_maturity = ParagraphStyle(
        'ScoreMaturityStyle',
        parent=styles['Normal'],
        fontName=CHINESE_FONT_BOLD,
        fontSize=14,
        textColor=colors.HexColor('#1B3A57'),
        alignment=TA_CENTER,
        leading=20
    )
    story.append(Paragraph(str(total_score), score_style_big))
    story.append(Paragraph('综合评分 / 100', score_style_small))
    story.append(Paragraph(maturity_level, score_style_maturity))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph('1. 数据资产成熟度评分', section_style))
    
    dimensions = report_data.get('dimensions', []) or []
    if dimensions:
        # 使用Paragraph包装表头
        dim_data = [
            [
                Paragraph('评价维度', table_cell_style),
                Paragraph('得分', table_cell_style),
                Paragraph('规则库判定逻辑摘要', table_cell_style)
            ]
        ]
        for dim in dimensions:
            name_text = safe_text(str(dim.get('name', '-')) or '-')
            comment = safe_text(str(dim.get('logic', dim.get('comment', '-')) or '-'))
            # 不再截断文本，Paragraph会自动换行
            dim_data.append([
                Paragraph(name_text, table_cell_style),
                Paragraph(f"{round(float(dim.get('score', 0) or 0), 1)}", table_cell_style),
                Paragraph(comment, table_cell_style)
            ])
        
        dim_table = Table(dim_data, colWidths=[4*cm, 2.5*cm, 8.5*cm])
        dim_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1B3A57')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), CHINESE_FONT),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dddddd')),
        ]))
        story.append(dim_table)
    
    story.append(Spacer(1, 12))
    
    story.append(Paragraph('2. 初步诊断结果', section_style))
    
    p0_issues = report_data.get('p0_issues', []) or []
    
    story.append(Paragraph('<b>P0级：关键缺失 (阻碍资产化最后一步)</b>', normal_style))
    if p0_issues:
        for issue in p0_issues:
            title = safe_text(str(issue.get('title', '') or ''))
            problem = safe_text(str(issue.get('problem', '') or ''))
            basis = safe_text(str(issue.get('basis', '') or ''))
            consequence = safe_text(str(issue.get('consequence', '') or ''))
            
            if title:
                story.append(Paragraph(f'* {title}', issue_title_style))
            if problem:
                story.append(Paragraph(f'问题：{problem}', issue_detail_style))
            if basis:
                story.append(Paragraph(f'依据：{basis}', issue_detail_style))
            if consequence:
                story.append(Paragraph(f'后果：{consequence}', issue_detail_style))
            story.append(Spacer(1, 4))
    else:
        story.append(Paragraph('暂无P0级关键缺失问题，合规基础良好', normal_style))
    
    story.append(Spacer(1, 8))
    
    p1_issues = report_data.get('p1_issues', []) or []
    
    story.append(Paragraph('<b>P1级：优化机会 (提升估值与溢价)</b>', normal_style))
    if p1_issues:
        for issue in p1_issues:
            title = safe_text(str(issue.get('title', '') or ''))
            problem = safe_text(str(issue.get('problem', '') or ''))
            opportunity = safe_text(str(issue.get('opportunity', '') or ''))
            basis = safe_text(str(issue.get('basis', '') or ''))
            consequence = safe_text(str(issue.get('consequence', '') or ''))
            
            if title:
                story.append(Paragraph(f'* {title}', issue_title_style))
            if problem:
                story.append(Paragraph(f'Current: {problem}', issue_detail_style))
            if opportunity:
                story.append(Paragraph(f'Opportunity: {opportunity}', issue_detail_style))
            if basis:
                story.append(Paragraph(f'Basis: {basis}', issue_detail_style))
            if consequence:
                story.append(Paragraph(f'Consequence: {consequence}', issue_detail_style))
            story.append(Spacer(1, 4))
    else:
        story.append(Paragraph('暂无P1级优化机会', normal_style))
    
    story.append(PageBreak())
    
    story.append(Paragraph('3. 潜在资产化路径建议', section_style))
    story.append(Paragraph('基于您的数据特点，规则库推荐<strong>"组合拳"</strong>策略，最大化释放价值：', normal_style))
    story.append(Spacer(1, 6))
    
    paths = [
        {
            'name': '路径A：数据资产入表',
            'icon': '📝',
            'rating': '⭐⭐⭐⭐⭐',
            'suitability': '⭐⭐⭐⭐⭐ (强烈推荐，优化科创属性)',
            'actions': ['完善成本辅助账', '双轨确权', '审计评估', '确认为"无形资产"'],
            'effect': '预计可增加资产规模，显著降低资产负债率，助力上市辅导。',
            'certs': ['《数据资产登记证书》', '《数据知识产权登记证书》', '《成本专项审计报告》']
        },
        {
            'name': '路径B：双轨制质押融资',
            'icon': '💰',
            'rating': '⭐⭐⭐⭐⭐',
            'suitability': '⭐⭐⭐⭐⭐ (快速获取低息资金)',
            'actions': ['基础层：凭《数据资产登记证书》申请"数据资产贷"', '智力层：凭《数据知识产权登记证书》申请"知识产权质押贷"'],
            'effect': '预计综合授信额度大幅提升，且可享受绿色金融贴息政策。',
            'certs': ['双证', '《价值评估报告》']
        },
        {
            'name': '路径C：场内交易与生态变现',
            'icon': '📈',
            'rating': '⭐⭐⭐⭐',
            'suitability': '⭐⭐⭐⭐ (打造行业标杆)',
            'actions': ['在数据交易所挂牌产品', '对接潜在买家', '交易合规鉴证'],
            'effect': '预计年交易额突破，成为数据要素典型案例。',
            'certs': ['《数据产品上市证书》', '交易鉴证报告']
        },
        {
            'name': '路径D：作价入股与合资运营',
            'icon': '🤝',
            'rating': '⭐⭐⭐⭐',
            'suitability': '⭐⭐⭐⭐ (拓展市场)',
            'actions': ['以数据知识产权作价', '与合作伙伴成立合资公司', '实现技术/数据输出'],
            'effect': '零现金出资占股，快速复制商业模式。',
            'certs': ['《数据知识产权登记证书》', '《资产评估报告》']
        },
        {
            'name': '路径E：政策奖补与荣誉申报',
            'icon': '🏆',
            'rating': '⭐⭐⭐⭐⭐',
            'suitability': '⭐⭐⭐⭐⭐ (必拿红利)',
            'actions': ['凭借"入表" + "双证" + "交易案例"', '申报示范项目', '争取财政补贴'],
            'effect': '预计获取财政补贴，并获得政府背书，提升品牌影响力。',
            'certs': ['政府补贴资金', '省级/市级荣誉证书']
        },
    ]
    
    for path in paths:
        story.append(Paragraph(f'{path["icon"]} {path["name"]} {path["rating"]}', path_title_style))
        story.append(Paragraph(f'<b>适用性：</b>{path["suitability"]}', normal_style))
        story.append(Paragraph('<b>核心动作：</b>', normal_style))
        for action in path['actions']:
            story.append(Paragraph(f'  - {action}', issue_detail_style))
        story.append(Paragraph(f'<b>预期效果：</b>{path["effect"]}', normal_style))
        story.append(Paragraph(f'<b>关键凭证：</b>{", ".join(path["certs"])}', normal_style))
        story.append(Spacer(1, 8))
    
    story.append(PageBreak())
    
    story.append(Paragraph('4. 价值预测总览', section_style))
    story.append(Paragraph('基于规则库中的行业估值模型，对整改前后的价值进行预测：', normal_style))
    story.append(Spacer(1, 6))
    
    # 使用Paragraph包装表格内容
    value_data = [
        [
            Paragraph('指标维度', table_cell_style),
            Paragraph('当前状态 (As-Is)', table_cell_style),
            Paragraph('整改后预期 (To-Be)', table_cell_style),
            Paragraph('增值驱动力', table_cell_style)
        ],
        [
            Paragraph('资产属性', table_cell_style),
            Paragraph('表外资源 (隐性价值)', table_cell_style),
            Paragraph('表内无形资产 (显性价值)', table_cell_style),
            Paragraph('✅ 资产规模增加 ¥500万+', table_cell_style)
        ],
        [
            Paragraph('法律权属', table_cell_style),
            Paragraph('授权运营 (行政许可)', table_cell_style),
            Paragraph('双证护航 (民事权利)', table_cell_style),
            Paragraph('✅ 法律确权，排他性保护', table_cell_style)
        ],
        [
            Paragraph('融资能力', table_cell_style),
            Paragraph('¥100万 (纯信用)', table_cell_style),
            Paragraph('¥500万+ (质押+信用)', table_cell_style),
            Paragraph('💰 双证叠加，授信翻倍', table_cell_style)
        ],
        [
            Paragraph('年交易营收', table_cell_style),
            Paragraph('线下零星', table_cell_style),
            Paragraph('线上规模化', table_cell_style),
            Paragraph('📈 产品标准化，买家增多', table_cell_style)
        ],
        [
            Paragraph('整体估值', table_cell_style),
            Paragraph('难以单独量化', table_cell_style),
            Paragraph('¥2000万 - ¥5000万', table_cell_style),
            Paragraph('🚀 收益法 + 市场法双重验证', table_cell_style)
        ],
    ]
    
    value_table = Table(value_data, colWidths=[3*cm, 4*cm, 4*cm, 4*cm])
    value_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1B3A57')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), CHINESE_FONT),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dddddd')),
    ]))
    story.append(value_table)
    story.append(Spacer(1, 6))
    story.append(Paragraph('注：以上预测基于行业平均水平及现行政策，具体数值需以正式评估报告为准。', issue_detail_style))
    
    story.append(PageBreak())
    
    story.append(Paragraph('5. 转化目标完成链路建议', section_style))
    story.append(Paragraph(f'为实现从{maturity_level}到更高级别的跨越，建议执行以下<strong>"四步走"</strong>加速计划：', normal_style))
    story.append(Spacer(1, 6))
    
    phases = [
        {
            'name': '第一阶段：成本重构与双轨策划',
            'time': 'Week 1-3',
            'goal': '解决成本计量模糊问题，制定双轨申报策略',
            'actions': ['成本精细化：建立数据资源专项辅助账，自动分摊研发工时与云资源成本', '资产拆分：将"基础数据"与"核心算法"进行逻辑拆分', '方案设计：制定《数据资产双轨确权实施方案》'],
            'outputs': ['《数据资源成本核算表》', '《双轨确权实施路线图》']
        },
        {
            'name': '第二阶段：双轨确权攻坚',
            'time': 'Week 4-7',
            'goal': '获取两大核心证书，夯实法律权属',
            'actions': ['资产登记：向数据交易所提交申请，获取《数据资产登记证书》', 'IP登记：向知识产权保护中心提交核心算法申请，获取《数据知识产权登记证书》', '合规复核：由律师出具最终版《数据合规法律意见书》'],
            'outputs': ['🏆《数据资产登记证书》', '🏆《数据知识产权登记证书》']
        },
        {
            'name': '第三阶段：评估入表与产品上架',
            'time': 'Week 8-11',
            'goal': '完成资产确认，实现产品挂牌',
            'actions': ['综合评估：聘请评估机构，结合双证出具高价值《资产评估报告》', '审计入表：配合会计师事务所，将数据资源正式列入资产负债表', '产品挂牌：在数交所正式挂牌数据产品'],
            'outputs': ['审计报告 (含数据资产)', '数交所挂牌证书']
        },
        {
            'name': '第四阶段：融资落地与生态扩张',
            'time': 'Week 12+',
            'goal': '资金到账，业务规模化',
            'actions': ['银企对接：持双证与评估报告，对接银行落实"数据资产质押贷"', '交易撮合：举办数据产品发布会，签约首批客户', '申报奖补：提交省级/市级示范项目申请材料'],
            'outputs': ['银行放款凭证', '大额交易合同', '政府立项通知']
        },
    ]
    
    for i, phase in enumerate(phases):
        story.append(Paragraph(f'{i+1}. {phase["name"]} ({phase["time"]})', path_title_style))
        story.append(Paragraph(f'<b>目标：</b>{phase["goal"]}', normal_style))
        story.append(Paragraph('<b>动作：</b>', normal_style))
        for action in phase['actions']:
            story.append(Paragraph(f'  - {action}', issue_detail_style))
        story.append(Paragraph(f'<b>产出：</b>{", ".join(phase["outputs"])}', normal_style))
        story.append(Spacer(1, 8))
    
    story.append(PageBreak())
    
    story.append(Paragraph('6. 深度咨询服务方案', section_style))
    story.append(Paragraph('数据资产化是一项涉及法律、财务、技术、业务的系统工程，尤其是<strong>"双轨确权"和"成本精细化核算"</strong>环节，需要资深专家团队的深度介入与全程陪跑。', normal_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph('🌟 我们的核心服务模块', path_title_style))
    
    # 使用Paragraph包装表格内容
    service_data = [
        [
            Paragraph('服务模块', table_cell_style),
            Paragraph('服务内容', table_cell_style),
            Paragraph('交付成果', table_cell_style)
        ],
        [
            Paragraph('1. 成本重构与入表辅导', table_cell_style),
            Paragraph('驻场指导成本归集、建立辅助账、协助选聘会所、审计沟通、报表披露', table_cell_style),
            Paragraph('《成本核算指引》、入表审计报告', table_cell_style)
        ],
        [
            Paragraph('2. 双轨确权全程代理', table_cell_style),
            Paragraph('资产/IP拆分策划、申报材料撰写、对接数交所/知产中心、答辩辅导', table_cell_style),
            Paragraph('🏆《数据资产登记证书》、🏆《数据知识产权登记证书》', table_cell_style)
        ],
        [
            Paragraph('3. 价值评估与融资对接', table_cell_style),
            Paragraph('引入顶级评估机构、设计融资方案、对接银行、落实放款', table_cell_style),
            Paragraph('《综合价值评估报告》、银行授信批复', table_cell_style)
        ],
        [
            Paragraph('4. 产品化与交易运营', table_cell_style),
            Paragraph('数据产品设计、API封装、数交所挂牌、买家撮合、交易合规鉴证', table_cell_style),
            Paragraph('数交所挂牌证书、交易合同', table_cell_style)
        ],
        [
            Paragraph('5. 政策申报与荣誉规划', table_cell_style),
            Paragraph('策划典型案例、申报示范项目、争取财政补贴', table_cell_style),
            Paragraph('政府补贴资金、荣誉证书', table_cell_style)
        ],
    ]
    
    service_table = Table(service_data, colWidths=[4*cm, 6.5*cm, 4.5*cm])
    service_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1B3A57')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), CHINESE_FONT),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dddddd')),
    ]))
    story.append(service_table)
    story.append(Spacer(1, 12))
    
    footer_style = ParagraphStyle(
        'FooterStyle',
        parent=styles['Normal'],
        fontName=CHINESE_FONT,
        fontSize=11,
        textColor=colors.HexColor('#999999'),
        alignment=TA_CENTER
    )
    story.append(Paragraph('数维创擎 —— 让数据真正成为您的核心资产', footer_style))
    story.append(Paragraph('基于数维·数据资产评价体系规则库 v1.0', footer_style))
    story.append(Paragraph('咨询热线：13982274410 | 邮箱：tuxiaowei@szt-dipr.com', footer_style))
    
    doc.build(story)
    
    buffer.seek(0)
    return buffer
