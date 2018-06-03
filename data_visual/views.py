import json
import xlrd
import os
#from django.core.urlresolvers import reverse
from django.shortcuts import render,redirect
from django.http import HttpResponse

# Create your views here.


def data_visual_home(request):
    return render(request,'visual_home.html')


def data_visual_process(request):
    return render(request,'analysis.html')


def upload_file(request):
    if request.method == "POST":    # 请求方法为POST时，进行处理  
        myFile =request.FILES.get("myfile", None)    # 获取上传的文件，如果没有文件，则默认为None  
        if not myFile:  
            return HttpResponse("没有文件被上传!") 
        base_path = os.path.dirname(os.path.dirname(__file__))
        global file_path
        file_path = os.path.join(base_path,'media\data_visual',myFile.name)
        destination = open(os.path.join(base_path,'media\data_visual',myFile.name),'wb+')    # 打开特定的文件进行二进制的写操作  
        print(file_path)
        for chunk in myFile.chunks():      # 分块写入文件  
            destination.write(chunk)  
        destination.close()  
        #return HttpResponse("上传成功!")
        return redirect(data_visual_process) 



def process_data(request):
    efile = xlrd.open_workbook(str(file_path))

    #for sheet_nmae in efile.sheet_names():
    sheet = efile.sheet_by_index(0)
    if sheet.nrows == 3:
        data = pie_and_simple_bar(sheet)
    elif sheet.nrows == 4:
        data = cluster_bar(sheet)
    else:
        data = effect_scatter(sheet)

    #data = pie_and_simple_bar(efile)
    return HttpResponse(json.dumps(data), content_type="application/json")


def pie_and_simple_bar(sheet):
    title = sheet.cell(0,0).value
    mtype = sheet.row_values(1)
    num = sheet.row_values(2)

    piedata = []
    for value,name in zip(num,mtype):
        temp_dict = {'value':value,'name':name}
        piedata.append(temp_dict)

    unit = '患病人数'
    data = {"bar":{"name": mtype,       # 坐标系横坐标
                    "data": num,        # 图像数据
                    "title": title,     # 图像标题
                    "present": unit,    # 图例
            },
            "pie":{
                    "data":piedata,     # 图表数据
                    "title":title,      # 图表标题
                    "present":mtype,    # 图例数据数组
                    "unit":unit         # 图表图例
            },
            "type":'pie_and_bar',
        }
    return data


def effect_scatter(sheet):
    title = sheet.cell(0,0).value
    col1 = sheet.col_values(0)[1:]  #获取第一列
    col2 = sheet.col_values(1)[1:]  #获取第二列
    xAxis = col1[0]                 #获取坐标名称
    yAxis = col2[0]

    rel_data = list(map(list,zip(col1[1:],col2[1:])))  #数据封装 单个格式为[142,54]

    x_max = rel_data[0]
    y_max = rel_data[0]

    for cell in rel_data:
        print(cell,type(cell),cell[0],type(cell[0]))
        if cell[0]>x_max[0]:
            x_max = cell
        if cell[1]>y_max[1]:
            y_max = cell

    rel_data.remove(x_max)
    rel_data.remove(y_max)

    data = {
            "xAxis_name":xAxis,
            "yAxis_name":yAxis,
            "effect_data":[x_max,y_max],
            "scatter_data":rel_data,
            "title":title,
            "type":'scatter',
        }
    return data



def cluster_bar(sheet):
    title = sheet.cell(0,0).value
    item_name = []
    clu_name = []
    clu_num = 0
    real_data = []

    for (row,row_range,col,col_range) in sheet.merged_cells:        
        if row == 1:
            item_num = col_range-col
            clu_name.append(sheet.cell(row,col).value)   
            clu_num += 1
    for x in range(item_num):
        item_name.append(sheet.cell(2,x).value)

    index = 0
    for x in range(item_num):
        index = x
        temp = []
        for y in range(clu_num):  
            temp.append(sheet.cell(3,index).value)
            index += item_num
        real_data.append(temp)

    data = {
        "title":title,
        "item_name":item_name,
        "clu_name":clu_name,
        "real_data":real_data,
        "item_num":item_num,
        "type":'cluster_bar',
    }

    return data

