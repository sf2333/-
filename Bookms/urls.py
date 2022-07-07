"""Bookms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
# from django.conf.urls import url
from app01 import views
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
import datetime
from app01.models import *

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('book/add/$', views.add_book),
    path('books/', views.books),
    path('query_books/', views.query_books),    # 查询书籍
    path('return_books/', views.return_book_menu),   # 还书主菜单
    re_path('book/(\d+)/change', views.change_book),
    re_path('book/(\d+)/delete', views.delete_book),
    re_path('book/(\d+)/borrow', views.borrow_book),
    re_path('book/(\d+)/order', views.order_book),
    re_path('book/(\d+-\d+)/return', views.return_book),  # 还某一本书操作页面
    re_path('book/(\d+-\d+)/renew', views.renew_book)
    # path('search_results')
]

Setting_once_fine = 1  # 设置逾期一天费用
# 定时任务
scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

# 时间间隔3秒钟打印一次当前的时间
@register_job(scheduler, "interval", minutes=30, id='test_job', replace_existing=True)
def test_job():
    print("我是apscheduler任务")
    borrow_list = Borrow.objects.filter(r_date=None)  # 得到未还书的借阅记录
    for borrow in borrow_list:
        s_id = borrow.s_id.s_id
        on_date = borrow.on_date.replace(tzinfo=None)    # 将带市区时间转换为无时区时间
        now = datetime.datetime.now()
        print('ssssssssssssssssss', s_id, now.strftime('%Y-%m-%d %H:%M:%S'), on_date.strftime('%Y-%m-%d %H:%M:%S'))
        if on_date < now:
            borrow.fine += Setting_once_fine
            borrow.save()
            continue

# per-execution monitoring, call register_events on your scheduler
register_events(scheduler)
scheduler.start()
print("Scheduler started!")
