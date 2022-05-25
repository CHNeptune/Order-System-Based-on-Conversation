import hashlib
from database import *
ROOTID = "1"
"""默认管理员账号ID"""
BUSINESSID = "2"
"""默认商家账号ID"""
def isLogin(uid:str,uid_md5:str):
    """登陆状态验证
        返回 1 :登陆验证通过 ;
             0 :登陆验证失败
        
    """
    #加盐
    uid = uid + "336695*%^&#"
    #超管权限,ID为1则为超管
    rootId = str(ROOTID) + "336695*%^&#"
    md5_expect = hashlib.md5(uid.encode("utf8")).hexdigest()
    root_md5_expect = hashlib.md5(rootId.encode("utf8")).hexdigest()
    if md5_expect == uid_md5 or root_md5_expect == uid_md5:
        return 1
    else :
        return 0
def set_cookie_login(uid:str):
    """设置uid对应的cookie"""
    #加盐
    uid = uid + "336695*%^&#"
    uid_md5 = hashlib.md5(uid.encode("utf8")).hexdigest()
    return uid_md5
def FoodsListToJson(FoodsList:list) -> str :
    """返回食品信息表json化的字符串, 如果为-1,则出现列表不匹配错误,所以不要轻易修改数据表字段 """
    #ID,name,type,old_price,new_Price,introduce,img,state
    FoodsListJson = ""
    
    for i in range(0,len(FoodsList)):
        FoodsJson = ""
        for j in range(0,len(FoodsList[i])):
            if len(FoodsList[i]) != 8 :
                return "-1"
            if j == 0 :
                FoodsJson = FoodsJson + """"ID":""" + str(FoodsList[i][j]) + ","
            elif j == 1 :
                FoodsJson = FoodsJson + """"name":"%s"\
                    """ % FoodsList[i][j] + ","
            elif j == 2 :
                if FoodsList[i][j] == None :
                    FoodsList[i][j] = ''
                FoodsJson = FoodsJson + """"type":"%s"\
                    """ % FoodsList[i][j] + ","
            elif j == 3 :
                FoodsJson = FoodsJson + """"old_price":"%s"\
                    """ % FoodsList[i][j] + ","
            elif j == 4 :
                FoodsJson = FoodsJson + """"new_price":"%s"\
                    """ % FoodsList[i][j] + ","
            elif j == 5 :
                if FoodsList[i][j] == None :
                    FoodsList[i][j] = ''
                FoodsJson = FoodsJson + """"introduce":"%s"\
                    """ % FoodsList[i][j] + ","
            elif j == 6 :
                if FoodsList[i][j] == None :
                    FoodsList[i][j] = ''
                FoodsJson = FoodsJson + """"img":"%s"\
                    """ % FoodsList[i][j] + ","
            elif j == 7 :
                if FoodsList[i][j] == None :
                    FoodsList[i][j] = ''
                FoodsJson = FoodsJson + """"state":%s\
                    """ % str(FoodsList[i][j])
        FoodsJson = "{" + FoodsJson + "}"
        if i != len(FoodsList) - 1 :
            FoodsListJson = FoodsListJson + FoodsJson + ","
        else :
            FoodsListJson = FoodsListJson + FoodsJson
    FoodsListJson = "[" + FoodsListJson + "]"
    return FoodsListJson
def FoodsCartListToJson(FoodsList:list) -> str :
    """返回食品信息购物车json化的字符串, 因为多了一个数量字段，所以不能复用前一个函数，如果为-1,则出现列表不匹配错误 """
    #ID,name,type,old_price,new_Price,introduce,img,state,number
    FoodsListJson = ""
    
    for i in range(0,len(FoodsList)):
        FoodsJson = ""
        for j in range(0,len(FoodsList[i])):
            if len(FoodsList[i]) != 9 :
                return "-1"
            if j == 0 :
                FoodsJson = FoodsJson + """"ID":""" + str(FoodsList[i][j]) + ","
            elif j == 1 :
                FoodsJson = FoodsJson + """"name":"%s"\
                    """ % FoodsList[i][j] + ","
            elif j == 2 :
                if FoodsList[i][j] == None :
                    FoodsList[i][j] = ''
                FoodsJson = FoodsJson + """"type":"%s"\
                    """ % FoodsList[i][j] + ","
            elif j == 3 :
                FoodsJson = FoodsJson + """"old_price":"%s"\
                    """ % FoodsList[i][j] + ","
            elif j == 4 :
                FoodsJson = FoodsJson + """"new_price":"%s"\
                    """ % FoodsList[i][j] + ","
            elif j == 5 :
                if FoodsList[i][j] == None :
                    FoodsList[i][j] = ''
                FoodsJson = FoodsJson + """"introduce":"%s"\
                    """ % FoodsList[i][j] + ","
            elif j == 6 :
                if FoodsList[i][j] == None :
                    FoodsList[i][j] = ''
                FoodsJson = FoodsJson + """"img":"%s"\
                    """ % FoodsList[i][j] + ","
            elif j == 7 :
                if FoodsList[i][j] == None :
                    FoodsList[i][j] = ''
                FoodsJson = FoodsJson + """"state":%s\
                    """ % str(FoodsList[i][j]) + ","
            elif j == 8 :
                if FoodsList[i][j] == None :
                    FoodsList[i][j] = ''
                FoodsJson = FoodsJson + """"number":%s\
                    """ % str(FoodsList[i][j])

        FoodsJson = "{" + FoodsJson + "}"
        if i != len(FoodsList) - 1 :
            FoodsListJson = FoodsListJson + FoodsJson + ","
        else :
            FoodsListJson = FoodsListJson + FoodsJson
    FoodsListJson = "[" + FoodsListJson + "]"
    return FoodsListJson
def OrdersListToJson(OrdersList:list) -> str :
    """返回订单表json化的字符串, 如果为-1,则出现列表不匹配错误,所以不要轻易修改数据表字段 """
    #ID,food_id,uid,price,date,pay_state,serve_state,remark
    OrdersListJson = ""
    
    for i in range(0,len(OrdersList)):
        OrdersJson = ""
        for j in range(0,len(OrdersList[i])):
            if len(OrdersList[i]) != 8 :
                return "-1"
            if j == 0 :
                OrdersJson = OrdersJson + """"ID":""" + str(OrdersList[i][j]) + ","
            elif j == 1 :
                OrdersJson = OrdersJson + """"food_id":"%s"\
                    """ % OrdersList[i][j] + ","
            elif j == 2 :
                if OrdersList[i][j] == None :
                    OrdersList[i][j] = ''
                OrdersJson = OrdersJson + """"uid":%s\
                    """ % OrdersList[i][j] + ","
            elif j == 3 :
                OrdersJson = OrdersJson + """"price":"%s"\
                    """ % OrdersList[i][j] + ","
            elif j == 4 :
                OrdersJson = OrdersJson + """"date":"%s"\
                    """ % OrdersList[i][j] + ","
            elif j == 5 :
                if OrdersList[i][j] == None :
                    OrdersList[i][j] = ''
                OrdersJson = OrdersJson + """"pay_state":%s\
                    """ % OrdersList[i][j] + ","
            elif j == 6 :
                if OrdersList[i][j] == None :
                    OrdersList[i][j] = ''
                OrdersJson = OrdersJson + """"serve_state":%s\
                    """ % OrdersList[i][j] + ","
            elif j == 7 :
                if OrdersList[i][j] == None :
                    OrdersList[i][j] = ''
                OrdersJson = OrdersJson + """"remark":"%s"\
                    """ % str(OrdersList[i][j])
        OrdersJson = "{" + OrdersJson + "}"
        if i != len(OrdersList) - 1 :
            OrdersListJson = OrdersListJson + OrdersJson + ","
        else :
            OrdersListJson = OrdersListJson + OrdersJson
    OrdersListJson = "[" + OrdersListJson + "]"
    return OrdersListJson
def MsgsListToJson(MsgsList:list) -> str :
    """返回消息表json化的字符串, 如果为-1,则出现列表不匹配错误,所以不要轻易修改数据表字段 """
    #ID,uid,date,title,content,isread
    MsgsListJson = ""
    
    for i in range(0,len(MsgsList)):
        MsgsJson = ""
        for j in range(0,len(MsgsList[i])):
            if len(MsgsList[i]) != 6 :
                return "-1"
            if j == 0 :
                MsgsJson = MsgsJson + """"ID":""" + str(MsgsList[i][j]) + ","
            elif j == 1 :
                MsgsJson = MsgsJson + """"uid":"%s"\
                    """ % MsgsList[i][j] + ","
            elif j == 2 :
                if MsgsList[i][j] == None :
                    MsgsList[i][j] = ''
                MsgsJson = MsgsJson + """"date":"%s"\
                    """ % MsgsList[i][j] + ","
            elif j == 3 :
                MsgsJson = MsgsJson + """"title":"%s"\
                    """ % MsgsList[i][j] + ","
            elif j == 4 :
                MsgsJson = MsgsJson + """"content":"%s"\
                    """ % MsgsList[i][j] + ","
            elif j == 5 :
                if MsgsList[i][j] == None :
                    MsgsList[i][j] = ''
                MsgsJson = MsgsJson + """"isread":%s\
                    """ % MsgsList[i][j]
            
        MsgsJson = "{" + MsgsJson + "}"
        if i != len(MsgsList) - 1 :
            MsgsListJson = MsgsListJson + MsgsJson + ","
        else :
            MsgsListJson = MsgsListJson + MsgsJson
    MsgsListJson = "[" + MsgsListJson + "]"
    return MsgsListJson

def UserListToJson(UList):
    #ID name address phone uname passwd table_number pre_food_id 
    """返回某个用户json化的字符串, 如果为-1,则出现列表不匹配错误,所以不要轻易修改数据表字段,\n不会返回密码 """
    UJson = ""
    for j in range(0,len(UList)):
        if len(UList) != 8 :
            return "-1"
        if j == 0 :
            UJson = UJson + """"ID":""" + str(UList[j]) + ","
        elif j == 1 :
            UJson = UJson + """"name":"%s"\
                """ % UList[j] + ","
        elif j == 2 :
            if UList[j] == None :
                UList[j] = ''
            UJson = UJson + """"address":"%s"\
                """ % UList[j] + ","
        elif j == 3 :
            if UList[j] == None :
                UList[j] = ''
            UJson = UJson + """"phone":"%s"\
                """ % UList[j] + ","
        elif j == 4 :
            UJson = UJson + """"uname":"%s"\
                """ % UList[j] + ","
        elif j == 6 :
            if UList[j] == None :
                UList[j] = ''
            UJson = UJson + """"table_number":"%s"\
                """ % UList[j] + ","
        elif j == 7 :
            if UList[j] == None :
                UList[j] = ''
            UJson = UJson + """"pre_food_id":"%s"\
                """ % UList[j]
            
    UJson = "{" + UJson + "}"
    
    return UJson
def CreateBaseAccount():
    global ROOTID
    global BUSINESSID
    rList = GetUsersByUname("ROOT")
    bList = GetUsersByUname("BUSINESS")
    if rList == [] :
        ROOTID = str(InsertTableUsers("ROOT","","00000000000","ROOT","root","NULL",""))
    else :
        ROOTID = str(rList[0])
    if bList == [] :
        BUSINESSID = str(InsertTableUsers("BUSINESS","","00000000000","BUSINESS","business","NULL",""))
    else :
        BUSINESSID = str(bList[0])


