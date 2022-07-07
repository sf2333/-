from django.db import models
# Create your models here.

class ManagerInfo(models.Model):
    m_id = models.DecimalField(max_digits=8, decimal_places=0, primary_key=True)
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=32)

class UserInfo(models.Model):
    u_id = models.DecimalField(max_digits=8, decimal_places=0, primary_key=True)
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    left_borrow = models.DecimalField(max_digits=2, decimal_places=0)   # 剩余借书次数
    left_order = models.DecimalField(max_digits=2, decimal_places=0)    # 剩余预约次数
    email = models.EmailField()

class BookInfo(models.Model):
    id = models.DecimalField(max_digits=8, decimal_places=0, primary_key=True)
    name = models.CharField(max_length=32)
    author = models.CharField(max_length=32)
    house = models.CharField(max_length=32)
    category = models.CharField(max_length=10)
    pub_date = models.DateTimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    sum = models.DecimalField(max_digits=8, decimal_places=0)
    remain = models.DecimalField(max_digits=8, decimal_places=0)
    pos = models.CharField(max_length=32)

class BookState(models.Model):
    s_id = models.CharField(max_length=20, primary_key=True)
    state = models.CharField(max_length=4)

class Borrow(models.Model):
    s_id = models.ForeignKey(to='BookState', to_field='s_id', on_delete=models.CASCADE)
    u_id = models.ForeignKey(to='UserInfo', to_field='u_id', on_delete=models.CASCADE)
    out_date = models.DateTimeField()
    on_date = models.DateTimeField()
    r_date = models.DateTimeField(null=True)
    renew_num = models.DecimalField(max_digits=2, decimal_places=0, null=True)  # 可以为空
    fine = models.DecimalField(max_digits=10, decimal_places=2, null=True)

class Order(models.Model):
    b_id = models.ForeignKey(to='BookInfo', to_field='id', on_delete=models.CASCADE)
    u_id = models.ForeignKey(to='UserInfo', to_field='u_id', on_delete=models.CASCADE)
    date = models.DateTimeField()

