from django.shortcuts import render
import pymysql

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core import serializers


def add_book_imformation(request):
    if request.method == "POST":
        # 获取表单提交的文本
        book_code = request.POST.get("book_code")  # 图书编号
        book_name = request.POST.get("book_name")  # 书名
        book_writer = request.POST.get("book_writer")  # 作者
        book_house = request.POST.get("book_house")  # 出版社
        book_type = request.POST.get("book_type")   # 图书类型
        book_num = request.POST.get("book_num")   # 图书数量
        book_position = request.POST.get("book_position")  # 图书位置
        # 打印字段
        print("图书编号"+book_code)
        print("书名"+book_name)
        print("作者"+book_writer)
        print("出版社地址"+book_house)
        print("图书类型"+book_type)
        print("图书数量"+book_num)
        print("图书位置"+book_position)
        # 存入数据库

    return render(request, "add_book_imformation.html")

@csrf_exempt
# 用来解决ajax的POST 403 主要是验证问题
def test(request):

    if request.method == "POST":
        # 获取表单提交的文本
        name = request.POST.get("name")
        book_code = request.POST.get("book_code")  # 图书编号
        book_name = request.POST.get("book_name")  # 书名
        book_writer = request.POST.get("book_writer")  # 作者
        book_house = request.POST.get("book_house")  # 出版社
        book_type = request.POST.get("book_type")  # 图书类型
        book_num = request.POST.get("book_num")  # 图书数量
        book_position = request.POST.get("book_position")  # 图书位置

        # 打印字段
        print("图书编号" + book_code)
        print("书名" + book_name)
        print("作者" + book_writer)
        print("出版社地址" + book_house)
        print("图书类型" + book_type)
        print("图书数量" + book_num)
        print("图书位置" + book_position)
        print(name)

    return render(request, "test.html")


@csrf_exempt
def test_NavMenu(request):
    if request.method == "POST":
        # 获取表单提交的文本
        name = request.POST.get("name")
        book_code = request.POST.get("book_code")  # 图书编号
        book_name = request.POST.get("book_name")  # 书名
        book_writer = request.POST.get("book_writer")  # 作者
        book_house = request.POST.get("book_house")  # 出版社
        book_type = request.POST.get("book_type")  # 图书类型
        book_num = request.POST.get("book_num")  # 图书数量
        book_position = request.POST.get("book_position")  # 图书位置

        # 打印字段
        print("图书编号" + book_code)
        print("书名" + book_name)
        print("作者" + book_writer)
        print("出版社地址" + book_house)
        print("图书类型" + book_type)
        print("图书数量" + book_num)
        print("图书位置" + book_position)
        print(name)
    return render(request, "test_NavMenu.html")

def mark(request):
    return render(request,'mark2.html')