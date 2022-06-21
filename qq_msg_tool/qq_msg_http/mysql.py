import pymysql
from DBUtils.PooledDB import PooledDB
pool = PooledDB(
      creator=pymysql,  # 使用链接数据库的模块
      maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数
      mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
      maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
      maxshared=3,  # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
      blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
      maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
      host='127.0.0.1',
      port=3306,
      user='root',
      password='qweasd159753',
      database='excel',
      charset='utf8'
 )
# 用户输入一个关键词调用
def Search1(str):
    if str!="":
        str='%'+str+'%'
        sql='select * from shengcai  where data_id like "%s"'%str
        connect =pool.connection()
        cursor = connect.cursor()
        num = cursor.execute(sql)
        jud_i=judge_db(num)
        # float转int
        jud_i=int(jud_i)
        r_all = cursor.fetchall()
        cursor.close()
        connect.close()
    return jud_i,num,r_all
# 用户输入两个关键词调用
def Search2(str1,str2):
    zl = ''
    if str1!="" and str2!="":
        str1 = '%' + str1 + '%'
        str2='%'+str2+'%'
        # 关键词作为变量传入
        sql = 'select * from shengcai  where data_id like "%s" and data_id like "%s"' %(str1,str2)
        connect =pool.connection()
        cursor = connect.cursor()
        num = cursor.execute(sql)
        jud_i = judge_db(num)
        # float转int
        jud_i = int(jud_i)
        r_all = cursor.fetchall()
        for i in range(0, num):
            zl = zl + r_all[i][0] + '\n'+r_all[i][1] + '\n'
        cursor.close()
        connect.close()
    return jud_i,num,r_all
# 用户输入三个关键词调用
def Search3(str1,str2,str3):
    if str1!="" and str2!="" and str3!="":
        dbinfo = {"host": "localhost",
                  "user": "root",
                  "password": "qweasd159753",
                  "db": "excel"
                  }
        str1 = '%' + str1 + '%'
        str2='%'+str2+'%'
        str3 = '%' + str3 + '%'
        sql = 'select * from shengcai  where data_id like "%s" and data_id like "%s" and data_id like "%s"' %(str1,str2,str3)
        connect = pymysql.connect(**dbinfo)
        cursor = connect.cursor()
        num = cursor.execute(sql)
        jud_i = judge_db(num)
        # float转int
        jud_i = int(jud_i)
        r_all = cursor.fetchall()
        zl = ''
        for i in range(0, num):
            zl = zl + r_all[i][0] + '\n'+r_all[i][1] + '\n'
        cursor.close()
        connect.close()
    return jud_i,num,r_all
# class index:
#     def GET(self):
#         return render.index(str)
#
# urls = (
#     '/(.*)', 'index'
# )
#
# render = web.template.render('templates/')
# app = web.application(urls, globals())
# 判断数据库查询的返回个数
def judge_db(num):
    if num>10:
        # 发送i+1次信息
        i=num/10+1
    elif num==0:
        i=0
    else:
        i=1
    return i
