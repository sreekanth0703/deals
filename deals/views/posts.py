# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from collections import OrderedDict

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from deals.views.decorators import login_required, user_logined
from xlrd import open_workbook
from django.core.files.storage import FileSystemStorage
from deals.models import *
import json
import re
import datetime
import copy

@csrf_exempt
@login_required
def posts(request):
    ''' Posts Template '''
    time_dict = {'%m/%d/%y %I:%M %p': '1/23/18 12:00 AM'}
    deal_sites = ['Amazon.in', 'Flipkart', 'Paytm', 'Snapdeal', 'Shopclues', 'Amazon.com', 'Myntra']
    return render(request, 'main/posts.html', {'time_dict': time_dict, 'deal_sites': deal_sites})


def read_cell_data(row_idx, col_idx, reader='', file_type='xls', is_float=False):
    ''' Reads Excel cell Data '''
    try:
        if file_type == 'csv':
            cell_data = reader[row_idx][col_idx]
        else:
            cell_data = reader.cell(row_idx, col_idx).value
        if not is_float and isinstance(cell_data, (int, float)):
            cell_data = str(int(cell_data))
        if not isinstance(cell_data, (int, float)):
            cell_data = str(re.sub(r'[^\x00-\x7F]+', ' ', cell_data))
        if is_float and not cell_data:
            cell_data = 0
    except:
        cell_data = ''
    return cell_data


def read_excel(excel):
    ''' Check and Return Excel data'''
    status, reader, no_of_rows, no_of_cols, file_type = '', '', '', '', ''
    if (excel.name).split('.')[-1] == 'csv':
        reader = [[val.replace('\n', '').replace('\t', '').replace('\r', '') for val in row] for row in
                  csv.reader(excel.read().splitlines())]
        no_of_rows = len(reader)
        file_type = 'csv'
        no_of_cols = 0
        if reader:
            no_of_cols = len(reader[0])
    elif (excel.name).split('.')[-1] == 'xls' or (excel.name).split('.')[-1] == 'xlsx':
        try:
            data = excel.read()
            open_book = open_workbook(filename=None, file_contents=data)
            open_sheet = open_book.sheet_by_index(0)
            reader = open_sheet
            no_of_rows = reader.nrows
            file_type = 'xls'
            no_of_cols = open_sheet.ncols
        except:
            status = 'Invalid File'
    return reader, no_of_rows, no_of_cols, file_type, status


def validate_posts_excel(request, reader, no_of_rows, no_of_cols, excel, columns_list, file_type='xls'):
    excel_col_map, data = {}, []
    product_fields = ['product_name', 'product_url', 'product_category', 'product_price', 'product_mrp', 'deal_site', 'offer_start', 'offer_end']
    number_fields = ['product_price', 'product_mrp']
    prd_mapping = OrderedDict()
    prd_excel = {}
    for prd_field in product_fields:
        if request.POST.get(prd_field, ''):
            prd_mapping[request.POST[prd_field]] = prd_field
    for col in range(0, no_of_cols):
        cell_data = read_cell_data(0, col, reader, file_type)
        if cell_data in columns_list:
            excel_col_map[cell_data] = col
        if cell_data in prd_mapping.keys():
            prd_excel[prd_mapping[cell_data]] = col
    if columns_list and not excel_col_map:
        return 'No Mapping Found', data
    for row in range(1, no_of_rows):
        col_dict = {}
        prd_dict = {}
        for key, col in excel_col_map.items():
            cell_data = read_cell_data(row, col, reader, file_type)
            col_dict[key] = cell_data
        for key, val in prd_excel.items():
            if key not in number_fields:
                cell_data = read_cell_data(row, val, reader, file_type)
            else:
                cell_data = read_cell_data(row, val, reader, file_type, is_float=True)
            prd_dict[key] = cell_data
        prd_dict['extra_fields'] = col_dict
        data.append(prd_dict)
    return '', data


@csrf_exempt
@login_required
def insert_post(request):
    ''' Insert New Post '''
    data_dict = dict(request.POST.lists())
    columns_list = data_dict['column_name']
    columns_list = [dat for dat in columns_list if dat]
    excel = request.FILES['excel-file']
    image_file = request.FILES.get('image-file', '')
    reader, no_of_rows, no_of_cols, file_type, ex_status = read_excel(excel)
    if ex_status:
        return HttpResponse(ex_status)
    status, data = validate_posts_excel(request, reader, no_of_rows, no_of_cols, excel, columns_list, file_type=file_type)
    if status:
        return HttpResponse(status)
    if data:
        post_title = request.POST.get('title', '')
        post_desc = request.POST.get('desc', '')
        if post_title:
            if Post.objects.filter(post_title=post_title):
                return HttpResponse("Post Title Already Exists")
            post_dict = {'post_title': post_title, 'post_desc': post_desc, 'status': 1}
            if image_file:
                fs = FileSystemStorage()
                filename = fs.save("static/post_images/" + post_title, image_file)
                uploaded_file_url = fs.url(filename)
                post_dict['post_image'] = uploaded_file_url
            post_obj = Post.objects.create(post_title=post_title, post_desc=post_desc, status=1)
            post_data_objs = []
            for prd_dat in data[:100]:
                prd_dat['post_id'] = post_obj.id
                if len(prd_dat.get('product_url', '')) > 350:
                    continue
                prd_extra = copy.deepcopy(prd_dat.get('extra_fields', {}))
                if 'extra_fields' in prd_dat:
                    del prd_dat['extra_fields']
                date_format = request.POST.get('start_format', '')
                if date_format:
                    prd_dat['offer_start'] = datetime.datetime.strptime(prd_dat['offer_start'], date_format)
                    prd_dat['offer_end'] = datetime.datetime.strptime(prd_dat['offer_end'], date_format)
                else:
                    prd_dat['offer_start'] = datetime.datetime.now().date()
                    prd_dat['offer_end'] = datetime.datetime.now().date() + datetime.timedelta(days=10)

                product_obj = Product.objects.create(**prd_dat)
                for key, val in prd_extra.items():
                    post_data_objs.append(ProductData(product_id=product_obj.id, display_name=key, column_value=val))
            print('completed')
            if post_data_objs:
                ProductData.objects.bulk_create(post_data_objs)

    return HttpResponse('Success')