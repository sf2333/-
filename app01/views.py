from django.shortcuts import render, HttpResponse, redirect
import datetime
from app01.models import *

left_borrow_MAX = 3
borrow_book_minutes_MAX = 30
renew_num_MAX = 3

# Create your views here.
def add_book(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        name = request.POST.get('name')
        author = request.POST.get('author')
        house = request.POST.get('house')
        category = request.POST.get('category')
        pub_date = request.POST.get('pub_date')
        price = request.POST.get('price')
        pos = request.POST.get('pos')
        sum = request.POST.get('sum')
        remain = sum

        # 添加书籍记录，一对多
        book_obj = BookInfo.objects.create(id=id, name=name, author=author, house=house, category=category, pub_date=pub_date, price=price, pos=pos, sum=sum, remain=remain)

        # 添加对应的数据状态记录
        for i in range(int(sum)):
            state_obj = BookState.objects.create(s_id=f'{id}-{i}', state='在馆')

        return redirect('/books')

    # publish_list = Publish.objects.all()
    # author_list = Author.objects.all()

    return render(request, 'addbook.html', locals())


def books(request):
    book_list = BookInfo.objects.all()
    return render(request, 'books.html', locals())


def change_book(request, edit_book_id):
    book_obj = BookInfo.objects.get(id=edit_book_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        author = request.POST.get('author')
        house = request.POST.get('house')
        category = request.POST.get('category')
        pub_date = request.POST.get('pub_date')
        price = request.POST.get('price')
        pos = request.POST.get('pos')

        old_sum = int(book_obj.sum)
        new_sum = int(request.POST.get('sum'))
        change_num = new_sum - old_sum
        old_remain = int(book_obj.remain)
        new_remain = old_remain + change_num

        # print(f'old_sum:{old_sum},new_sum:{new_sum},old_remain:{old_remain},new_remain:{new_remain}')

        # 更新书籍记录
        BookInfo.objects.filter(id=edit_book_id).update(name=name, author=author, house=house, pub_date=pub_date, price=price, pos=pos, sum=new_sum, remain=new_remain)
        # 更新状态记录(增加、减少）
        # print(f'this is {change_num}')

        if change_num < 0:
            for i in range(1, -change_num + 1):
                order = old_sum - i
                s_id = f'{edit_book_id}-{order}'
                BookState.objects.get(s_id=s_id).delete()
        else:
            for i in range(change_num):
                order = old_sum + i
                s_id = f'{edit_book_id}-{order}'
                state_obj = BookState.objects.create(s_id=s_id, state='在馆')

        return redirect('/books')

    return render(request, 'editbook.html', locals())


def delete_book(request, delete_book_id):

    book_obj = BookInfo.objects.get(id=delete_book_id)
    sum = book_obj.sum
    remain = book_obj.remain
    if sum == remain:
        for i in range(int(sum)):
            BookState.objects.get(s_id=f'{delete_book_id}-{i}').delete()
        book_obj.delete()
        return redirect('/books')

    else:
        return render(request, 'delete_fail.html')


def query_books(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        author = request.POST.get('author')
        house = request.POST.get('house')
        category = request.POST.get('category')

        book_list = BookInfo.objects.filter(name__contains=name).filter(author__contains=author).filter(house__contains=house).filter(category__contains=category)

        return render(request, 'search_results.html', locals())

    return render(request, 'query_books.html', locals())

def borrow_book(request, borrow_book_id, u_id=0):
    book_obj = BookInfo.objects.get(id=borrow_book_id)
    user_obj = UserInfo.objects.get(u_id=u_id)  # 用户功能还没写暂时定为 0 号用户
    remain = book_obj.remain
    left_borrow = user_obj.left_borrow
    if remain == 0 or left_borrow == 0:
        return render(request, 'borrow_fail.html')
    else:
        free_book_list = BookState.objects.filter(state='在馆', s_id__contains=f'{borrow_book_id}')
        num_list = [int(x.s_id.split('-')[1]) for x in free_book_list]
        num_list.sort()
        now = num_list[0]  # 最小号数的空闲图书
        state_obj = BookState.objects.get(s_id=f'{borrow_book_id}-{now}')  # 外键必须是个对象
        out_date = datetime.datetime.now()  # 获取当前时间
        on_date = out_date + datetime.timedelta(minutes=borrow_book_minutes_MAX)  # 借书期限等于设定好的最大值
        out_date = out_date.strftime("%Y-%m-%d %H:%M:%S")
        on_date = on_date.strftime("%Y-%m-%d %H:%M:%S")

        # 创建对应的借阅记录
        Borrow.objects.create(s_id=state_obj, u_id=user_obj, out_date=out_date, on_date=on_date, renew_num=0, fine=0)  # 续借次数和逾期费用初始为0

        # 更新状态表对应s_id状态
        state_obj.state = '借出'
        state_obj.save()

        # 更新用户表对应借阅上限信息
        user_obj.left_borrow = left_borrow - 1
        user_obj.save()

        # 更新图书表剩余信息
        book_obj.remain = remain - 1
        book_obj.save()

        return render(request, 'borrow_success.html')

    return redirect('/books')

def return_book_menu(request, u_id=0):
    all_borrow_obj_list = Borrow.objects.filter(u_id=u_id)  # 获取所有借书记录
    # ective_borrow_obj_list = all_borrow_obj_list.filter().exclude(r_date=None).all()  # 获取未还书的借书记录
    book_obj_list = []

    for borrow_record in all_borrow_obj_list:
        # borrow_record.s_id 因为外键的原因 指向的是 对象 Borrow 而不是 s_id
        s_id = borrow_record.s_id.s_id
        id = int(s_id.split('-')[0])  # 从 s_id 得到 book id
        book_obj_list.append(BookInfo.objects.get(id=id))
    return_obj_list = zip(all_borrow_obj_list, book_obj_list)

    return render(request, 'return_books.html', locals())


def return_book(request, return_book_id, u_id=0):
    state_obj = BookState.objects.get(s_id=return_book_id)
    borrow_obj = Borrow.objects.filter(s_id=return_book_id).get(r_date=None)  # 得到还书时间为空的记录
    user_obj = UserInfo.objects.get(u_id=u_id)
    id = int(return_book_id.split('-')[0])
    book_obj = BookInfo.objects.get(id=id)

    # 更新状态表信息
    state_obj.state = '在馆'
    state_obj.save()

    # 更新图书表信息
    book_obj.remain += 1
    book_obj.save()

    # 更新用户表信息
    user_obj.left_borrow += 1
    user_obj.save()

    # 更新借阅记录中的借阅时间
    borrow_obj.r_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 获取当前时间
    borrow_obj.save()

    return render(request, 'return_success.html', locals())

def renew_book(request, renew_book_id, u_id=0):
    borrow_obj = Borrow.objects.filter(s_id=renew_book_id).get(r_date=None)  # 得到还书时间为空的记录
    # user_obj = UserInfo.objects.get(u_id=u_id)

    if borrow_obj.renew_num < renew_num_MAX: # 续借次数小于等于最大值
        # 更新借书记录里的 续借次数 和 还书期限
        borrow_obj.renew_num += 1
        old_on_date = borrow_obj.on_date
        new_on_date = (old_on_date + datetime.timedelta(minutes=borrow_book_minutes_MAX)).strftime("%Y-%m-%d %H:%M:%S")
        borrow_obj.on_date = new_on_date
        borrow_obj.save()

        return render(request, 'renew_success.html', locals())
    else:
        return render(request, 'renew_fail.html', locals())

def order_book(request, order_book_id, u_id=0):
    book_obj = BookInfo.objects.get(id=order_book_id)
    user_obj = UserInfo.objects.get(u_id=u_id)

    left_order = user_obj.order
    return render(request, 'order_success.html', locals())

