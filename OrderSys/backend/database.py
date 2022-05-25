"""
    本文件为数据库调用API,如有需要,可以添加
"""
import pymysql


#私有函数，不建议调用（暂不设计面向对象机制）
def ConnectToDB():
    db = pymysql.connect(host="localhost",
        user="root",
        password="ct5935836",
        database="ordersys")
    return db
#示例函数，按行以字符串输出test表数据
def GetTestTable():
    db = ConnectToDB()
    c = db.cursor()
    c.execute("select * from test")
    data = c.fetchall()
    s = ""
    for  i in range(0,len(data)):
        for  j in range(0,len(data[i])):
            s += str(data[i][j]) + " "
        s += "\n--"
    db.close()
    return s
#示例函数，创建test表
def CreateTableTest():
    db = ConnectToDB()
    c = db.cursor()
    sql = """create table if not exists test(
        first int,
        second varchar(100)
    )
    """
    c.execute(sql)
    db.close()
#示例函数，插入test表数据
def InsertTableTest(first:str,second:str):
    second = '"' + second
    second = second + '"'
    db = ConnectToDB()
    c = db.cursor()
    sql = """insert into test(first,second)
        values("""+ first +""",""" + second + """)
    """
    try:
        c.execute(sql)
        db.commit()
    except:
        db.rollback()
    
    db.close()

#数据库操作API
#-------------------------------------------------------------------#
#用户信息表
def CreateTableUsers():
    """创建用户信息表"""
    db = ConnectToDB()
    c = db.cursor()
    sql = """create table if not exists users(
        ID int unsigned auto_increment,
        name varchar(100) not null,
        address varchar(300),
        phone varchar(20) not null,
        uname varchar(40) not null,
        passwd varchar(40) not null,
        table_number int,
        pre_food_id varchar(300),
        primary key (ID),
        unique (uname)

    )
    """
    c.execute(sql)
    db.close()
def InsertTableUsers(name:str,address:str,phone:str,uname:str,passwd:str,table_number:str,pre_food_id:str):
    """插入用户信息,空值可能为字符串NULL,即使数字类型也以字符串形式作为参数
        address,table_number,pre_food_id可为NULL -------
        返回用户id,返回-1则失败,返回-2则为特殊的 【用户名重复】失败
    """
    if table_number == None:
        table_number = ""
    db = ConnectToDB()
    c = db.cursor()
    id = -1
    sql = """insert into users(name,address,phone,uname,passwd,table_number,pre_food_id) 
        values('%s','%s','%s','%s','%s',%s,'%s') """ % (name,address,phone,uname,passwd,table_number,pre_food_id)
    try:
        c.execute(sql)
        id = c.lastrowid
        db.commit()
    except Exception as e:
        se = str(e)
        print("---!!!--->插入错误：" + se + "\n--->sql语句:"+sql)
        if se[1:5] == '1062':
            id = -2
        else :
            id = -1
        db.rollback()
    db.close()
    return id
def GetUsersByUname(uname:str):
    """以用户名获取用户信息,以list返回该条记录"""
    db = ConnectToDB()
    c = db.cursor()
    c.execute("select * from users where uname = '%s'" % uname )
    data = c.fetchone()
    if data == None:
        db.close()
        return []
    l = list(data)
    db.close()
    return l
def GetUsersByUid(uid:str):
    """以用户id获取用户信息,以list返回该条记录"""
    db = ConnectToDB()
    c = db.cursor()
    c.execute("select * from users where id = '%s'" % uid )
    data = c.fetchone()
    if data == None:
        db.close()
        return []
    l = list(data)
    db.close()
    return l
def GetUidByUname(uname:str):
    """以用户名获取用户id,以str返回"""
    db = ConnectToDB()
    c = db.cursor()
    c.execute("select id from users where uname = '%s'" % uname )
    data = c.fetchone()
    if data == None:
        db.close()
        return ""
    s = str(data[0])
    db.close()
    return s
def UpdateUsersByUid(uid:str,field:str,value:str):
    """更新用户信息，第一个参数为用户id，第二个参数为更新字段，第三个参数为更新字段值---
        如果字段类型为数字，那么不能传入空串，以字符串NULL代替
    """
    db = ConnectToDB()
    c = db.cursor()
    if field != "table_number" :
        value = "'" + value
        value = value + "'"
    sql = """update users
        set %s = %s
        where id = %s
        """ % (field,value,uid)
    try:
        c.execute(sql)
        db.commit()
    except Exception as e:
        print("---!!!--->更新错误：" + str(e))
        db.rollback()
    db.close()
def UpdateUsersByUname(uname:str,field:str,value:str):
    """更新用户信息，第一个参数为用户名，第二个参数为更新字段，第三个参数为更新字段值---
        如果字段类型为数字，那么不能传入空串，以字符串NULL代替
    """
    db = ConnectToDB()
    c = db.cursor()
    if field != "table_number" :
        value = "'" + value
        value = value + "'"
    sql = """update users
        set %s = %s
        where uname = '%s'
        """ % (field,value,uname)
    try:
        c.execute(sql)
        db.commit()
    except Exception as e:
        print("---!!!--->更新错误：" + str(e))
        db.rollback()
    db.close()


#----------------------------------------------------------------------#
#食品信息表
def CreateTableFoods():
    """创建食品信息表"""
    db = ConnectToDB()
    c = db.cursor()
    sql = """create table if not exists foods(
        ID int unsigned auto_increment,
        name varchar(100) not null,
        type varchar(20),
        old_price varchar(20) not null,
        new_price varchar(20) not null,
        introduce varchar(400) ,
        img varchar(200),
        state int,
        primary key (ID),
        unique (name)
    )
    """
    c.execute(sql)
    db.close()
def InsertTableFoods(name:str,type:str,old_price:str,new_Price:str,introduce:str,img:str,state:str):
    """插入食品信息,名字必须唯一.
        state:0,失效;  1,有效
        ---返回 0 :插入成功;-1失败
        """
    db = ConnectToDB()
    c = db.cursor()
    su = 0
    sql = """insert into foods(name,type,old_price,new_Price,introduce,img,state)
        values('%s','%s','%s','%s','%s','%s',%s) """ % (name,type,old_price,new_Price,introduce,img,state)
    try:
        c.execute(sql)
        su = c.lastrowid
        db.commit()
    except Exception as e:
        print("---!!!--->sql:"+ sql +"\n插入错误：" + str(e))
        su = -1
        db.rollback()
    db.close()
    return su
def GetFoodsByName(name:str):
    """以食品名获取食品信息,以list返回该条记录"""
    db = ConnectToDB()
    c = db.cursor()
    c.execute("select * from foods where name = '%s'" % name )
    data = c.fetchone()
    if data == None:
        db.close()
        return []
    l = list(data)
    db.close()
    return l
def GetFoodsById(id:str):
    """以食品id获取食品信息,以list返回该条记录"""
    db = ConnectToDB()
    c = db.cursor()
    c.execute("select * from foods where id = '%s'" % id )
    data = c.fetchone()
    if data == None:
        db.close()
        return []
    l = list(data)
    db.close()
    return l
def GetFoodsList():
    """获取所有食品信息,以二维list返回"""
    db = ConnectToDB()
    c = db.cursor()
    c.execute("select * from foods")
    data = c.fetchall()
    l = []
    for  i in range(0,len(data)):
        l.append(list(data[i]))
    
    db.close()
    return l
def GetValidFoodsNameList():
    """获取所有有效食品名字,以list返回"""
    db = ConnectToDB()
    c = db.cursor()
    c.execute("select name from foods where state = 1")
    data = c.fetchall()
    l = []
    if len(data) == 0:
        db.close()
        return l
    for  i in range(0,len(data)):
        l.append(data[i][0])
    
    db.close()
    return l
def GetValidFoodsTypeList():
    """获取所有有效食品类型,以list返回"""
    db = ConnectToDB()
    c = db.cursor()
    c.execute("select type from foods where state = 1")
    data = c.fetchall()
    l = []
    if len(data) == 0:
        db.close()
        return l
    for  i in range(0,len(data)):
        l.append(data[i][0])
    
    db.close()
    return l
def GetTypeFoodsNameList(type:str):
    """根据类型获取所有有效食品名字,以list返回"""
    db = ConnectToDB()
    c = db.cursor()
    c.execute("""select name from foods where type = "%s" """ % type)
    data = c.fetchall()
    l = []
    if len(data) == 0:
        db.close()
        return l
    for  i in range(0,len(data)):
        l.append(data[i][0])
    
    db.close()
    return l
def UpdateFoodsById(id:str,name:str,type:str,old_price:str,new_Price:str,introduce:str,img:str,state:str):
    """更新食物信息，比插入多了个id,若设置state为失效,则前端不显示\n
        
    """
    db = ConnectToDB()
    c = db.cursor()
    
    sql = """update foods
        set name = '%s',
        type = '%s',
        old_price = '%s',
        new_price = '%s',
        introduce = '%s',
        img = '%s',
        state = %s
        where id = %s
        """ % (name,type,old_price,new_Price,introduce,img,state,id)
    try:
        c.execute(sql)
        db.commit()
    except Exception as e:
        print("---!!!--->更新错误：" + str(e),"\nsql:",sql)
        db.rollback()
        db.close()
        return -1
    db.close()
    return 0
def DeleteFoodsById(id:str):
    """根据食物ID删除食物信息\n
        
    """
    db = ConnectToDB()
    c = db.cursor()
    
    sql = """delete from foods
        where id = %s
        """ % id
    try:
        c.execute(sql)
        db.commit()
    except Exception as e:
        print("---!!!--->删除错误：" + str(e))
        db.rollback()
        db.close()
        return -1
    db.close()
    return 0

#----------------------------------------------------------------------#
#订单表
def CreateTableOrders():
    """创建订单表"""
    db = ConnectToDB()
    c = db.cursor()
    sql = """create table if not exists orders(
        ID int unsigned auto_increment,
        food_id varchar(300) not null,
        uid int not null,
        price varchar(20) not null,
        date varchar(15) not null,
        pay_state int not null,
        serve_state int not null,
        remark varchar(500),
        primary key (ID)
    )
    """
    c.execute(sql)
    db.close()
def InsertTableOrders(food_id:str,uid:str,price:str,date:str,pay_state:str,serve_state:str,remark:str):

    """插入订单记录,返回订单ID.
        food_id:多个以分号隔开
        pay_state: 0,待支付;  1,已支付;  2,失效
        serve_state:0,无需服务;  1,待服务;  2,已服务
        
        """
    db = ConnectToDB()
    c = db.cursor()
    id = -1
    sql = """insert into orders(food_id,uid,price,date,pay_state,serve_state,remark)
        values('%s',%s,'%s','%s',%s,%s,'%s') """ % (food_id,uid,price,date,pay_state,serve_state,remark)
    try:
        c.execute(sql)
        id = c.lastrowid
        db.commit()

    except Exception as e:
        print("---!!!--->插入错误：" + str(e))
        db.rollback()
    
    db.close()
    return id
def GetOrdersByUid(uid:str):
    """以用户ID获取订单信息,以二维list返回"""
    db = ConnectToDB()
    c = db.cursor()
    c.execute("select * from orders where uid = %s" % uid )
    data = c.fetchall()
    l = []
    for  i in range(0,len(data)):
        l.append(list(data[i]))
    db.close()
    return l
def GetOrdersById(id:str):
    """以订单ID获取订单信息,返回一条list记录"""
    db = ConnectToDB()
    c = db.cursor()
    c.execute("select * from orders where id = %s" % id )
    data = c.fetchone()
    if data == None:
        db.close()
        return []
    l = list(data)
    db.close()
    return l
def GetOrdersList():
    """获取所有订单信息,以二维list返回
        注: 数据量较大时,不建议调用此函数,可以增加条件查询API
    """
    db = ConnectToDB()
    c = db.cursor()
    c.execute("select * from orders")
    data = c.fetchall()
    l = []
    for  i in range(0,len(data)):
        l.append(list(data[i]))
    db.close()
    return l
def GetOrdersByState(pay_state:str,serve_state):
    """以服务状态获取订单信息,以二维list返回"""
    db = ConnectToDB()
    c = db.cursor()
    c.execute("select * from orders where pay_state = %s and serve_state = %s" % (pay_state,serve_state) )
    data = c.fetchall()
    l = []
    for  i in range(0,len(data)):
        l.append(list(data[i]))
    db.close()
    return l
def UpdateOrdersById(id:str,field:str,value:str):
    """更新订单信息，第一个参数为订单id，第二个参数为更新字段，第三个参数为更新字段值,不可删除订单记录"""
    db = ConnectToDB()
    c = db.cursor()
    if field != "uid" or field != "pay_state" or field != "serve_state" :
        value = "'" + value
        value = value + "'"
    sql = """update orders
        set %s = %s
        where id = %s
        """ % (field,value,id)
    try:
        c.execute(sql)
        db.commit()
    except Exception as e:
        print("---!!!--->更新错误：" + str(e))
        db.rollback()
    db.close()


#----------------------------------------------------------------------#
#对话记录表
def CreateTableDialogs():
    """创建订单表"""
    db = ConnectToDB()
    c = db.cursor()
    sql = """create table if not exists dialogs(
        ID int unsigned auto_increment,
        uid int not null,
        date varchar(15) not null,
        msg_type varchar(15) not null,
        parm varchar(100),
        content varchar(500),
        primary key (ID)
    )
    """
    c.execute(sql)
    db.close()
def InsertTableDialogs(uid:str,date:str,msg_type:str,parm:str,content:str):

    """插入对话记录,返回对话id
        date:年月日时分秒
        msg_type: 0:用户发出,  1: 系统发出
        parm: 可空
        
        """
    db = ConnectToDB()
    c = db.cursor()
    id = -1
    sql = """insert into dialogs(uid,date,msg_type,parm,content)
        values(%s,'%s','%s','%s','%s') """ % (uid,date,msg_type,parm,content)
    try:
        c.execute(sql)
        id = c.lastrowid
        db.commit()

    except Exception as e:
        print("---!!!--->插入错误：" + str(e))
        db.rollback()
    
    db.close()
    return id
def GetDialogsByUid(uid:str):
    """以用户ID获取对话记录,以二维list返回"""
    db = ConnectToDB()
    c = db.cursor()
    c.execute("select * from dialogs where uid = %s" % uid )
    data = c.fetchall()
    l = []
    for  i in range(0,len(data)):
        l.append(list(data[i]))
    db.close()
    return l
def GetDialogsById(id:str):
    """以对话ID获取对话信息,返回一条list记录"""
    db = ConnectToDB()
    c = db.cursor()
    c.execute("select * from dialogs where id = %s" % id )
    data = c.fetchone()
    if data == None:
        db.close()
        return []
    l = list(data)
    db.close()
    return l
def UpdateDialogsById(id:str,field:str,value:str):
    """更新对话记录，第一个参数为订单id，第二个参数为更新字段，第三个参数为更新字段值,不可删除对话记录
        目前暂无该函数调用场景
    """
    db = ConnectToDB()
    c = db.cursor()
    if field != "uid" :
        value = "'" + value
        value = value + "'"
    sql = """update dialogs
        set %s = %s
        where id = %s
        """ % (field,value,id)
    try:
        c.execute(sql)
        db.commit()
    except Exception as e:
        print("---!!!--->更新错误：" + str(e))
        db.rollback()
    db.close()

#----------------------------------------------------------------------#
#消息通知表
def CreateTableMsgs():
    """创建消息表"""
    db = ConnectToDB()
    c = db.cursor()
    sql = """create table if not exists msgs(
        ID int unsigned auto_increment,
        uid int not null,
        date varchar(15) not null,
        title varchar(25) not null,
        content varchar(500),
        isread int not null,
        primary key (ID)
    )
    """
    c.execute(sql)
    db.close()
def InsertTableMsgs(uid:str,date:str,title:str,content:str,isread:str):

    """插入消息,返回id
        date:年月日时分秒
        isread: 0，未读;1，已读
        """
    db = ConnectToDB()
    c = db.cursor()
    id = -1
    sql = """insert into msgs(uid,date,title,content,isread)
        values(%s,'%s','%s','%s',%s) """ % (uid,date,title,content,isread)
    try:
        c.execute(sql)
        id = c.lastrowid
        db.commit()

    except Exception as e:
        print("---!!!--->插入错误：" + str(e))
        db.rollback()
    
    db.close()
    return id
def GetMsgsById(uid:str):
    """以用户ID获取消息记录,返回二维list记录"""
    db = ConnectToDB()
    c = db.cursor()
    c.execute("select * from msgs where uid = %s" % uid )
    data = c.fetchall()
    l = []
    for  i in range(0,len(data)):
        l.append(list(data[i]))
    db.close()
    return l
def MsgHasReadById(id:str):
    """消息标记为已读，参数为消息id
    """
    db = ConnectToDB()
    c = db.cursor()
    sql = """update msgs
        set isread = 1
        where id = %s
        """ % id
    try:
        c.execute(sql)
        db.commit()
    except Exception as e:
        print("---!!!--->更新错误：" + str(e))
        db.rollback()
    db.close()