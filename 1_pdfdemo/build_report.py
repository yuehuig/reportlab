#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
    file: build_report.py
    author: Zhangke <ke.zhang@capitalbio.com> Changyujun <yujunchang@capitalbio.com>
    version: 3.1.4
    last update: 2020.06.18
    function: judge postive and build report
'''

__all__ = ['group_judge_positive', 'create_pdf', 'decompose_final_result', 'write_summarize_result']

import os
import time
from ast import literal_eval

import pandas as pd
import numpy as np

from plotter import plot_bar, plot_error
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import (Image, PageBreak, Paragraph, Preformatted,
                                SimpleDocTemplate, Spacer, Table, TableStyle, KeepTogether)
from reportlab.platypus.flowables import TopPadder
from reportlab.lib.units import mm                                

pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
pdfmetrics.registerFont(TTFont('simsun', '/home/zongyaru/.fonts/chinese/songti/STZHONGS.TTF'))
pdfmetrics.registerFont(TTFont('Times', '/home/zongyaru/.fonts/chinese/Time_new_Roman/timesi.ttf'))
pdfmetrics.registerFont(TTFont('msyh', '/usr/share/fonts/msyh/msyh.ttc'))



def iter_draw_tables(total_read_count_for_each_txid_dict, species_list, story, fig_folder):
    '''
    [0] Rank                    1
    [1] Kingdom                 'V'
    [2] txid                    '290028'
    [3] sciName                 'Human_coronavirus_HKU1'
    [4] uniq_reads_num          229
    [5] total_reads_num         452
    [6] coverage_len            1051
    [7] coverage_ref_len        2985744
    [8] coverage_percent        3.52
    [9] depth_total             46471
    [10] depth_avg              1051
    [11] nt_title               DQ415906.1|29857|Human coronavirus HKU1 strain N9 genotype A, complete genome
    [12] avg_hit_num            1
    [13] reads_distr            0.28
    '''
    component_data = []
    all_table_style = [('FONTNAME', (0, 0), (-1, -1), 'msyh'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),  # 整个表格字体大小
        ('LINEBEFORE', (0, 0), (-1, -1), 0.1, colors.lightgrey),  # 设置表格左边线颜色为灰色，线宽为0.1
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),  # 设置表格内文字颜色
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # 对齐
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 对齐
        ('GRID', (0, 0), (-1, -1), 0.1, colors.grey),  # 设置表格框线为灰色，线宽为0.5
    ]
    for i in range(len(species_list)):
        id = species_list[i][2]
        rank = '排名：' + str(i + 1)
        sciname = '种名：' + species_list[i][3]
        txid = '种分类号：' + str(species_list[i][2])
        #total_reads = '总命中reads数：' + str(total_read_count_for_each_txid_dict[id])
        #uniq_reads = '种特异性reads数：' + str(species_list[i][4])
        uniq_reads = '检出reads数：' + str(total_read_count_for_each_txid_dict[id])
        #total_hit_len = '总命中长度：' + str(species_list[i][6])
        coverage = '覆盖度：' + str(species_list[i][8]) + '%'
        #depth = '覆盖区平均深度：' + str(species_list[i][9]) + '/' + str(species_list[i][6]) + '=' + str(species_list[i][10])
        ref_seq = '命中参考序列：' + str(species_list[i][11]).split('|')[1][0:75]
        hit_reads_ratio = int(species_list[i][5] * 100 / total_read_count_for_each_txid_dict[id])
        annotation_str = '# 技术性注释 #\n'
        annotation_str = annotation_str + '# 共有 ' + str(total_read_count_for_each_txid_dict[id]) + ' 条reads命中“' + str(
            species_list[i][2]) + '（' + species_list[i][3] + '）”\n'
        annotation_str = annotation_str + '# 其中 ' + str(hit_reads_ratio) + '% 的reads具体命中 ' + \
                         str(species_list[i][11]).split('|')[1][0:65] + '\n'
        annotation_str = annotation_str + '# 命中的物种基因组总长度为 ' + str(species_list[i][7]) + ' bp，测到的该物种序列拼接后总长度为 ' + str(
            species_list[i][6]) + ' bp，覆盖度为 ' + str(species_list[i][8]) + '%\n'
        annotation_str = annotation_str + '# 测到的该物种序列的总碱基数为 ' + str(species_list[i][9]) + ' bp，测到的该物种序列拼接后总长度为 ' + str(
            species_list[i][6]) + ' bp，平均深度为 ' + str(species_list[i][10]) + 'X'

        fig_dir = fig_folder.rstrip('/') + '/' + species_list[i][2] + '.png'
        plot_data_path = fig_folder.rstrip('/') + '/' + species_list[i][2] + '.npz'
        if not os.path.exists(fig_dir):
            if os.path.exists(plot_data_path):
                #data = np.load(plot_data_path, allow_pickle=True).item()
                data = np.load(plot_data_path)
                x_data = str(data['x_arr'])
                x_arr = eval(x_data)
                try:
                    plot_bar(x_arr, data['coverage_arr'], str(data['sciname']), str(data['sample_name']),
                        float(data['coverage']), float(data['avg_depth']), str(data['nt_item']), fig_dir)
                except MemoryError:
                    plot_error(str(data['sciname']), float(data['coverage']), float(data['avg_depth']),
                            str(data['nt_item']), fig_dir)
            else:
                print(species_list[i])
                raise IOError("%s not found!" % plot_data_path)
        img = Image(fig_dir)
        img.drawHeight = 120
        img.drawWidth = 440

        component_data = [[rank, sciname, txid], 
                        ['  ' + uniq_reads + '    |    ' + coverage],
                        [annotation_str], [ref_seq], [img]]
        
        #begin_index = 5*i + 1
        #end_index = 5*i + 4 + 1
        for k in range(1, 5):
            all_table_style.append(('SPAN', (0, k), (2, k)))
        component_table = Table(component_data, colWidths=[60, 290, 100])
        component_table.setStyle(TableStyle(all_table_style))
        story.append(KeepTogether(component_table))
    return story


def _header_footer(canvas, doc):
    # Save the state of our canvas so we can draw on it
    canvas.saveState()
    styles = getSampleStyleSheet()

    # Header
    space = "&nbsp;" * 73
    dash = "-" * 150
    # header_text = '''<para autoLeading="off" fontSize=8 color=gray align=left><font face="msyh">
    # 北京博奥医学检验所{0}QR-D.SY003-03-BABJ A/1{1}超广谱病原微生物mNGS检测报告[MAPMI v3.2.0]</font><br/>
    # <font face='STSong-Light' color=gray>{2}</font><br/><br/></para>'''.format(space, space, dash)
    header_text = '''<para autoLeading="off" fontSize=8 color=gray align=left><font face="msyh">
        中南大学湘雅医学检验所{0}超广谱病原微生物mNGS检测报告[MAPMI v3.1.4]</font><br/>
        <font face='STSong-Light' color=gray>{1}</font><br/><br/></para>'''.format(space, dash)

    header = Paragraph(header_text, styles['Normal'])
    __, h = header.wrap(doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - float(h) / float(2))

    # Footer
    space1 = "&nbsp;" * 14
    space2 = "&nbsp;" * 85
    page_num = "第%s页" % str(int(canvas.getPageNumber()) - 1)
    global g_page_total
    g_page_total = int(canvas.getPageNumber()) - 1
    footer_text = '''<para autoLeading="off" fontSize=8 color=gray align=left>
    <font face='STSong-Light' color=gray>{0}</font><br/><font face='msyh' fontSize=7 color=gray>地址：湖南省长沙市开福区湘雅路110号{1}电话：0731-84805380{2}{3}<br/></font>
    </para>'''.format(dash, space1, space2, page_num)

    footer = Paragraph(footer_text, styles['Normal'])
    __, h = footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, h)

    canvas.restoreState()

def _header_footer_second(canvas, doc):
    # Save the state of our canvas so we can draw on it
    canvas.saveState()
    styles = getSampleStyleSheet()

    # Header
    space = "&nbsp;" * 73
    dash = "-" * 150
    header_text = '''<para autoLeading="off" fontSize=8 color=gray align=left><font face="msyh">
    中南大学湘雅医学检验所{0}超广谱病原微生物mNGS检测报告[MAPMI v3.1.4]</font><br/>
    <font face='STSong-Light' color=gray>{1}</font><br/><br/></para>'''.format(space, dash)

    header = Paragraph(header_text, styles['Normal'])
    __, h = header.wrap(doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - float(h) / float(2))

    # Footer
    space1 = "&nbsp;" * 14
    space2 = "&nbsp;" * 85
    page_num = "第%d页/共%d页" % ((int(canvas.getPageNumber()) - 1), g_page_total)

    footer_text = '''<para autoLeading="off" fontSize=8 color=gray align=left>
        <font face='STSong-Light' color=gray>{0}</font><br/><font face='msyh' fontSize=7 color=gray>地址：湖南省长沙市开福区湘雅路110号{1}电话：0731-84805380{2}{3}<br/></font>
        </para>'''.format(dash, space1, space2, page_num)

    footer = Paragraph(footer_text, styles['Normal'])
    __, h = footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, h)

    canvas.restoreState()


def _on_page_start(canvas, doc):
    c = Const()
    canvas.saveState()
    background = c.FIRST_PAGE_BG
    capitalbio = c.FIRST_PAGE_LOGO_JY
    canvas.drawImage(capitalbio, 30, 720, width=110, height=80)  ## 设置CapitalBio_MedLab.png图片
    canvas.drawImage(background, 8, float(doc.height) / 3.6, width=582, height=500)
    canvas.restoreState()

def _on_page_start_manu(canvas, doc):
    c = Const('Other')
    canvas.saveState()
    background = c.FIRST_PAGE_BG
    capitalbio = c.FIRST_PAGE_LOGO_JY
    canvas.drawImage(capitalbio, 30, 720, width=110, height=80)      ## 设置CapitalBio_MedLab.png图片
    canvas.drawImage(background, 8, float(doc.height) / 3.6, width=582, height=500)
    canvas.restoreState()


def clinic_info_read_store(samplename, patient_info_file, sample_clinic_info_list):

    patient_info_dict = {}
    all_submitted_sample_dict = {}
    for patient in sample_clinic_info_list:
        all_submitted_sample_dict[patient[0]] = patient

    if samplename in all_submitted_sample_dict.keys():

        w = open(patient_info_file, 'w')
        str_w = ''
        for item in all_submitted_sample_dict[samplename]:
            str_w = str_w + item.encode('utf-8') + '|*|'
        w.write(str_w + '\n')
        w.close()

        patient_info_dict['sample_no'] = samplename
        patient_info_dict['barcode'] = all_submitted_sample_dict[samplename][1].encode('utf-8')
        patient_info_dict['hospitalized_no'] = all_submitted_sample_dict[samplename][2].encode('utf-8')
        patient_info_dict['name'] = all_submitted_sample_dict[samplename][3].encode('utf-8')
        patient_info_dict['gender'] = all_submitted_sample_dict[samplename][4].encode('utf-8')
        patient_info_dict['age'] = all_submitted_sample_dict[samplename][5].encode('utf-8')
        patient_info_dict['doctor'] = all_submitted_sample_dict[samplename][6].encode('utf-8')
        patient_info_dict['department'] = all_submitted_sample_dict[samplename][7].encode('utf-8')
        patient_info_dict['institute'] = all_submitted_sample_dict[samplename][8].encode('utf-8')
        patient_info_dict['sample_type'] = all_submitted_sample_dict[samplename][9].encode('utf-8')
        patient_info_dict['sample_vol'] = all_submitted_sample_dict[samplename][10].encode('utf-8')
        patient_info_dict['date_sample'] = all_submitted_sample_dict[samplename][11].encode('utf-8')

        patient_info_dict['symptom'] = all_submitted_sample_dict[samplename][12].encode('utf-8')
        patient_info_dict['diagnosis_info'] = all_submitted_sample_dict[samplename][13].encode('utf-8')
        patient_info_dict['treatment'] = all_submitted_sample_dict[samplename][14].encode('utf-8')

        patient_info_dict['date_report'] = time.strftime('%Y-%m-%d %H:%M:%S')
    else:
        if os.path.exists(patient_info_file):
            with open(patient_info_file) as file:
                for line in file:
                    patient_info_dict['sample_no'] = samplename
                    patient_info_dict['barcode'] = line.strip().split('|*|')[1]
                    patient_info_dict['hospitalized_no'] = line.strip().split('|*|')[2]
                    patient_info_dict['name'] = line.strip().split('|*|')[3]
                    patient_info_dict['gender'] = line.strip().split('|*|')[4]
                    patient_info_dict['age'] = line.strip().split('|*|')[5]
                    patient_info_dict['doctor'] = line.strip().split('|*|')[6]
                    patient_info_dict['department'] = line.strip().split('|*|')[7]
                    patient_info_dict['institute'] = line.strip().split('|*|')[8]
                    patient_info_dict['sample_type'] = line.strip().split('|*|')[9]
                    patient_info_dict['sample_vol'] = line.strip().split('|*|')[10]
                    patient_info_dict['date_sample'] = line.strip().split('|*|')[11]

                    patient_info_dict['symptom'] = line.strip().split('|*|')[12]
                    patient_info_dict['diagnosis_info'] = line.strip().split('|*|')[13]
                    patient_info_dict['treatment'] = line.strip().split('|*|')[14]

                    patient_info_dict['date_report'] = time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            patient_info_dict['sample_no'] = samplename
            patient_info_dict['barcode'] = '-'
            patient_info_dict['hospitalized_no'] = '-'
            patient_info_dict['name'] = '-'
            patient_info_dict['gender'] = '-'
            patient_info_dict['age'] = '-'
            patient_info_dict['doctor'] = '-'
            patient_info_dict['department'] = '-'
            patient_info_dict['institute'] = '-'
            patient_info_dict['sample_type'] = '-'
            patient_info_dict['sample_vol'] = '-'
            patient_info_dict['date_sample'] = '-'
            patient_info_dict['symptom'] = '-'
            patient_info_dict['diagnosis_info'] = '-'
            patient_info_dict['treatment'] = '-'
            patient_info_dict['date_report'] = time.strftime('%Y-%m-%d %H:%M:%S')

    for key in patient_info_dict.keys():
        if patient_info_dict[key] == 'undefined':
            patient_info_dict[key] = '-'

    return patient_info_dict


def _sample_clinic_info(samplename, story, patient_info_file, patient_info_dict):

    stylesheet = getSampleStyleSheet()
    normalStyle = stylesheet['Normal']
    text = '<para autoLeading="off" fontSize=11><b><font face="msyh">一、样品信息</font></b><br/><br/></para>'
    story.append(Paragraph(text, normalStyle))

    text = '<para autoLeading="off" fontSize=10><b><font face="msyh">（一）受检者</font></b><br/><br/></para>'
    story.append(Paragraph(text, normalStyle))

    component_data = [['姓名：'.decode('utf-8') + patient_info_dict['name'].decode('utf-8'),
                       '性别：'.decode('utf-8') + patient_info_dict['gender'].decode('utf-8')],
                       ['年龄：'.decode('utf-8') + patient_info_dict['age'].decode('utf-8'),
                       '住院号/门诊号：'.decode('utf-8') + patient_info_dict['hospitalized_no'].decode('utf-8')]]

    #component_data = [['条码号：'.decode('utf-8') + patient_info_dict['barcode'].decode('utf-8'), ''],
    #                  ['样品编号：'.decode('utf-8') + patient_info_dict['sample_no'].decode('utf-8'),
    #                   '住院号：'.decode('utf-8') + patient_info_dict['hospitalized_no'].decode('utf-8')],
    #                  ['姓名：'.decode('utf-8') + patient_info_dict['name'].decode('utf-8'),
    #                   '性别：'.decode('utf-8') + patient_info_dict['gender'].decode('utf-8')],
    #                  ['年龄：'.decode('utf-8') + patient_info_dict['age'].decode('utf-8'),
    #                   '送检医生：'.decode('utf-8') + patient_info_dict['doctor'].decode('utf-8')],
    #                  ['送检科室：'.decode('utf-8') + patient_info_dict['department'].decode('utf-8'),
    #                   '送检单位：'.decode('utf-8') + patient_info_dict['institute'].decode('utf-8')],
    #                  ['样品类型：'.decode('utf-8') + patient_info_dict['sample_type'].decode('utf-8'),
    #                   '样品体积：'.decode('utf-8') + patient_info_dict['sample_vol'].decode('utf-8')],
    #                  ['接收日期：'.decode('utf-8') + patient_info_dict['date_sample'].decode('utf-8'),
    #                   '报告日期：'.decode('utf-8') + patient_info_dict['date_report'].decode('utf-8')]]

    component_table = Table(component_data, colWidths=[180, 180])
    component_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'msyh'),  # 整个表格字体
        ('FONTSIZE', (0, 0), (-1, -1), 8),  # 整个表格字体大小
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.white),
        #('BOX', (0, 0), (-1, -1), 0.25, colors.white),
        #('BACKGROUND', (0, 1), (2, 1), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),  # 设置表格内文字颜色
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # 对齐
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 对齐
        ('GRID', (0, 0), (-1, -1), 0.1, colors.grey),  # 设置表格框线为灰色，线宽为0.5
    ]))



    #component_table.setStyle(TableStyle([
    #    ('FONTNAME', (0, 0), (-1, -1), 'msyh'),  # 整个表格字体
    #    ('FONTSIZE', (0, 0), (-1, -1), 8),  # 整个表格字体大小
    #    ('LINEBEFORE', (0, 0), (-1, -1), 0.1, colors.lightgrey),  # 设置表格左边线颜色为灰色，线宽为0.1
    #    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),  # 设置表格内文字颜色
    #    ('SPAN', (0, 0), (1, 0)),  # 合并第一行前二列
    #    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # 对齐
    #    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 对齐
    #    ('GRID', (0, 0), (-1, -1), 0.1, colors.grey),  # 设置表格框线为灰色，线宽为0.5
    #]))
    story.append(component_table) 


    text = '<para autoLeading="off" fontSize=10><br/><br/><br/><br/><b><font face="msyh">（二）样品信息</font></b><br/><br/></para>'
    story.append(Paragraph(text, normalStyle))
    component_data = [['送 检 号：'.decode('utf-8') + patient_info_dict['barcode'].decode('utf-8'), 
                        '样品编号：'.decode('utf-8') + patient_info_dict['sample_no'].decode('utf-8')],
                    ['样品类型：'.decode('utf-8') + patient_info_dict['sample_type'].decode('utf-8'),
                       '样品体积：'.decode('utf-8') + patient_info_dict['sample_vol'].decode('utf-8')],
                    ['接收日期：'.decode('utf-8') + patient_info_dict['date_sample'].decode('utf-8'),
                       '报告日期：'.decode('utf-8') + patient_info_dict['date_report'].decode('utf-8')]]
    # 诊断信息
    #component_data = [['临床症状：'.decode('utf-8'), patient_info_dict['symptom'].decode('utf-8')],
    #                  ['前期诊断信息：'.decode('utf-8'), patient_info_dict['diagnosis_info'].decode('utf-8')],
    #                  ['近期用药：'.decode('utf-8'), patient_info_dict['treatment'].decode('utf-8')]]
    component_table = Table(component_data, colWidths=[180, 180])
    component_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'msyh'),  # 整个表格字体
        ('FONTSIZE', (0, 0), (-1, -1), 8),  # 整个表格字体大小
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.white),
        #('BOX', (0, 0), (-1, -1), 0.25, colors.white),
        #('BACKGROUND', (0, 1), (2, 1), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),  # 设置表格内文字颜色
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # 对齐
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 对齐
        ('GRID', (0, 0), (-1, -1), 0.1, colors.grey),
    ]))
    #component_table.setStyle(TableStyle([
    #    ('FONTNAME', (0, 0), (-1, -1), 'msyh'),  # 整个表格字体 
    #    ('FONTSIZE', (0, 0), (-1, -1), 8),  # 整个表格字体大小
    #    ('LINEBEFORE', (0, 0), (-1, -1), 0.1, colors.lightgrey),  # 设置表格左边线颜色为灰色，线宽为0.1
    #    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),  # 设置表格内文字颜色
    #    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # 对齐
    #    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 对齐
    #    ('GRID', (0, 0), (-1, -1), 0.1, colors.grey),  # 设置表格框线为灰色，线宽为0.5
    #]))
    story.append(component_table)

    text = '<para autoLeading="off" fontSize=10><br/><br/><br/><br/><b><font face="msyh">（三）送检信息</font></b><br/><br/></para>'
    story.append(Paragraph(text, normalStyle))
    
    component_data = [['送检单位：'.decode('utf-8') + patient_info_dict['institute'].decode('utf-8'),
                       '送检科室：'.decode('utf-8') + patient_info_dict['department'].decode('utf-8')],
                       ['送检医生：'.decode('utf-8') + patient_info_dict['doctor'].decode('utf-8'),'']]
    component_table = Table(component_data, colWidths=[180, 180])
    component_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'msyh'),  # 整个表格字体
        ('FONTSIZE', (0, 0), (-1, -1), 8),  # 整个表格字体大小
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.white),
        #('BOX', (0, 0), (-1, -1), 0.25, colors.white),
        #('BACKGROUND', (0, 1), (2, 1), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),  # 设置表格内文字颜色
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # 对齐
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 对齐
        ('GRID', (0, 0), (-1, -1), 0.1, colors.grey),
    ]))
    story.append(component_table)

    text = '<para autoLeading="off" fontSize=10><br/><br/><br/><br/><b><font face="msyh">（四）临床信息</font></b><br/><br/></para>'
    story.append(Paragraph(text, normalStyle))

    # 添加自定义样式
    stylesheet.add(
        ParagraphStyle(name='body',
                       parent=stylesheet['Normal'],
                       fontName="msyh",
                       fontSize=8,
                       textColor='black',
                       leading=16,                # 行间距
                       spaceBefore=0,             # 段前间距
                       spaceAfter=10,             # 段后间距
                       leftIndent=40,              # 左缩进
                       rightIndent=0,             # 右缩进
                       firstLineIndent=-40,        # 首行缩进，每个汉字为10
                       alignment=TA_JUSTIFY,      # 对齐方式
                       )
                    )
    body = stylesheet['body']
    body.wordWrap = 'CJK'
    text1 = '临床症状：'.decode('utf-8')+patient_info_dict['symptom'].decode('utf-8')
    text2 = '前期检测：'.decode('utf-8')+patient_info_dict['diagnosis_info'].decode('utf-8')
    text3 = '前期用药：'.decode('utf-8')+patient_info_dict['treatment'].decode('utf-8')
    #story.append(Paragraph(text1, body))
    #story.append(Paragraph(text2, body))
    #story.append(Paragraph(text3, body))

    component_data = [[Paragraph(text1, body)],
                    [Paragraph(text2, body)],
                    [Paragraph(text3, body)]]
    component_table = Table(component_data, colWidths=[360])
    component_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'msyh'),  # 整个表格字体
        ('FONTSIZE', (0, 0), (-1, -1), 8),  # 整个表格字体大小
        #('INNERGRID', (0, 0), (-1, -1), 0.25, colors.white),
        #('BOX', (0, 0), (-1, -1), 0.25, colors.white),
        #('BACKGROUND', (0, 1), (2, 1), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),  # 设置表格内文字颜色
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # 对齐
        #('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 对齐
        ('GRID', (0, 0), (-1, -1), 0.1, colors.grey),
    ]))
    story.append(component_table)

    ## 诊断信息
    #component_data = [['临床症状：'.decode('utf-8')+patient_info_dict['symptom'].decode('utf-8'),''],
    #                  ['前期检测：'.decode('utf-8')+patient_info_dict['diagnosis_info'].decode('utf-8'),''],
    #                  ['前期用药：'.decode('utf-8')+patient_info_dict['treatment'].decode('utf-8'),'']]
    #component_table = Table(component_data, colWidths=[360, 0])
    #component_table.setStyle(TableStyle([
    #    ('FONTNAME', (0, 0), (-1, -1), 'msyh'),  # 整个表格字体
    #    ('FONTSIZE', (0, 0), (-1, -1), 8),  # 整个表格字体大小
    #    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.white),
    #    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),  # 设置表格内文字颜色
    #    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # 对齐
    #    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 对齐
    #    #('GRID', (0, 0), (-1, -1), 0.1, colors.grey),  # 设置表格框线为灰色，线宽为0.5
    #]))
    #story.append(component_table)

    space = '&nbsp;' * 40
    detect_date = time.strftime('%Y-%m-%d %H:%M:%S').split()[0]
    text = '''<para  autoLeading="off" fontSize=9 align=center>
    <b><font face='msyh' color=black>检验人：{0}审核人：{0}报告日期：{1}</font></b><br/><br/><br/></para>'''.format(
        space, detect_date)
    story.append(Spacer(1, 5 * mm))
    story.append(TopPadder(Paragraph(text, normalStyle)))

    #text = '''[免责声明]\n
    #1. 本检测为新技术方法的临床验证，结果仅供参考，不用于诊断。
    #2. 本检测结果只对本次受检样品负责，相关解释须咨询临床医生。
    #3. 本方法与其它检测方法一样，有自身的检测能力和检测范围（即方法局限性），本报告未报告微生物只代表在本方法
    #    的检测能力下无阳性物种报告，不代表样品中一定不存在病原微生物。
    #4. 如上述第3点所述，造成本方法假阴性结果的原因包括但不限于以下两点：
    #   1) 被检病原体浓度过低：本方法对低于100copies/mL（对于病毒为1000copies/mL）的病原体浓度不能保证100%检出。
    #   2) 被检病原体不在数据库中：本方法虽然构建有包括7373种病毒、3348种细菌、209种真菌和153种寄生虫在内的数据
    #       库，但这仍不保证完全涵盖所有临床可能出现的病原微生物。
    #5. 由于众所周知的原因，耐药基因与实际耐药表型并不完全一致，该报告中耐药基因检测结果仅供临床医生参考。
    #6. 本检测对该结果保密并依法保护受检者隐私，但因受检者个人原因出现信息外泄，本实验室不承担相应责任。
    #'''
    #component_data = [[text]]
    #component_table = Table(component_data, colWidths=[450])
    #component_table.setStyle(TableStyle([
    #    ('FONTNAME', (0, 0), (-1, -1), 'msyh'),  # 整个表格字体
    #    ('FONTSIZE', (0, 0), (-1, -1), 8),  # 整个表格字体大小
    #    ('LINEBEFORE', (0, 0), (-1, -1), 0.1, colors.lightgrey),  # 设置表格左边线颜色为灰色，线宽为0.1
    #    ('TEXTCOLOR', (0, 0), (-1, -1), colors.grey),  # 设置表格内文字颜色
    #    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # 对齐
    #    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 对齐
    #    ('GRID', (0, 0), (-1, -1), 0.1, colors.grey),  # 设置表格框线为灰色，线宽为0.5
    #]))
    #story.append(component_table)

    #text = '''<para  autoLeading="off" fontSize=9 color=grey align=center><br/><br/>
    #<b><font face='msyh' color=grey>* 本报告结果仅对本次送检标本负责！结果仅供医生参考，不作为临床诊断唯一依据 *</font></b></para>'''
    #story.append(Paragraph(text, normalStyle))

    return story


def _sequencing_statistics_info(story, sequencing_info_list):
    '''
    sequencing_info_list:
    [0]total_raw_reads
    [1]total_qualified_reads
    [2]dedup_percent
    [3]human_reads
    [4]human_reads_perc
    [5]no_human_reads
    [6]read_avg_len
    [7]avg_quality
    [8]read_len_png_dir
    [9]avg_quality_png_dir
    [10]platform
    [11]microbial_reads_num
    '''

    total_raw_reads = sequencing_info_list[0]
    total_qualified_reads = sequencing_info_list[1]
    #dedup_percent = sequencing_info_list[2]
    human_reads = sequencing_info_list[3]
    human_reads_perc = sequencing_info_list[4]
    no_human_reads = sequencing_info_list[5]
    read_avg_len = sequencing_info_list[6]
    avg_quality = sequencing_info_list[7]
    read_len_png_dir = sequencing_info_list[8]
    avg_quality_png_dir = sequencing_info_list[9]
    platform = sequencing_info_list[10]
    qualified_reads_perc = '%.2f' % (float(total_qualified_reads) * 100 / float(total_raw_reads)) + '%'
    no_human_reads_perc = '%.2f' % (float(int(no_human_reads) * 100) / float(int(total_raw_reads))) + '%'
    micro_reads = sequencing_info_list[11]
    micro_reads_perc = '%.2f' % (float(int(micro_reads) * 100) / float(int(total_raw_reads))) + '%'
    unmap_reads = str(int(no_human_reads) - int(micro_reads))
    unmap_reads_perc = '%.2f' % (float(int(unmap_reads) * 100) / float(int(total_raw_reads))) + '%'

    if os.path.exists(read_len_png_dir):
        img_len = Image(read_len_png_dir)
        img_len.drawHeight = 80
        img_len.drawWidth = 200
    else:
        img_len = 'no Figure'

    if os.path.exists(avg_quality_png_dir):
        img_qual = Image(avg_quality_png_dir)
        img_qual.drawHeight = 80
        img_qual.drawWidth = 200
    else:
        img_qual = 'no Figure'

    stylesheet = getSampleStyleSheet()
    normalStyle = stylesheet['Normal']

    #text = '<para autoLeading="off" fontSize=11><b><font face="msyh">四、测序质控</font></b></para>'
    #story.append(KeepTogether(Paragraph(text, normalStyle)))

    component_data = [['四、测序质控', '',''],
                      ['测序平台：', platform, ''],
                      #['总reads数', total_qualified_reads, img_len],
                      ['总reads数', total_raw_reads, img_len],
                      #['过滤去重后reads数(百分比)：', total_qualified_reads + ' (' + qualified_reads_perc + ')', ''],
                      ['人源reads数：', human_reads, ''],
                      #['  > 非人源reads总数(百分比)：', no_human_reads + ' (' + no_human_reads_perc + ')', ''],

                      ['微生物reads数', micro_reads, img_qual],
                      #['    >> Unmapped_reads数(百分比)：', unmap_reads + ' (' + unmap_reads_perc + ')', ''],
                      ['用于鉴定的reads平均长度：', read_avg_len, ''],
                      #['用于鉴定的reads平均质量：', avg_quality, '']]
                    ]
    component_table = Table(component_data, colWidths=[140, 90, 220], rowHeights=[46, 20] + [46] * 4 )
    component_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'msyh'),  # 整个表格字体
        ('FONTSIZE', (0, 0), (-1, -1), 8),  # 整个表格字体大小
        ('FONTSIZE', (0, 0), (-1, 0), 11),  # 第一行字体大小
        #('BOX', (0, 0), (-1, 0), 0.25, colors.white),
        #('LINEBEFORE', (0, 0), (-1, 0), 0.1, colors.white),  # 第一行表格颜色
        #('LINEBEFORE', (0, 1), (-1, -1), 0.1, colors.lightgrey),  # 从第2行设置表格左边线颜色为灰色，线宽为0.1
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),  # 设置表格内文字颜色
        ('SPAN', (0, 0), (2, 0)),  # 合并第1行第一二三列
        ('SPAN', (1, 1), (2, 1)),  # 合并第2行第二三列
        ('SPAN', (2, 2), (2, 3)),  # 合并第三列第3、4行
        ('SPAN', (2, 4), (2, 5)),  # 合并第三列后五行
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # 对齐
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 对齐
        #('TEXTCOLOR', (0, 5), (-1, 5), colors.darkred),  # 设置表格内文字颜色
        #('TEXTCOLOR', (0, 3), (-1, 3), colors.blue),  # 设置表格内文字颜色
        ('GRID', (0, 1), (-1, -1), 0.1, colors.grey),  # 设置表格框线为灰色，线宽为0.5
    ]))
    story.append(KeepTogether(component_table))

    return story


def _main_report_page(story,
                      virus_pos_speices_list,
                      bacteria_pos_speices_list,
                      eukaryote_pos_speices_list,
                      armgene_pos_speices_list, c):

    # 报告首页
    stylesheet = getSampleStyleSheet()
    normalStyle = stylesheet['Normal']
    text = '<para autoLeading="off" fontSize=11><b><font face="msyh">二、检测结果</font></b><br/><br/></para>'
    story.append(Paragraph(text, normalStyle))

    # 自动生成注释列表
    species_translate_dict = {}
    species_annotation_dict = {}

    with open(c.SPECIES_TRANSLATE) as file:
        for line in file:
            species_translate_dict[line.split('\t')[0]] = line.split('\t')[3].strip()

    with open(c.SPECIES_ANNOTATION) as file:
        for line in file:
            species_annotation_dict[line.split('\t')[0]] = line.split('\t')[2].strip()

    pos_txid_li = []
    for species in virus_pos_speices_list:
        pos_txid_li.append(species[2])
    for species in bacteria_pos_speices_list:
        pos_txid_li.append(species[2])
    for species in eukaryote_pos_speices_list:
        pos_txid_li.append(species[2])

    if len(pos_txid_li) == 0:
        pos_chn_name_str = '无'.decode('utf-8')
        pos_chn_annotation_str = '\n采用MAPMI技术对该样品进行检测，在方法检测能力和检测范围内，未检测到相关病原微生物。'.decode('utf-8')
    elif len(pos_txid_li) >= 1:
        pos_chn_name_str = ''
        pos_chn_annotation_str = '【阳性指标说明】：\n\n'.decode('utf-8')

        if pos_txid_li[0] in species_translate_dict.keys():
            n = 1
            for species_access_no in pos_txid_li:
                try:
                    pos_chn_name_str = pos_chn_name_str + species_translate_dict[species_access_no].decode(
                        'utf-8') + '、'.decode('utf-8')
                except KeyError:
                    pos_chn_name_str = pos_chn_name_str + str(species_access_no).decode(
                        'utf-8') + '、'.decode('utf-8')

                try:
                    pos_chn_annotation_str = pos_chn_annotation_str + str(n) + '. ' + species_translate_dict[
                        species_access_no].decode('utf-8') + '：'.decode('utf-8') + species_annotation_dict[
                                                 species_access_no].decode('utf-8') + '\n\n'
                except KeyError:
                    try:
                        pos_chn_annotation_str = pos_chn_annotation_str + str(n) + '. ' + species_translate_dict[
                            species_access_no].decode('utf-8') + '：无注释。\n\n'.decode('utf-8')
                    except KeyError:
                        pos_chn_annotation_str = pos_chn_annotation_str + str(n) + '. ' + str(species_access_no).decode(
                            'utf-8') + '：无注释。\n\n'.decode('utf-8')

                n += 1

        else:
            pos_chn_name_str = '无'.decode('utf-8')
            pos_chn_annotation_str = '\n采用MAPMI技术对该样品进行检测，在方法检测能力和检测范围内，未检测到相关病原微生物。'.decode('utf-8')

    pos_chn_name_str = pos_chn_name_str.rstrip(u'\u3001').replace('\n', '<br/>')
    pos_chn_annotation_str = pos_chn_annotation_str.rstrip('\n').replace('\n', '<br/>')

    table_str_s = getSampleStyleSheet()
    table_str_s = stylesheet['Normal']
    table_str_s.wordWrap = 'CJK'
    table_str_s.fontName = 'msyh'
    table_str_s.fontSize = 8

    cjk_pos_chn_name_str = Paragraph(pos_chn_name_str, table_str_s)
    cjk_pos_chn_annotation_str = Paragraph(pos_chn_annotation_str, table_str_s)

    notation = '置信度：根据序列比对，综合评价在样品中鉴定该病原体的可信度。'
    component_data = [
                      ['1-检出<高置信度>阳性指标'],
                      [cjk_pos_chn_name_str],
                      ['2-检出<中置信度>阳性指标'],
                      ['无'],
                      ['3-检出<疑似>阳性指标'],
                      ['无'],
                      [cjk_pos_chn_annotation_str],
                      [notation]]
    component_table = Table(component_data, colWidths=[450], rowHeights=[18, 40, 18, 40, 18, 25, 450, 30])
    component_table.setStyle(TableStyle([
        #('SPAN', (0, 0), (-1, 0)),  # 合并第一行所有列
        ('SPAN', (0, -1), (-1, -1)),  # 合并最后一行所有列
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # 对齐
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 对齐
        ('VALIGN', (0, 6), (-1, 6), 'TOP'),  # 对齐
        ('FONTNAME', (0, 0), (-1, -1), 'msyh'),  # 整个表格字体
        ('FONTSIZE', (0, 0), (-1, -1), 8),  # 整个表格字体大小
        #('FONTSIZE', (0, 0), (0, 0), 10),  # 第一行字体大小
        ('FONTSIZE', (0, -1), (-1, -1), 6),  # 最后一行字体大小
        #('ALIGN', (0, 0), (-1, 0), 'CENTER'),  # 第一行水平居中
        ('LINEBEFORE', (0, 0), (-1, -1), 0.1, colors.lightgrey),  # 设置表格左边线颜色为灰色，线宽为0.1
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),  # 设置表格内文字颜色
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.grey),  # 设置表格内文字颜色
        #('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),  # 设置第一行背景颜色
        ('GRID', (0, 0), (-1, -1), 0.1, colors.grey),  # 设置表格框线为灰色，线宽为0.5
    ]))
    story.append(component_table)
    story.append(PageBreak())

    return story

def _build_no_suspect_list(story):
    '###############附录部分：补充报告-疑似病原信息##################'
    stylesheet = getSampleStyleSheet()
    normalStyle = stylesheet['Normal']
    text = '<para autoLeading="off" fontSize=11 color=black><b><font face="msyh">附录二-[补充报告]</font></b><br/><br/></para>'
    nothing_text = '<para autoLeading="off" fontSize=11 color=black><b><font face="msyh">无</font></b><br/></para>'
    nothing_str = text + nothing_text
    story.append(KeepTogether(Paragraph(nothing_str, normalStyle)))

    return story

def _build_suspect_list(story,
                        suspected_speices_list):
    
    def construct_sketchy_list(VBE_flag, pos_speices_list, story):

        table_str_s = getSampleStyleSheet()
        table_str_s = stylesheet['Normal']
        table_str_s.wordWrap = 'CJK'
        table_str_s.fontName = 'msyh'
        table_str_s.fontSize = 8

        component_data = [[VBE_flag, '', ''],
            ['名称', 'Name', '检出序列数']]
        for species in pos_speices_list:
            txid = species[0]
            sciName = species[1]
            species_chinese_name = species[3]
            total_reads_num = species[6]
            element = [Paragraph(species_chinese_name, table_str_s),
                        Paragraph(sciName, table_str_s),
                        total_reads_num]
            component_data.append(element)

        return component_data

    '###############附录部分：补充报告-疑似病原信息##################'
    stylesheet = getSampleStyleSheet()
    normalStyle = stylesheet['Normal']
    text = '<para autoLeading="off" fontSize=11 color=black><b><font face="msyh">附录二-[补充报告]</font></b><br/><br/></para>'
    story.append(KeepTogether(Paragraph(text, normalStyle)))

    stylesheet.add(
        ParagraphStyle(name='indentlist',
                       parent=stylesheet['Normal'],
                       fontName="msyh",
                       fontSize=10,
                       textColor='black',
                       leading=16,                # 行间距
                       spaceBefore=0,             # 段前间距
                       spaceAfter=0,             # 段后间距
                       leftIndent=20,              # 左缩进
                       rightIndent=0,             # 右缩进
                       firstLineIndent=-20,        # 首行缩进，每个汉字为10
                       alignment=TA_JUSTIFY,      # 对齐方式
                       )
                    )
    body2 = stylesheet['indentlist']
    body2.wordWrap = 'CJK'
    text = '<para autoLeading="off" fontSize=10><b><font face="msyh">声明：</font></b><br/></para>'
    story.append(Paragraph(text, body2))

    text1 = '<para>&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;1. 该补充报告列表为样本中检出但未达到阳性指标判定标准的潜在致病微生物。</para>'
    text2 = '<para>&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;2. 该补充报告仅供临床参考，该部分不报告耐药基因。<br/><br/></para>'

    story.append(Paragraph(text1, body2))
    story.append(Paragraph(text2, body2))

    vir_species_list, bac_species_list, euk_species_list = [],[],[] 
    for ele in suspected_speices_list:
        ktype = ele[2]
        ## 完成NC扣除和高风险病原过滤后，根据cover_len;unq_reads;cover_perc筛选？
        if ktype == 'V':
            vir_species_list.append(ele)
        elif ktype == 'B':
            bac_species_list.append(ele)
        elif ktype in ['F', 'P']:
            euk_species_list.append(ele)
    sus_index_num = 1
    component_data = []
    begin_index = []
    if len(vir_species_list) > 0:
        vir_str = str(sus_index_num) + '. 病毒筛查结果'
        vir_data = construct_sketchy_list(vir_str, vir_species_list, story)
        component_data += vir_data
        begin_index.append(len(vir_data))
        sus_index_num += 1
    if len(bac_species_list) > 0:
        bac_str = str(sus_index_num) + '. 细菌筛查结果'
        bac_data = construct_sketchy_list(bac_str, bac_species_list, story)
        component_data += bac_data
        if len(begin_index) > 0:
            begin_index.append(begin_index[0] + len(bac_data))
        else:
            begin_index.append(len(bac_data))
        sus_index_num += 1
    if len(euk_species_list) > 0:
        euk_str = str(sus_index_num) + '. 真菌、寄生虫筛查结果'
        euk_data = construct_sketchy_list(euk_str, euk_species_list, story)
        component_data += euk_data
    
    component_table = Table(component_data, colWidths=[100, 230, 50])
    all_style_list = [('FONTNAME', (0, 0), (-1, -1), 'msyh'),  # 整个表格字体
        ('FONTSIZE', (0, 0), (-1, -1), 8),  # 整个表格字体大小
        ('LINEBEFORE', (0, 0), (-1, -1), 0.1, colors.lightgrey),  # 设置表格左边线颜色为灰色，线宽为0.1
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),  # 设置表格内文字颜色
        ('GRID', (0, 0), (-1, -1), 0.1, colors.grey),  # 设置表格框线为灰色，线宽为0.5
        ('SPAN', (0, 0), (-1, 0)),  # 合并第一行所有列
        #('SPAN', (4, 1), (5, 1)),  # 合并第二行最后两列
        #('FONTSIZE', (3, 2), (3, -1), 6),  # 第四列字体大小
        ('FONTSIZE', (1, 2), (1, -1), 7),  # 第二列字体大小
        #('FONTSIZE', (4, 2), (4, -1), 7),  # 第五列字体大小
        ('BACKGROUND', (0, 0), (0, 0), colors.lightblue),  # 设置第一行背景颜色
        ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),  # 对齐
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # 对齐
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 对齐
        ('TEXTCOLOR', (2, 0), (2, -1), colors.blue),  # 设置表格内文字颜色
        #('TEXTCOLOR', (3, 0), (3, -1), colors.darkred),  # 设置表格内文字颜色
    ]
    for every_element in begin_index:
        all_style_list.append(('SPAN', (0, every_element), (-1, every_element)))
        all_style_list.append(('BACKGROUND', (0, every_element), (-1, every_element), colors.lightblue))
    component_table.setStyle(TableStyle(all_style_list))
    story.append(component_table)
    return story

def _build_sketchy_list(story,
                        total_read_count_for_each_txid_dict,
                        virus_pos_speices_list,
                        bacteria_pos_speices_list,
                        eukaryote_pos_speices_list,
                        armgene_pos_speices_list,
                        total_raw_reads, c):

    def concentration_estimate(txid, kingdom, total_reads, total_raw_reads, species_len, c):

        segment_species = ['11320', '11520']
        species_len_true = species_len

        if str(txid) in segment_species:
            species_len_true = species_len * 8

        if kingdom == 'V':
            perc = float(1E+12 * total_reads) / float(total_raw_reads * species_len_true) * 50 * 0.05
        else:
            perc = float(1E+12 * total_reads) / float(total_raw_reads * species_len_true) * 125 * 0.05

        conc_level = Image(c.CONC_BAR_E6)
        if perc >= 1E+6:
            conc_level = Image(c.CONC_BAR_E6)
        elif perc < 1E+6 and perc >= 1E+5:
            conc_level = Image(c.CONC_BAR_E5)
        elif perc < 1E+5 and perc >= 1E+4:
            conc_level = Image(c.CONC_BAR_E4)
        elif perc < 1E+4 and perc >= 1E+3:
            conc_level = Image(c.CONC_BAR_E3)
        elif perc < 1E+3 and perc >= 1E+2:
            conc_level = Image(c.CONC_BAR_E2)
        elif perc < 1E+2:
            conc_level = Image(c.CONC_BAR_E1)

        concentration = '{0:.1E}'.format(perc)
        conc_level.drawHeight = 19.5
        conc_level.drawWidth = 52.7

        return concentration, conc_level

    def construct_sketchy_list(VBE_flag, pos_speices_list, total_read_count_for_each_txid_dict, story):

        def auto_line_break(line, re_len):
            chs_line = line.decode('utf-8')
            if len(chs_line) <= re_len:
                break_line = chs_line
            else:
                if len(chs_line) <= 2 * re_len:
                    break_line = '\n'.join([chs_line[0:re_len], chs_line[re_len:len(chs_line)]])
                else:
                    break_line = '\n'.join(
                        [chs_line[0:re_len], chs_line[re_len:2 * re_len], chs_line[2 * re_len:len(chs_line)]])

            return break_line

        kingdom, sciName, total_reads_num, coverage_len, judge_index, coverage_perc, abundance, conc_img, txid_li = [], [], [], [], [], [], [], [], []
        if VBE_flag.find('耐药基因') >= 0:
            is_arm = True
        else:
            is_arm = False

        for species in pos_speices_list[:20]:
            txid = species[2]
            species_len = int(species[7])
            total_reads = total_read_count_for_each_txid_dict[txid]
            concentration, conc_level = concentration_estimate(txid, species[1], total_reads, total_raw_reads, species_len, c)
            txid_li.append(txid)
            kingdom.append(species[1])
            sciName.append(species[3])
            coverage_len.append(str(species[6]) + ' bp')
            total_reads_num.append(total_reads)

            uniq_efficiency = str(int(float(int(species[4]) * 100) / float(total_reads)))
            try:
                cover_efficiency = str(int(species[6]) / int(species[5]))
            except ZeroDivisionError:
                cover_efficiency = '0'
            judge_index.append(uniq_efficiency + ' | ' + cover_efficiency)
            coverage_perc.append(str(species[8]) + '%')
            abundance.append(concentration)
            conc_img.append(conc_level)

        table_str_s = getSampleStyleSheet()
        table_str_s = stylesheet['Normal']
        table_str_s.wordWrap = 'CJK'
        table_str_s.fontName = 'msyh'
        table_str_s.fontSize = 8

        if is_arm == False:
            species_translate_dict = {}
            with open(c.SPECIES_TRANSLATE) as file:
                for line in file:
                    species_translate_dict[line.split('\t')[0]] = line.split('\t')[3].strip()
            species_translate_dict['IC'] = '内对照'

            component_data = [[VBE_flag, '', '', '', ''],
                              ['名称', 'Name', '检出序列数', '基因组覆盖度', '估测浓度[copies/mL]']]

            if len(kingdom) > 0:
                for i in range(len(kingdom)):
                    try:
                        species_chinese_name = species_translate_dict[txid_li[i]]
                    except KeyError:
                        if txid_li[i] == c.IC_TAXID:
                            species_chinese_name = '内对照'
                        else:
                            species_chinese_name = '-'
                    element = [Paragraph(species_chinese_name, table_str_s),
                               Paragraph(sciName[i][0:28], table_str_s),
                               total_reads_num[i],
                               coverage_len[i] + ' / ' + coverage_perc[i],
                               abundance[i]]

                    component_data.append(element)
            else:
                component_data.append(['-', '-', '-', '-', '-'])
            component_table = Table(component_data, colWidths=[85, 140, 50, 75, 100])
            component_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'msyh'),  # 整个表格字体
                ('FONTSIZE', (0, 0), (-1, -1), 8),  # 整个表格字体大小
                ('LINEBEFORE', (0, 0), (-1, -1), 0.1, colors.lightgrey),  # 设置表格左边线颜色为灰色，线宽为0.1
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),  # 设置表格内文字颜色
                ('GRID', (0, 0), (-1, -1), 0.1, colors.grey),  # 设置表格框线为灰色，线宽为0.5
                ('SPAN', (0, 0), (-1, 0)),  # 合并第一行所有列
                #('SPAN', (4, 1), (5, 1)),  # 合并第二行最后两列
                ('FONTSIZE', (3, 2), (3, -1), 6),  # 第四列字体大小
                ('FONTSIZE', (1, 2), (1, -1), 7),  # 第二列字体大小
                #('FONTSIZE', (4, 2), (4, -1), 7),  # 第五列字体大小
                ('BACKGROUND', (0, 0), (0, 0), colors.lightblue),  # 设置第一行背景颜色
                ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),  # 对齐
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # 对齐
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 对齐
                ('TEXTCOLOR', (2, 0), (2, -1), colors.blue),  # 设置表格内文字颜色
                ('TEXTCOLOR', (3, 0), (3, -1), colors.darkred),  # 设置表格内文字颜色
            ]))
            story.append(component_table)

        else:
            arm_translate_dict = {}

            with open(c.ARM_TRANSLATE) as file:
                for line in file:
                    arm_translate_dict[line.split('\t')[0]] = line.split('\t')[2]

            component_data = [[VBE_flag, '', ''],
                              ['检测到的耐药基因', '基因耐药参考', '检出序列数']]
            if len(kingdom) > 0:
                for i in range(len(kingdom)):
                    element = [Paragraph(sciName[i], table_str_s),
                               Paragraph(arm_translate_dict[txid_li[i]], table_str_s),
                               total_reads_num[i]]

                    component_data.append(element)
            else:
                component_data.append(['-', '-', '-', '', ''])
            component_table = Table(component_data, colWidths=[195, 195, 60, 0, 0])
            component_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, -1), 'msyh'),  # 整个表格字体
                ('FONTSIZE', (0, 0), (-1, -1), 8),  # 整个表格字体大小
                #('FONTSIZE', (0, 0), (0, -1), 6),  # 第一列字体大小
                #('FONTSIZE', (2, 0), (2, -1), 6),  # 第四列字体大小
                ('FONTSIZE', (0, 0), (-1, 1), 8),  # 第一、二 行字体大小
                #('LINEBEFORE', (0, 0), (-1, -1), 0.1, colors.lightgrey),  # 设置表格左边线颜色为灰色，线宽为0.1
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),  # 设置表格内文字颜色
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # 对齐
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # 对齐
                ('GRID', (0, 0), (-1, -1), 0.1, colors.grey),  # 设置表格框线为灰色，线宽为0.5

                ('SPAN', (0, 0), (-1, 0)),  # 合并第一行所有列
                ('BACKGROUND', (0, 0), (0, 0), colors.lightblue),  # 设置第一行背景颜色
                ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),  # 对齐

                ('TEXTCOLOR', (2, 0), (2, -1), colors.blue),  # 设置表格内文字颜色
                #('TEXTCOLOR', (3, 0), (3, -1), colors.darkred),  # 设置表格内文字颜色
            ]))
            story.append(component_table)

        return story

    '###############附录部分：详细技术信息##################'
    # 第二部分
    stylesheet = getSampleStyleSheet()
    normalStyle = stylesheet['Normal']
    text = '<para autoLeading="off" fontSize=11 color=black><b><font face="msyh">三、检测结果列表</font></b><br/><br/></para>'
    story.append(KeepTogether(Paragraph(text, normalStyle)))

    #text = '<para autoLeading="off" fontSize=10><b><font face="msyh">（一）检出阳性病原技术信息</font></b><br/><br/></para>'
    #story.append(Paragraph(text, normalStyle))

    story = construct_sketchy_list('1. 病毒筛查结果',
                                   virus_pos_speices_list, total_read_count_for_each_txid_dict, story)
    story = construct_sketchy_list('2. 细菌筛查结果',
                                   bacteria_pos_speices_list, total_read_count_for_each_txid_dict, story)
    story = construct_sketchy_list('3. 真菌、寄生虫筛查结果',
                                   eukaryote_pos_speices_list, total_read_count_for_each_txid_dict, story)
    story = construct_sketchy_list('4. 耐药基因筛查结果',
                                   armgene_pos_speices_list, total_read_count_for_each_txid_dict, story)

    return story

def _detecting_method_indtroduction(story):
    stylesheet = getSampleStyleSheet()
    normalStyle = stylesheet['Heading2']

    # 添加自定义样式
    stylesheet.add(
        ParagraphStyle(name='body',
                       parent=stylesheet['Normal'],
                       fontName="msyh",
                       fontSize=10,
                       textColor='black',
                       leading=16,                # 行间距
                       spaceBefore=0,             # 段前间距
                       spaceAfter=10,             # 段后间距
                       leftIndent=0,              # 左缩进
                       rightIndent=0,             # 右缩进
                       firstLineIndent=20,        # 首行缩进，每个汉字为10
                       alignment=TA_JUSTIFY,      # 对齐方式
                       )
                    )
    stylesheet.add(
        ParagraphStyle(name='indentlist',
                       parent=stylesheet['Normal'],
                       fontName="msyh",
                       fontSize=10,
                       textColor='black',
                       leading=16,                # 行间距
                       spaceBefore=0,             # 段前间距
                       spaceAfter=0,             # 段后间距
                       leftIndent=20,              # 左缩进
                       rightIndent=0,             # 右缩进
                       firstLineIndent=-10,        # 首行缩进，每个汉字为10
                       alignment=TA_JUSTIFY,      # 对齐方式
                       )
                    )

    body = stylesheet['body']
    body.wordWrap = 'CJK'
    body2 = stylesheet['indentlist']
    body2.wordWrap = 'CJK'
   

    # 检测方法学介绍

    text = '<para autoLeading="off" fontSize=11><b><font face="msyh">五、检测方法学介绍</font></b><br/></para>'
    story.append(Paragraph(text, normalStyle))

    text = '<para autoLeading="off" fontSize=10><b><font face="msyh">（一）检测内容</font></b><br/></para>'
    story.append(Paragraph(text, normalStyle))

    text = '<para>基于二代测序的宏基因组测序技术，直接对样品中' \
    "的核酸进行检测，获得样品中微生物的序列信息，无需提前预判感染微生物，无偏向性的鉴定可疑致病微生物。博奥MAPMI<super rise=9 size=2>TM</super>" \
    "检测基于BioelectronSeq 4000基因测序仪，7374种病毒（涵盖DNA病毒和RNA病毒）、13362种细菌、1659种真菌、153种寄生虫及2500种耐药基因。</para>" 

    story.append(Paragraph(text, body))

    text = '<para autoLeading="off" fontSize=10><b><font face="msyh">（二）检测局限性</font></b><br/></para>'
    story.append(Paragraph(text, normalStyle))

    text1 = '<para>1. 本方法与其它检测方法一样，有自身的检测能力和检测范围，本次检测未报告微生物不代表样'\
            '本中一定不存在致病微生物，并不能排除受检者感染某种病原微生物的可能性，其原因包括但不限'\
            '于： 1). 样品中病原微生物浓度低于检测限； 2). 病原微生物未被涵盖在检测范围内。</para>'
    text2 = '<para>2. 临床研究表明，耐药基因与实际耐药表型并不完全一致，报告中耐药基因检测结果仅供临床参考。</para>'

    story.append(Paragraph(text1, body2))
    story.append(Paragraph(text2, body2))

    text = '<para autoLeading="off" fontSize=10><b><font face="msyh">（三）检测结果说明</font></b><br/></para>'
    story.append(Paragraph(text, normalStyle))

    text1 = "<para>1. 以上检测结果仅供临床参考，不作为临床诊断唯一依据，如有疑义请在收到结果后七个工作日内与我们联系；</para>"
    text2 = "<para>2. 本报告结果仅对本次送检样品负责，报告相关解释需咨询临床医生；</para>"
    #text3 = "<para>3. 本方法与其它检测方法一样，有自身的检测能力和检测范围（即方法局限性），本报告未报告的微生物仅代表在本方法的检测能力下无阳性物种报告，并不能排除受检者感染某种病原微生物的可能性；</para>"
    text4 = "<para>3. 本检测对该结果保密并依法保护受检者隐私，但因受检者个人原因出现信息外泄，本实验室不承担相应责任。</para>"
    story.append(Paragraph(text1, body2))
    story.append(Paragraph(text2, body2))
    #story.append(Paragraph(text3, body2))
    story.append(Paragraph(text4, body2))

    return story

def create_pdf(samplename,
               total_read_count_for_each_txid_dict,
               virus_pos_speices_list,
               bacteria_pos_speices_list,
               eukaryote_pos_speices_list,
               armgene_pos_speices_list,
               suspected_speices_list,
               fig_folder,
               output,
               sequencing_info_list,
               sample_clinic_info_list,
               print_suspect_species, platform, c):
    curr_date = time.strftime('%Y-%m-%d %H:%M:%S')

    story = []
    stylesheet = getSampleStyleSheet()
    normalStyle = stylesheet['Normal']

    '###############首页、页眉页脚##################'
    patient_info_file = output.replace('_final_report.pdf', '.ClinicInfo')
    patient_info_dict = clinic_info_read_store(samplename, patient_info_file, sample_clinic_info_list)
    patient_name = patient_info_dict['name']

    if patient_name in ['', '-', 'undefined']:
        patient_name = samplename
    # title1 = '''<para autoLeading="off" fontSize=24 color=black align=center>
    #     <br/><br/><br/><b><font face="simsun" >中 南 大 学 湘 雅 医 学 检 验 所</font></b><br/><br/></para>'''
    title1 = '''<para autoLeading="off" fontSize=24 color=black align=center>
             <br/><br/><br/>中 南 大 学 湘 雅 医 学 检 验 所<br/><br/><br/></para>'''

    # mystyle = ParagraphStyle(name="my_style", fontName="simsun", alignment=TA_JUSTIFY, leftIndent=50)
    title1_style = ParagraphStyle(name="title1_style", fontName="simsun")

    # title2 = '''<para autoLeading="off" fontSize=12 color=black align=center >
    #         <br/><font face="Times">Personalized Medical Molecular Testing Laboratory, XiangYa medical laboratory, Central South University</font></para>'''
    title2 = '''<para autoLeading="off" fontSize=12 color=black>
            <br/><font face="Times">Personalized Medical Molecular Testing Laboratory, XiangYa medical laboratory, Central South University</font>
            </br></br></br></br></br></para>'''
    title2_style = ParagraphStyle(name="title2_style",  leftIndent=-40, rightIndent=-50, spaceAfter=15)
    title3 = '''<para autoLeading="off" fontSize=13 color=grey align=center><font face="msyh"><br/>
        <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
        <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
        <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
        姓名：{0} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;日期：{1}</font></para>'''.format(patient_name, curr_date.split()[0])

    # title2 = '''<para autoLeading="off" fontSize=13 color=grey align=center>
    #         <br/><br/><br/><br/><br/><br/><b><font face="msyh">北京博奥医学检验所</font></b></para>'''
    story.append(Paragraph(title1, title1_style))
    story.append(Paragraph(title2, title2_style))
    story.append(Paragraph(title3, normalStyle))
    # story.append(Paragraph(title2, normalStyle))
    # 首页换页
    story.append(PageBreak())

    '###############第一大部分：临床样品信息显示##################'
    story = _sample_clinic_info(samplename, story, patient_info_file, patient_info_dict)
    # 第一部分换页
    story.append(PageBreak())

    '###############第二大部分：MAPMI检测结果##################'
    story = _main_report_page(story,
                              virus_pos_speices_list,
                              bacteria_pos_speices_list,
                              eukaryote_pos_speices_list,
                              armgene_pos_speices_list, c)
    '###############第三大部分：病原技术信息汇总##################'
    # （一）检出阳性指标技术信息

    summarize_file = os.path.join(os.path.dirname(output),
                                  os.path.basename(output).replace('_final_report.pdf', '.summarize'))
    with open(summarize_file) as file:
        for line in file:
            # if the path contain 'raw', the program will report error, so change match rules from 'raw' to 'raw reads'
            if line.find('raw reads') > 0:
                total_raw_reads = int(line.split('=')[1].strip())

    story = _build_sketchy_list(story,
                                total_read_count_for_each_txid_dict,
                                virus_pos_speices_list,
                                bacteria_pos_speices_list,
                                eukaryote_pos_speices_list,
                                armgene_pos_speices_list,
                                total_raw_reads, c)

    # （四）测序质控信息
    #story.append(PageBreak())
    story = _sequencing_statistics_info(story, sequencing_info_list)
    # 第（五）部分换页
    story.append(PageBreak())

    #检测方法学介绍
    story = _detecting_method_indtroduction(story)
    
    # 附录部分换页
    story.append(PageBreak())

    text = '<para autoLeading="off" fontSize=11 color=black><b><font face="msyh">附录一-[阳性指标详细信息]</font></b><br/><br/></para>'
    story.append(Paragraph(text, normalStyle))

    # （附录）详细技术信息汇总
    text = '<para autoLeading="off" fontSize=10 color=black><b><font face="msyh">（一）阳性病毒详细技术信息</font></b><br/><br/></para>'
    story.append(Paragraph(text, normalStyle))

    if len(virus_pos_speices_list) > 0:
        story = iter_draw_tables(total_read_count_for_each_txid_dict, virus_pos_speices_list, story, fig_folder)
        text = '<para><br/><br/></para>'
        story.append(Paragraph(text, normalStyle))
    else:
        text = '<para autoLeading="off" fontSize=9 color=black><br/><b><font face="msyh">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;未检测到相关病毒。</font></b><br/><br/></para>'
        story.append(Paragraph(text, normalStyle))

    text = '<para autoLeading="off" fontSize=10 color=black><b><font face="msyh">（二）阳性细菌详细技术信息</font></b><br/><br/></para>'
    story.append(KeepTogether(Paragraph(text, normalStyle)))
    if len(bacteria_pos_speices_list) > 0:
        story = iter_draw_tables(total_read_count_for_each_txid_dict, bacteria_pos_speices_list, story, fig_folder)
        text = '<para><br/><br/></para>'
        story.append(KeepTogether(Paragraph(text, normalStyle)))
    else:
        text = '<para autoLeading="off" fontSize=9 color=black><b><font face="msyh">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;未检测到相关细菌。</font></b><br/><br/></para>'
        story.append(KeepTogether(Paragraph(text, normalStyle)))

    text = '<para autoLeading="off" fontSize=10 color=black><b><font face="msyh">（三）阳性真菌、寄生虫详细技术信息</font></b><br/><br/></para>'
    story.append(KeepTogether(Paragraph(text, normalStyle)))
    if len(eukaryote_pos_speices_list) > 0:
        story = iter_draw_tables(total_read_count_for_each_txid_dict, eukaryote_pos_speices_list, story, fig_folder)
        text = '<para><br/><br/></para>'
        story.append(KeepTogether(Paragraph(text, normalStyle)))
    else:
        text = '<para autoLeading="off" fontSize=9 color=black><b><font face="msyh">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;未检测到相关真菌、寄生虫。</font></b><br/><br/></para>'
        story.append(KeepTogether(Paragraph(text, normalStyle)))

    text = '<para autoLeading="off" fontSize=10 color=black><b><font face="msyh">（四）阳性耐药基因详细技术信息</font></b><br/><br/></para>'
    story.append(KeepTogether(Paragraph(text, normalStyle)))
    if len(armgene_pos_speices_list) > 0:
        story = iter_draw_tables(total_read_count_for_each_txid_dict, armgene_pos_speices_list, story, fig_folder)
        text = '<para><br/><br/></para>'
        story.append(KeepTogether(Paragraph(text, normalStyle)))
    else:
        text = '<para autoLeading="off" fontSize=9 color=black><b><font face="msyh">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;未检测到相关耐药基因。</font></b><br/><br/></para>'
        story.append(KeepTogether(Paragraph(text, normalStyle)))
    
    # 补充报告部分换页
    # 六、补充报告展示模块
    #print(virus_pos_speices_list[0])
    #print(suspected_speices_list[0])
    #是否展示补充报告模块（疑似病原）
    #print_suspect_species = True
    if print_suspect_species == "true":
        if bool(suspected_speices_list) and len(suspected_speices_list) > 0:
            story.append(PageBreak())
            story = _build_suspect_list(story, suspected_speices_list)
        else:
            story.append(PageBreak())
            story = _build_no_suspect_list(story)

    '###############写入结果结束##################'
    story1 = story[:]
    tmp_doc = SimpleDocTemplate(output.replace('.pdf', '_tmp.pdf'))
    tmp_doc.build(story1, onFirstPage=_on_page_start, onLaterPages=_header_footer)
    #pdfReader = PdfFileReader(output.replace('.pdf', '_tmp.pdf'))
    #global g_page_total
    #g_page_total = pdfReader.getNumPages()-1
    os.remove(output.replace('.pdf', '_tmp.pdf'))
    doc = SimpleDocTemplate(output)
    if platform == 'BioelectronSeq4000':
        doc.build(story, onFirstPage=_on_page_start, onLaterPages=_header_footer_second)
    else:
        # to avoid the bug due to lower version of reportlab and error: tostring() has been removed. Please call tobytes() instead
        from PIL import Image
        Image.Image.tostring = Image.Image.tobytes
        doc.build(story, onFirstPage=_on_page_start_manu, onLaterPages=_header_footer_second)


def decompose_final_result(final_result_dir):
    '''
    [0] Rank                    1
    [1] Kingdom                 'V'
    [2] txid                    '290028'
    [3] sciName                 'Human_coronavirus_HKU1'
    [4] uniq_reads_num          229
    [5] total_reads_num         452
    [6] coverage_len            1051
    [7] coverage_ref_len        2985744
    [8] coverage_percent        3.52
    [9] depth_total             46471
    [10] depth_avg              1051
    [11] nt_title               DQ415906.1|29857|Human coronavirus HKU1 strain N9 genotype A, complete genome
    [12] avg_hit_num            1
    [13] reads_distr            0.28
    '''

    decompose_list = []
    with open(final_result_dir) as file:
        for line in file:
            if line.startswith('#'):
                rank = int(line.split('~')[0].replace('#', ''))
                kingdom = line.split('~')[1]
                taxid = line.split('~')[2]
                if taxid == '77643':
                    sciname = 'Mycobacterium_tuberculosis_complex'
                else:
                    sciname = line.split('~')[3]
                judge_index = int(line.split('~')[4].split('<')[0].replace(' unique reads hit', '').replace('[', ''))
                avg_hit_num = int(line.split('~')[4].split('<')[1].replace('>]', ''))
                # |分隔符前后数字分别表示species level和accession level的hit reads数量，取0表示在最终judgement csv中取species level的总hitreads数
                total_reads_num = int(line.split('~')[5].replace(' reads hit', '').split('|')[0])
                try:
                    coverage_len = int(line.split('~')[6].replace('coverage:', '').split('/')[0])
                    coverage_ref_len = int(line.split('~')[6].replace('coverage:', '').split('/')[1].split('=')[0])
                    coverage_percent = float(line.split('~')[6].replace('coverage:', '').split('=')[1].replace('%', ''))
                    depth_total = int(line.split('~')[7].replace('depth:', '').split('/')[0])
                    depth_avg = float(line.split('~')[7].replace('depth:', '').split('=')[1])
                    nt_title = line.split('~')[8].replace('Title:', '').split('|')[0] + '|' + \
                               line.split('~')[8].replace('Title:', '').strip().split('|')[2][0:80]
                    reads_distr = line.split('~')[9].replace('reads_distr:', '')
                except ValueError:
                    continue
                except Exception:
                    coverage_len = 0
                    coverage_ref_len = 0
                    coverage_percent = 0.0
                    depth_total = 0
                    depth_avg = 0.0
                    nt_title = 'N/A'
                    reads_distr = 'N/A'

                decompose_list.append([rank, kingdom, taxid, sciname, judge_index, total_reads_num, coverage_len, coverage_ref_len, coverage_percent, depth_total, depth_avg, nt_title, avg_hit_num, reads_distr])

    return decompose_list


def write_summarize_result(virus_pos_speices_list,
                           bacteria_pos_speices_list,
                           eukaryote_pos_speices_list,
                           armgene_pos_speices_list,
                           final_result_file):
    def write_in(pos_speices_list, w):
        for i in range(len(pos_speices_list)):
            item = pos_speices_list[i]
            item[0] = '#' + str(i + 1)
            w.write('\t'.join(str(i) for i in item) + '\n')
        w.write('\n')

    w = open(final_result_file, 'w')
    w.write('\t'.join(['rank', 'Kingdom', 'txid', 'sciName', 'uniq_reads_num', 'total_reads_num',
                       'coverage_len', 'coverage_ref_len', 'coverage_percent', 'depth_total',
                       'depth_avg', 'avg_hit_num']) + '\n')

    write_in(virus_pos_speices_list, w)
    write_in(bacteria_pos_speices_list, w)
    write_in(eukaryote_pos_speices_list, w)
    write_in(armgene_pos_speices_list, w)
    w.close()


def group_judge_positive(manual_pos_species_list, total_read_count_for_each_txid_dict, decompose_list, judgement_record_file, sensitive_param_arr, final_taxonomy_detail_file, c):
    '''
    [0] Rank                    1
    [1] Kingdom                 'V'
    [2] txid                    '290028'
    [3] sciName                 'Human_coronavirus_HKU1'
    [4] uniq_reads_num          229
    [5] total_reads_num         452
    [6] coverage_len            1051
    [7] coverage_ref_len        2985744
    [8] coverage_percent        3.52
    [9] depth_total             46471
    [10] depth_avg              1051
    [11] nt_title               DQ415906.1|29857|Human coronavirus HKU1 strain N9 genotype A, complete genome
    [12] avg_hit_num            1
    [13] reads_distr            0.28
    '''

    def get_hazard_level(species_txid, taxonomy_detail, hazard_level_dict):
        hazard_level = np.nan
        g_hazard_level = ''
        s_hazard_level = ''
        sub_species = []
        if species_txid in taxonomy_detail.keys():
            #kingdom = taxonomy_detail[species_txid][0]
            genus_txid = taxonomy_detail[species_txid][1]
            txid = taxonomy_detail[species_txid][2]
            for id in hazard_level_dict.keys():
                #h_kingdom = hazard_level_dict[id][0]
                h_rank = hazard_level_dict[id][1]
                h_hazard_level = hazard_level_dict[id][2]
                h_current_name = hazard_level_dict[id][3]
                if h_rank == 'genus' and str(genus_txid) == str(id):
                    g_hazard_level = 'genus: ' + h_hazard_level
                elif h_rank == 'species' and str(species_txid) == str(id):
                    s_hazard_level = 'species: ' + h_hazard_level
                elif h_rank != 'species' and h_rank != 'genus' and  (str(id) in txid.split(',')):
                    sub_species.append('subspecies: '+h_current_name + '-' + h_hazard_level)
            if g_hazard_level != '':
                hazard_level = g_hazard_level
            elif s_hazard_level != '':
                hazard_level = s_hazard_level
            elif len(sub_species) != 0:
                sub_hazard_level = ';'.join(sub_species)
                hazard_level = sub_hazard_level
        return hazard_level

    def nonsense_virus_filter(txid, sci_name, c):
        nonsense_virus_list = c.FILTER_VIRUS_NAME
        not_nonsense_virus = True

        for name in nonsense_virus_list:
            if sci_name.find(name) >= 0 and txid != c.IC_TAXID:
                not_nonsense_virus = False

        return not_nonsense_virus

    def sys_species_filter(txid, c):
        sys_species_list = c.SYS_SPECIES
        not_sys_species = True

        if txid in sys_species_list:
            not_sys_species = False

        return not_sys_species

    def cover_efficiency_judge(txid, cover_efficiency, coverage, COVER_EFFICIENCY_THRESHOLD, c):
        try:
            txid_int = int(txid)
        except ValueError:
            txid_int = txid

        if txid_int in c.SPECIAL_SPECIES:
            cover_efficiency_OK = (cover_efficiency >= COVER_EFFICIENCY_THRESHOLD and coverage >= 0.15) or coverage >= 1
        else:
            cover_efficiency_OK = (cover_efficiency >= COVER_EFFICIENCY_THRESHOLD and coverage >= 0.001) or coverage >= 1

        return cover_efficiency_OK

    def uniq_efficiency_judge(txid, uniq_efficiency, UNIQ_EFFICIENCY_THRESHOLD_NORMAL, c):
        if txid in c.SPECIAL_UNIQ_EFFICIENCY:
            uniq_efficiency_OK = (uniq_efficiency >= c.UNIQ_EFFICIENCY_THRESHOLD_SPECIAL)
        else:
            uniq_efficiency_OK = (uniq_efficiency >= UNIQ_EFFICIENCY_THRESHOLD_NORMAL)

        return uniq_efficiency_OK

    #def initialize_bg_species(c):
    #    mapmi_bg_species_dict = {}
    #    with open(c.MAPMI_BG_SPECIES) as file:
    #        for line in file:
    #            txid = line.split()[0]
    #            if txid != 'txid':
    #                frequency = int(line.split()[3])
    #                cover_len_avg = int(line.split()[4])
    #                cover_len_max = int(line.split()[5])
    #                uniq_effi_avg = float('%.3f' % float(line.split()[6]))
    #                uniq_effi_max = float('%.3f' % float(line.split()[7]))
    #                cover_effi_avg = float(line.split()[8])
    #                cover_effi_max = float(line.split()[9].strip())
    #                mapmi_bg_species_dict[txid] = [
    #                    frequency, (cover_len_avg, cover_len_max), (uniq_effi_avg, uniq_effi_max),
    #                    (cover_effi_avg, cover_effi_max)]
    #    return mapmi_bg_species_dict

    def initialize_bg_species(c):
        bg_species_df = pd.DataFrame()
        if os.path.exists(c.MAPMI_BG_SPECIES):
            bg_species_df = pd.read_csv(c.MAPMI_BG_SPECIES, sep='\t', index_col='txid', converters=dict(cover_length=literal_eval))
        else:
            raise IOError("File not found! %s , please check installation." % c.MAPMI_BG_SPECIES)
        if bg_species_df.shape[0] > 0:
            return bg_species_df
        else:
            raise ValueError("Length of bg_species_df lt 1! Check %s, it should be a table separated by tab" % c.MAPMI_BG_SPECIES)

    def confidence_index_calc(kingdom, cover_len, cover_effi, uniq_reads, uniq_effi, bg_cover_len, reads_distr):
        # calculate a confidence index for each positive species to help judge
        if txid in c.SPECIAL_UNIQ_EFFICIENCY:
            uniq_effi = 0.3
        if kingdom == 'B' or kingdom == 'F' or kingdom == 'P':
            CI_cover_len = max((cover_len - bg_cover_len) / 10000.0, 0)
            CI_cover_effi = max(cover_effi / 100.0, 0.3)
            confidence_index = CI_cover_effi * CI_cover_len * uniq_effi / reads_distr
        elif kingdom == 'V':
            CI_cover_len = max((uniq_reads - bg_cover_len / 100.0) / 5.0, 0)
            CI_cover_effi = max(cover_effi / 100.0, 0.3)
            confidence_index = CI_cover_effi * CI_cover_len * uniq_effi
        elif kingdom == 'R':
            confidence_index = uniq_reads / 3.0 * uniq_effi

        return confidence_index

    # Initialize the background species:
    mapmi_bg_species = initialize_bg_species(c)

    species_translate_dict = {}
    pathogen_level_dict = {}
    hazard_level_dict={}
    taxonomy_detail={}
    # Initialize the species name translation mapping file:
    with open(c.SPECIES_TRANSLATE) as file:
        for line in file:
            line_array = line.strip().split('\t')
            species_translate_dict[line_array[0]] = line_array[3]
            pathogen_level_dict[line_array[0]] = line_array[4]
    with open(c.HAZARD_LEVEL) as file:
        for line in file:
            if line.startswith('#'):
                continue
            line_array = line.strip().split('\t')
            hazard_level_dict[line_array[0]] = [line_array[1], line_array[2], line_array[5], line_array[3]]
    with open (final_taxonomy_detail_file) as file:
        for line in file:
            line_array = line.strip().split('\t')
            taxonomy_detail[line_array[0]] =[line_array[1], line_array[2], line_array[3]]

    virus_pos_speices_list = []
    bacteria_pos_speices_list = []
    eukaryote_pos_speices_list = []
    armgene_pos_speices_list = []
    judgement_record_list = []

    HIT_COVERAGE_THRESHOLD_V = int(sensitive_param_arr[0])
    HIT_COVERAGE_THRESHOLD_B = int(sensitive_param_arr[1])
    HIT_COVERAGE_THRESHOLD_E = int(sensitive_param_arr[2])
    HIT_COVERAGE_THRESHOLD_R = int(sensitive_param_arr[3])
    UNIQ_READS_THRESHOLD_V = int(sensitive_param_arr[4])
    UNIQ_READS_THRESHOLD_B = int(sensitive_param_arr[5])
    UNIQ_READS_THRESHOLD_E = int(sensitive_param_arr[6])
    UNIQ_READS_THRESHOLD_R = int(sensitive_param_arr[7])
    UNIQ_EFFICIENCY_THRESHOLD_NORMAL = float(sensitive_param_arr[8])
    COVER_EFFICIENCY_THRESHOLD = int(sensitive_param_arr[9])

    for decompose_sub_list in decompose_list:
        txid = decompose_sub_list[2]
        try:
            chinese_name = species_translate_dict[txid]
        except:
            chinese_name = 'N/A'
        try:
            pathogen_level = pathogen_level_dict[txid]
        except:
            pathogen_level = 'N/A'
        # hit uniq_reads and coverage can not be less than a preset threshold
        uniq_reads = decompose_sub_list[4]
        hit_reads = decompose_sub_list[5]
        coverage_len = decompose_sub_list[6]
        coverage = decompose_sub_list[8]
        # hit accession length can not be less than a preset value
        ref_length = decompose_sub_list[7]
        try:
            reads_distr = float(decompose_sub_list[13].replace('\n', ''))
        except ValueError:
            reads_distr = 1.0

        try:
            uniq_efficiency = float(uniq_reads) / float(total_read_count_for_each_txid_dict[txid])
            cover_efficiency = int(coverage_len) / int(hit_reads)
        except KeyError:
            uniq_efficiency = float(decompose_sub_list[4]) / 20.0
            cover_efficiency = int(coverage_len) / 20
        except ZeroDivisionError:
            '''
                hit_reads == 0, only BUG
            '''
            uniq_efficiency = float(uniq_reads) / float(total_read_count_for_each_txid_dict[txid])
            cover_efficiency = 0

        cover_efficiency_OK = cover_efficiency_judge(txid, cover_efficiency, coverage, COVER_EFFICIENCY_THRESHOLD, c)
        uniq_efficiency_OK = uniq_efficiency_judge(txid, uniq_efficiency, UNIQ_EFFICIENCY_THRESHOLD_NORMAL, c)


        if str(txid) in mapmi_bg_species.index:
            bg_species_param_list = mapmi_bg_species.loc[str(txid)][2:8].tolist()
        else:
            bg_species_param_list = [0, '[0, 0, 0, 0, 0]', '[0, 0, 0, 0, 0]', [0, 0, 0, 0, 0], '[0, 0, 0, 0, 0]', '[0, 0, 0, 0, 0]']

        confidence_index = confidence_index_calc(decompose_sub_list[1], coverage_len, cover_efficiency, uniq_reads,
                                                 uniq_efficiency, bg_species_param_list[3][4], reads_distr)

        #manual_pos_species_list = ['60133', '712710', '2697049', '76775', 'AR4985209']
        if len(manual_pos_species_list) == 0:
            #print("de: %s, %d > %d, %d > %d %d, %d, %s, %s, " % (decompose_sub_list[1], uniq_reads, UNIQ_READS_THRESHOLD_V, coverage_len, HIT_COVERAGE_THRESHOLD_V, bg_species_param_list[1][1], ref_length, str(uniq_efficiency_OK), str(cover_efficiency_OK)))
            positive_virus = decompose_sub_list[1] == 'V' and \
                             uniq_reads >= UNIQ_READS_THRESHOLD_V and \
                             coverage_len >= HIT_COVERAGE_THRESHOLD_V and \
                             coverage_len >= bg_species_param_list[3][4] and \
                             ref_length > 1000 and \
                             uniq_efficiency_OK and \
                             cover_efficiency_OK and \
                             nonsense_virus_filter(txid, decompose_sub_list[3], c) and \
                             sys_species_filter(txid, c) and \
                             confidence_index >= 0.4

            positive_bacteria = decompose_sub_list[1] == 'B' and \
                                uniq_reads >= UNIQ_READS_THRESHOLD_B and \
                                coverage_len >= HIT_COVERAGE_THRESHOLD_B and \
                                coverage_len >= bg_species_param_list[3][4] and \
                                uniq_efficiency_OK and \
                                cover_efficiency_OK and \
                                sys_species_filter(txid, c) and \
                                confidence_index >= 0.4

            positive_fungi = (decompose_sub_list[1] == 'F' or decompose_sub_list[1] == 'P') and \
                             uniq_reads >= UNIQ_READS_THRESHOLD_E and \
                             coverage_len >= HIT_COVERAGE_THRESHOLD_E and \
                             coverage_len >= bg_species_param_list[3][4] and \
                             uniq_efficiency_OK and \
                             cover_efficiency_OK and \
                             sys_species_filter(txid, c) and \
                             confidence_index >= 0.4

            positive_arm = (decompose_sub_list[1] == 'R') and \
                           uniq_reads >= UNIQ_READS_THRESHOLD_R and \
                           coverage_len >= HIT_COVERAGE_THRESHOLD_R and \
                           confidence_index >= 0.4

        else:
            positive_virus = (decompose_sub_list[1] == 'V') and (txid in manual_pos_species_list)

            positive_bacteria = (decompose_sub_list[1] == 'B') and (txid in manual_pos_species_list)

            positive_fungi = (decompose_sub_list[1] == 'F' or decompose_sub_list[1] == 'P') and (
                        txid in manual_pos_species_list)

            positive_arm = (decompose_sub_list[1] == 'R') and (txid in manual_pos_species_list)

        positive_or_not = 'False'

        if positive_virus:
            if txid != c.IC_TAXID:
                virus_pos_speices_list.append(decompose_sub_list)
            positive_or_not = 'virus_positive'

        elif positive_bacteria:
            bacteria_pos_speices_list.append(decompose_sub_list)
            positive_or_not = 'bacteria_positive'

        elif positive_fungi:
            eukaryote_pos_speices_list.append(decompose_sub_list)
            positive_or_not = 'eukary_positive'

        elif positive_arm:
            armgene_pos_speices_list.append(decompose_sub_list)
            positive_or_not = 'ARM_positive'
        
        hazard_level = get_hazard_level(txid, taxonomy_detail, hazard_level_dict)
        judgement_record_list.append(
            [txid, decompose_sub_list[3], decompose_sub_list[1], chinese_name, pathogen_level, '%.2f' % confidence_index,
             hit_reads, uniq_reads, coverage_len,
             coverage, uniq_efficiency, cover_efficiency, reads_distr, positive_or_not, bg_species_param_list[0],
             bg_species_param_list[1], bg_species_param_list[2], bg_species_param_list[3], bg_species_param_list[4], bg_species_param_list[5], hazard_level])

    judgement_record_list_resort = sorted(judgement_record_list, key=lambda x: x[8], reverse=True)
    list_index = 0
    for item in judgement_record_list_resort:
        item[10] = '%.3f' % item[10]
        #item[15] = [str(item[15][0]), str(item[15][1])]
        #item[16] = ['%.3f' % item[16][0], '%.3f' % item[16][1]]
        #item[17] = ['%.1f' % item[17][0], '%.1f' % item[17][1]]
        #item=[str(x).replace(' ', '') for x in item]
        judgement_record_list_resort[list_index] = item
        list_index += 1
    judge_df = pd.DataFrame(judgement_record_list_resort)
    
    judge_df.columns = ['txid', 'name', 'kingdom', 'Chinese', 'Pathogenicity', 'CI', 
                        'hit_reads', 'uniq_reads', 'cover_length', 'cover_perc(%)', 
                        'uniq_efficiency(>0.01)', 'cover_efficiency(>50)', 'reads_distr', 'positive_status', 'bg_freq', 'bg_hit_reads', 'bg_uniq_reads',
                        'bg_cover_length', 'bg_uniq_effi', 'bg_cover_effi', 'hazard_level']
    if len(manual_pos_species_list) != 0:
        new_col = [(ele in manual_pos_species_list) for ele in judge_df.txid]
        judge_df['manual_pos'] = new_col

    judge_df.to_csv(judgement_record_file, encoding='gb18030', index = False, header=True, na_rep='N/A')
    
    virus_pos_speices_list_resort = sorted(virus_pos_speices_list, key=lambda x: x[4], reverse=True)
    bacteria_pos_speices_list_resort = sorted(bacteria_pos_speices_list, key=lambda x: x[4], reverse=True)
    eukaryote_pos_speices_list_resort = sorted(eukaryote_pos_speices_list, key=lambda x: x[4], reverse=True)
    armgene_pos_speices_list_resort = sorted(armgene_pos_speices_list, key=lambda x: x[4], reverse=True)

    return virus_pos_speices_list_resort, bacteria_pos_speices_list_resort, eukaryote_pos_speices_list_resort, armgene_pos_speices_list_resort, judge_df
