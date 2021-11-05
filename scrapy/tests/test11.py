# 1、13位时间戳转换为datetime类
import datetime
def to_date(value):
    otherStyleTime = datetime.datetime.fromtimestamp(value / 1000)
    return otherStyleTime
print(to_date(1635749969000))
print(type(to_date(1635749969000)))


#2、字符串时间转换为datetime类
from datetime import datetime
t = datetime.strptime("1999-01-11", "%Y-%m-%d")
print(type(t), t)


#3、dateparser 将字符串时间转换为datetime类
import dateparser
t = dateparser.parse("1999-01-11")
print(type(t), t)


#4、dateparser 将时间戳转换为datetime类
import dateparser
t = dateparser.parse('1635750944')
print(type(t), t)


# str-->date
import dateparser
t = dateparser.parse('3小时前')
print(type(t), t)   ##输出当前时间减3小时后的时间