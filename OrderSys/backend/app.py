"""
设置响应状态码和响应头
return时,加上
如 return jsonerror,200,[("token", "123456"), ("City", "zhaotong")]
如 return jsonsuccess,200,[("Set-Cookie","uid=c4ca4238a0b923820dcc509a6f75849b")]
"""





import voiceToText
import random
from flask import Flask,request, url_for,send_file
from database import *
from function import *
from datetime import datetime
import base64
app = Flask(__name__)

print("-----------HI!---------------------------------------------START HERE!---------")
CreateTableTest()
CreateTableUsers()
CreateBaseAccount()
CreateTableFoods()
CreateTableOrders()
CreateTableDialogs()
CreateTableMsgs()
from recognition import ContentInAndOut
@app.after_request
def set_head(response):
    response.headers["Content-Type"]="application/json"
    response.headers["Access-Control-Allow-Origin"]="*"
    response.headers["Access-Control-Allow-Methods"]="*"
    response.headers["Access-Control-Allow-Headers"]="Content-Type,XFILENAME,XFILECATEGORY,XFILESIZE,Authentication"
    response.headers["Access-Control-Expose-Headers"]="Authentication"
    return response
# 装饰器就是，在下方函数前后执行一段代码，这段代码是装饰器函数事先定义的内容
@app.route('/')
def root():
    return "<a href='/test' >click here to test</>"

@app.route('/register',methods=['POST'])
def register():
    """调试阶段允许get"""
    #name, address, phone, uname, passwd
    name = request.get_json().get('name')
    address = request.get_json().get('address')
    phone = request.get_json().get('phone')
    uname = request.get_json().get('uname')
    passwd = request.get_json().get('passwd')
    if address == None :
        address = ""
    if name == None or phone == None or uname == None or passwd == None \
    or name == '' or phone == '' or uname == '' or passwd == '' :
        jsonerror = """{"errno":"2","errmsg":"Missing required parameter." ,"id":"-1"  }"""
        return jsonerror
    id = InsertTableUsers(name,address,phone,uname,passwd,'NULL','')
    if id == -1 :
        jsonerror = """{"errno":"3","errmsg":"Registration Fail. Database Insertion error" ,"id":"-1"  }"""
        return jsonerror
    elif id == -2 :
        jsonerror = """{"errno":"1","errmsg":"Registration Fail. User name duplicated" ,"id":"-1"  }"""
        return jsonerror
    jsonsuccess = """{"errno":"0","errmsg":"Successful!" ,"id":"%s"  }""" % id
    return jsonsuccess

@app.route('/login',methods=['POST'])
def login():
    """调试阶段允许get
        前端需要限制数据类型，特别是table_number只能为数字
    """
    #name, passwd, table_number
    #---------------------TODO:如果是已登录状态，返回【已登录】错误------------------------------------#
    uname = request.get_json().get('uname')
    passwd = request.get_json().get('passwd')
    table_number = request.values.get('table_number')
    if uname == None or passwd == None \
    or uname == '' or passwd == '' :
        jsonerror = """{"errno":"2","errmsg":"Missing required parameter."   }"""
        return jsonerror
    UserList = GetUsersByUname(uname)
    if UserList == [] :
        jsonerror = """{"errno":"3","errmsg":"User does not exist!"   }"""
        return jsonerror
    PasswdExpected = UserList[5]
    if PasswdExpected != passwd :
        jsonerror = """{"errno":"4","errmsg":"Password is wrong!"   }"""
        return jsonerror
    if table_number != None and table_number != '' :
        UpdateUsersByUname(uname,"table_number",table_number)
    else :
        UpdateUsersByUname(uname,"table_number","NULL")

    
    uid = GetUidByUname(uname)
    uid_md5 = set_cookie_login(uid)
    cookie = "uid=" + uid_md5
    set_cookie = [("Authentication",cookie)]
    jsonsuccess = """{"errno":"0","errmsg":"Login successful!","ID":"%s"}""" % uid
    return jsonsuccess,200,set_cookie

@app.route('/logout',methods=['POST'])
def logout():
    jsonsuccess = """{"errno":"0","errmsg":"Logout successful!"}"""
    uid = "-1"
    cookie = "uid=" + uid
    set_cookie = [("Authentication",cookie)]
    return jsonsuccess,200,set_cookie

@app.route('/getfoodslist',methods=['GET'])
def getfoodslist():
    FoodsList = GetFoodsList()
    FoodsListJson = FoodsListToJson(FoodsList)
    if FoodsListJson == "-1":
        jsonerror = """{"errno":"1","errmsg":"Datbase error, check function FoodsListToJson"}"""
        return jsonerror

    jsonsuccess = """{"errno":"0","errmsg":"successful!","foodslist":%s }""" % FoodsListJson
    return jsonsuccess

@app.route('/cart/get',methods=['GET'])
def getcart():
    """鉴权，返回该用户的食品信息，最后加一个字段【数量】"""

    #可复用代码------------------
    uid = request.values.get('uid')
    uid_cookie = request.headers.get("Authentication")
    if uid_cookie == None:
        uid_cookie = "-1"
    
    if uid == None or uid == "" :
        jsonerror = """{"errno":"2","errmsg":"Missing required parameter."   }"""
        return jsonerror
    userlist = GetUsersByUid(uid)
    if userlist == []:
        jsonerror = """{"errno":"3","errmsg":"User does not exist."   }"""
        return jsonerror
    #鉴权
    if isLogin(uid,uid_cookie) == 0 :
        jsonerror = """{"errno":"4","errmsg":"Authentication failed."   }"""
        return jsonerror
    #---------------------------

    FoodsIds = str(userlist[7]).split(";")
    if FoodsIds == ['NULL'] or FoodsIds == [''] :
        jsonsuccess = """{"errno":"0","errmsg":"successful!","foodslist":[] }""" 
        return jsonsuccess
    
    FoodsIds.sort()
    FoodsList = []
    
    lastid = -1
    pos = -1
    for i in range(0,len(FoodsIds)) :
        #对每个id查询foods表获取信息，并且检查重复，若重复，则最后一个字段number++
        oneList = GetFoodsById(FoodsIds[i])
        if oneList == [] :
            lastid = -1
            continue
        if lastid == -1:
            lastid =oneList[0]
            oneList.append(1)
            FoodsList.append(oneList) 
            pos = len(FoodsList) - 1
            continue
            
        else:
            if lastid == oneList[0] : #与上条记录相同
                if pos == -1 :
                    print("---!!!--->算法错误！")
                FoodsList[pos][8] += 1
            else :  #与上条记录不同
                lastid = oneList[0]
                oneList.append(1)
                FoodsList.append(oneList) 
                pos = len(FoodsList) - 1
        

        


    FoodsListJson = FoodsCartListToJson(FoodsList)
    
    jsonsuccess = """{"errno":"0","errmsg":"successful!","foodslist":%s }""" % FoodsListJson
    return jsonsuccess

@app.route('/cart/add',methods=['POST'])
def addcart():
    """鉴权，添加该用户的食品信息(购物车)"""
    food_id = request.get_json().get('food_id')
    #可复用代码------------------
    uid = request.get_json().get('uid')
    uid_cookie = request.headers.get("Authentication")
    if uid_cookie == None:
        uid_cookie = "-1"
    
    if uid == None or uid == "" or food_id == None or food_id == "":
        jsonerror = """{"errno":"2","errmsg":"Missing required parameter."   }"""
        return jsonerror
    userlist = GetUsersByUid(uid)
    if userlist == []:
        jsonerror = """{"errno":"3","errmsg":"User does not exist."   }"""
        return jsonerror
    #鉴权
    if isLogin(uid,uid_cookie) == 0 :
        jsonerror = """{"errno":"4","errmsg":"Authentication failed."   }"""
        return jsonerror
    #---------------------------
    uList = GetUsersByUid(uid)
    pre_food_id = uList[7]
    if pre_food_id == "" or pre_food_id == "NULL" or pre_food_id == None :
        pre_food_id = food_id
    else :
        pre_food_id = pre_food_id + ";" + food_id

    UpdateUsersByUid(uid,"pre_food_id",pre_food_id)

    jsonsuccess = """{"errno":"0","errmsg":"successful!"}""" 
    return jsonsuccess

@app.route('/cart/delete',methods=['POST'])
def deletecart():
    """鉴权,若food_id == -2 ,清空cart,若大于0,查找并删除一个，若未找到，返回错误"""

    food_id = request.get_json().get('food_id')

    #可复用代码------------------
    uid = request.get_json().get('uid')
    uid_cookie = request.headers.get("Authentication")
    if uid_cookie == None:
        uid_cookie = "-1"
    
    if uid == None or uid == "" or food_id == None or food_id == "":
        jsonerror = """{"errno":"2","errmsg":"Missing required parameter."   }"""
        return jsonerror
    userlist = GetUsersByUid(uid)
    if userlist == []:
        jsonerror = """{"errno":"3","errmsg":"User does not exist."   }"""
        return jsonerror
    #鉴权
    if isLogin(uid,uid_cookie) == 0 :
        jsonerror = """{"errno":"4","errmsg":"Authentication failed."   }"""
        return jsonerror
    #---------------------------
    #验证food_id,若为-2，则清空uid的对应项，否则，获取cart，查找，去除，若未找到，返回error
    if food_id == "-2" :
        UpdateUsersByUid(uid,"pre_food_id","")
        jsonsuccess = """{"errno":"0","errmsg":"successful!"}""" 
        return jsonsuccess
    else:
        cart = str(GetUsersByUid(uid)[7])
        cartList = cart.split(";")
        isFind = 0
        for i in range(0,len(cartList)) :
            if food_id == cartList[i] :
                isFind = 1
                del cartList[i]
                break
        if isFind == 1 :
            cart = ';'.join(cartList)
            UpdateUsersByUid(uid,"pre_food_id",cart)
            jsonsuccess = """{"errno":"0","errmsg":"successful!"}""" 
            return jsonsuccess
        else :
            jsonerror = """{"errno":"5","errmsg":"Food does not exist in cart!"   }"""
            return jsonerror

@app.route('/order/make',methods=['POST'])
def makeorder():
    remark = request.get_json().get('remark')
    if remark == None :
        remark = ''
    #可复用代码------------------
    uid = request.get_json().get('uid')
    uid_cookie = request.headers.get("Authentication")
    if uid_cookie == None:
        uid_cookie = "-1"
    
    if uid == None or uid == "" :
        jsonerror = """{"errno":"2","errmsg":"Missing required parameter."   }"""
        return jsonerror
    userlist = GetUsersByUid(uid)
    if userlist == []:
        jsonerror = """{"errno":"3","errmsg":"User does not exist."   }"""
        return jsonerror
    #鉴权
    if isLogin(uid,uid_cookie) == 0 :
        jsonerror = """{"errno":"4","errmsg":"Authentication failed."   }"""
        return jsonerror
    #---------------------------
    foodIDs = str(GetUsersByUid(uid)[7])
    foodIDList = foodIDs.split(";")#
    TotalPrice = 0.0
    foodListBlank = 1 #是空的
    for ID in foodIDList :
        foodlist = GetFoodsById(ID)
        if foodlist == [] :
            continue
        foodListBlank = 0
        state = str(foodlist[7])
        if state == "0" : #无效
            jsonerror = """{"errno":"5","errmsg":"Invalid item in shopping cart!"   }"""
            return jsonerror
        TotalPrice += float(foodlist[4])
    if foodListBlank == 1 :
        jsonerror = """{"errno":"6","errmsg":"Cart is blank!"   }"""
        return jsonerror

    TotalPrice = str(round(TotalPrice,2))
    time = datetime.now().strftime("""%Y%m%d%H%M%S""")
    orderID = InsertTableOrders(foodIDs,uid,TotalPrice,time,"0","0",remark)
    UpdateUsersByUid(uid,"pre_food_id","")
    InsertTableMsgs(uid,time,"下单成功","您已成功下单，详情点击个人中心页面【我的订单】查看","0")
    InsertTableMsgs(BUSINESSID,time,"用户已下单","用户有新的订单，详情点击个人中心页面【我的订单】查看并处理","0")
    jsonsuccess = """{"errno":"0","errmsg":"successful!","oid":%s }""" % orderID
    return jsonsuccess

@app.route('/order/get/user',methods=['GET'])
def getorder():
    oid = request.values.get('oid')
    #可复用代码------------------
    uid = request.values.get('uid')
    uid_cookie = request.headers.get("Authentication")
    if uid_cookie == None:
        uid_cookie = "-1"
    
    if uid == None or uid == "" :
        jsonerror = """{"errno":"2","errmsg":"Missing required parameter."   }"""
        return jsonerror
    userlist = GetUsersByUid(uid)
    if userlist == []:
        jsonerror = """{"errno":"3","errmsg":"User does not exist."   }"""
        return jsonerror
    #鉴权
    if isLogin(uid,uid_cookie) == 0 :
        jsonerror = """{"errno":"4","errmsg":"Authentication failed."   }"""
        return jsonerror
    #---------------------------
    #TODO-------------------------->
    OrdersList = GetOrdersByUid(uid)
    #oid限制，若不匹配，则返回空
    NotExist = 1
    if oid != None and oid != "" :
        for Order in OrdersList :
            if oid == str(Order[0]) :
                OrdersList = [Order]
                NotExist = 0
                break
        if NotExist == 1 :
            OrdersList = []
    
    OrdersListJson = OrdersListToJson(OrdersList)          

    jsonsuccess = """{"errno":"0","errmsg":"successful!","orders":%s }""" % OrdersListJson
    return jsonsuccess

@app.route('/order/update',methods=['POST'])
def updateorder():
    oid = request.get_json().get('oid')
    event = request.get_json().get('event')
    remark = request.get_json().get('remark')

    #可复用代码------------------
    uid = request.get_json().get('uid')
    uid_cookie = request.headers.get("Authentication")
    if uid_cookie == None:
        uid_cookie = "-1"
    
    if uid == None or uid == "" or oid == None or oid == "" or event == "" or event == None :
        jsonerror = """{"errno":"2","errmsg":"Missing required parameter."   }"""
        return jsonerror
    userlist = GetUsersByUid(uid)
    if userlist == []:
        jsonerror = """{"errno":"3","errmsg":"User does not exist."   }"""
        return jsonerror
    #登陆鉴权
    if isLogin(uid,uid_cookie) == 0 :
        jsonerror = """{"errno":"4","errmsg":"Authentication failed."   }"""
        return jsonerror
    #---------------------------
    oList = GetOrdersById(oid)
    if oList == [] :
        jsonerror = """{"errno":"6","errmsg":"Order does not exist!"   }"""
        return jsonerror
    oUid = oList[2]
    time = datetime.now().strftime("""%Y%m%d%H%M%S""")
    if event == "paid" : #已支付,进入服务,商家权限
        if uid != BUSINESSID :
            jsonerror = """{"errno":"4","errmsg":"Authentication failed."   }"""
            return jsonerror
        UpdateOrdersById(oid,"pay_state","1")
        UpdateOrdersById(oid,"serve_state","1")
        InsertTableMsgs(oUid,time,"支付成功","您已成功支付，商家正在为您备菜，请耐心等待","0")
    elif event == "unpaid" : #待支付,商家权限
        if uid != BUSINESSID :
            jsonerror = """{"errno":"4","errmsg":"Authentication failed."   }"""
            return jsonerror
        UpdateOrdersById(oid,"pay_state","0")
        UpdateOrdersById(oid,"serve_state","0")
    elif event == "invalid" : #无效,用户权限
        if uid != str(oList[2]) and uid != BUSINESSID:
            jsonerror = """{"errno":"4","errmsg":"Authentication failed."   }"""
            return jsonerror
        UpdateOrdersById(oid,"pay_state","2")
        UpdateOrdersById(oid,"serve_state","0")
        InsertTableMsgs(oUid,time,"订单无效","订单已撤销，若有疑问咨询商家","0")
    elif event == "served" : #服务完成,商家权限
        if uid != BUSINESSID :
            jsonerror = """{"errno":"4","errmsg":"Authentication failed."   }"""
            return jsonerror
        UpdateOrdersById(oid,"pay_state","1")
        UpdateOrdersById(oid,"serve_state","2")
        InsertTableMsgs(oUid,time,"订单完成","您的订单已经完成，如有疑问请咨询商家","0")
    elif event == "remark" : #增加标记备注,用户权限,检查是否是用户id对应的订单
        if uid != str(oList[2]) :
            jsonerror = """{"errno":"4","errmsg":"Authentication failed."   }"""
            return jsonerror
        if remark == None or remark == '' :
            jsonerror = """{"errno":"2","errmsg":"Missing required parameter."   }"""
            return jsonerror
        UpdateOrdersById(oid,"remark",remark)
    else :
        jsonerror = """{"errno":"5","errmsg":"event error"   }"""
        return jsonerror
    jsonsuccess = """{"errno":"0","errmsg":"successful!" }""" 
    return jsonsuccess

@app.route('/foods/update',methods=['POST'])
def updatefoods():
    """uid,name,type,old_price,new_price,introduce,img,state\n
        
    """
    fid = request.form.get('fid')
    name = request.form.get('name')
    types = request.form.get('type')
    old_price = request.form.get('old_price')
    new_price = request.form.get('new_price')
    introduce= request.form.get('introduce')
    img = request.files.get('img')
    state = request.form.get('state')
    #可复用代码------------------
    uid = request.form.get('uid')
    uid_cookie = request.headers.get("Authentication")
    if uid_cookie == None:
        uid_cookie = "-1"
    print(request.form,request.files)
    if fid == None or fid == ""or uid == None or uid == "" or name == None or name == "" or types == "" or types == None or\
        old_price == "" or old_price == None or new_price == None or new_price == "" or\
        img == None or img == "" or state == None or state == "":
        jsonerror = """{"errno":"2","errmsg":"Missing required parameter."   }"""
        return jsonerror
    if introduce == None :
        introduce = ""
    userlist = GetUsersByUid(uid)
    if userlist == []:
        jsonerror = """{"errno":"3","errmsg":"User does not exist."   }"""
        return jsonerror
    #登陆鉴权
    if isLogin(uid,uid_cookie) == 0 :
        jsonerror = """{"errno":"4","errmsg":"Authentication failed."   }"""
        return jsonerror
    #---------------------------
    if uid != BUSINESSID : #商家权限验证
        jsonerror = """{"errno":"4","errmsg":"Authentication failed. Only business can do this."   }"""
        return jsonerror
    randname = "".join(random.sample('zyxwvutsrqponmlkjihgfedcbaQWERTYUIOPASDFGHJKLZXCVBNM',20))

    randname = "./imgs/" + randname + ".jpg"
    img.save(randname)
    randname = randname[7:]
    UpdateFoodsById(fid,name,types,old_price,new_price,introduce,randname,state)
    
    jsonsuccess = """{"errno":"0","errmsg":"successful!" }""" 
    return jsonsuccess
    
@app.route('/foods/add',methods=['POST'])
def addfoods():
    """uid,name,type,old_price,new_price,introduce,img,state\n
        
    """
    
    name = request.form.get('name')
    types = request.form.get('type')
    old_price = request.form.get('old_price')
    new_price = request.form.get('new_price')
    introduce= request.form.get('introduce')
    img = request.files.get('img')
    state = request.form.get('state')
    #可复用代码------------------
    uid = request.form.get('uid')
    uid_cookie = request.headers.get("Authentication")
    if uid_cookie == None:
        uid_cookie = "-1"
    print(request.form,request.files)
    if uid == None or uid == "" or name == None or name == "" or types == "" or types == None or\
        old_price == "" or old_price == None or new_price == None or new_price == "" or\
        img == None or img == "" or state == None or state == "":
        jsonerror = """{"errno":"2","errmsg":"Missing required parameter."   }"""
        return jsonerror
    if introduce == None :
        introduce = ""
    userlist = GetUsersByUid(uid)
    if userlist == []:
        jsonerror = """{"errno":"3","errmsg":"User does not exist."   }"""
        return jsonerror
    #登陆鉴权
    if isLogin(uid,uid_cookie) == 0 :
        jsonerror = """{"errno":"4","errmsg":"Authentication failed."   }"""
        return jsonerror
    #---------------------------
    if uid != BUSINESSID : #商家权限验证
        jsonerror = """{"errno":"4","errmsg":"Authentication failed. Only business can do this."   }"""
        return jsonerror
    randname = "".join(random.sample('zyxwvutsrqponmlkjihgfedcbaQWERTYUIOPASDFGHJKLZXCVBNM',20))

    randname = "./imgs/" + randname + ".jpg"
    img.save(randname)
    randname = randname[7:]
    InsertTableFoods(name,types,old_price,new_price,introduce,randname,state)
    
    jsonsuccess = """{"errno":"0","errmsg":"successful!" }""" 
    return jsonsuccess
@app.route('/foods/delete',methods=['GET','POST'])
def deletefoods():
    fid = request.values.get('fid')
    #可复用代码------------------
    uid = request.values.get('uid')
    uid_cookie = request.headers.get("Authentication")
    if uid_cookie == None:
        uid_cookie = "-1"
    
    if uid == None or uid == "" or fid == None or fid == ""  :
        jsonerror = """{"errno":"2","errmsg":"Missing required parameter."   }"""
        return jsonerror
    userlist = GetUsersByUid(uid)
    if userlist == []:
        jsonerror = """{"errno":"3","errmsg":"User does not exist."   }"""
        return jsonerror
    #登陆鉴权
    if isLogin(uid,uid_cookie) == 0 :
        jsonerror = """{"errno":"4","errmsg":"Authentication failed."   }"""
        return jsonerror
    #---------------------------
    if uid != BUSINESSID : #商家权限验证
            jsonerror = """{"errno":"4","errmsg":"Authentication failed.Only business can do this."   }"""
            return jsonerror
    DeleteFoodsById(fid)
    jsonsuccess = """{"errno":"0","errmsg":"successful!" }""" 
    return jsonsuccess
@app.route('/order/get/business',methods=['GET'])
def getorderb():

    state_type = request.values.get('state_type')
    #可复用代码------------------
    uid = request.values.get('uid')
    uid_cookie = request.headers.get("Authentication")
    if uid_cookie == None:
        uid_cookie = "-1"
    
    if uid == None or uid == "" or state_type == None or state_type == "" :
        jsonerror = """{"errno":"2","errmsg":"Missing required parameter."   }"""
        return jsonerror
    userlist = GetUsersByUid(uid)
    if userlist == []:
        jsonerror = """{"errno":"3","errmsg":"User does not exist."   }"""
        return jsonerror
    #登陆鉴权
    if isLogin(uid,uid_cookie) == 0 :
        jsonerror = """{"errno":"4","errmsg":"Authentication failed."   }"""
        return jsonerror
    #---------------------------
    if uid != BUSINESSID : #商家权限验证
            jsonerror = """{"errno":"4","errmsg":"Authentication failed.Only business can do this."   }"""
            return jsonerror
    OrderList = []
    if state_type == "unpaid":
        OrderList = GetOrdersByState("0","0")
    elif state_type == "paid":
        OrderList = GetOrdersByState("1","1")
    elif state_type == "invalid":
        OrderList = GetOrdersByState("2","0")
    elif state_type == "served":
        OrderList = GetOrdersByState("1","2")
    else :
        jsonerror = """{"errno":"5","errmsg":"State type error."   }"""
        return jsonerror
    OrdersListJson = OrdersListToJson(OrderList)
    jsonsuccess = """{"errno":"0","errmsg":"successful!","orders":%s }""" % OrdersListJson
    return jsonsuccess

@app.route('/userdata/get',methods=['GET'])
def getuserdata():
    theUid = request.values.get('theuid')
    uid = request.values.get('uid')
    uid_cookie = request.headers.get("Authentication")
    if uid_cookie == None:
        uid_cookie = "-1"
    if uid == None or uid == ""  :
        jsonerror = """{"errno":"2","errmsg":"Missing required parameter."   }"""
        return jsonerror
    userlist = GetUsersByUid(uid)
    if userlist == []:
        jsonerror = """{"errno":"3","errmsg":"User does not exist."   }"""
        return jsonerror
    #登陆鉴权
    if isLogin(uid,uid_cookie) == 0 :
        jsonerror = """{"errno":"4","errmsg":"Authentication failed."   }"""
        return jsonerror
    if (uid != BUSINESSID and uid != ROOTID) and theUid != uid:#非商家只能查看自己信息
        jsonerror = """{"errno":"4","errmsg":"Authentication failed."   }"""
        return jsonerror
    UList = GetUsersByUid(theUid)
    if UList == []:
        jsonerror = """{"errno":"5","errmsg":"the searched User does not exist."   }"""
        return jsonerror
    UListJson =  UserListToJson(UList)
    jsonsuccess = """{"errno":"0","errmsg":"successful!","user":%s }""" % UListJson
    return jsonsuccess

@app.route('/userdata/update',methods=['POST'])
def updateuserdata():

    updateid = request.get_json().get('updateid')
    event = request.get_json().get('event')
    parm = request.get_json().get('parm')
    #可复用代码------------------
    uid = request.get_json().get('uid')
    uid_cookie = request.headers.get("Authentication")
    if uid_cookie == None:
        uid_cookie = "-1"
    
    if uid == None or uid == "" or updateid == None or updateid == "" or event == ""\
        or event == None or parm == "" or parm == None  :
        jsonerror = """{"errno":"2","errmsg":"Missing required parameter."   }"""
        return jsonerror
    userlist = GetUsersByUid(uid)
    if userlist == []:
        jsonerror = """{"errno":"3","errmsg":"User does not exist."   }"""
        return jsonerror
    #登陆鉴权
    if isLogin(uid,uid_cookie) == 0 :
        jsonerror = """{"errno":"4","errmsg":"Authentication failed."   }"""
        return jsonerror
    #---------------------------
    if uid != updateid and uid != ROOTID:
        jsonerror = """{"errno":"5","errmsg":"Only ROOT can change other user data"   }"""
        return jsonerror
    if event != "name" and event != "address" and event != "phone" and\
        event !="passwd" and event !="table_number":
        jsonerror = """{"errno":"6","errmsg":"Event error."   }"""
        return jsonerror
    UpdateUsersByUid(updateid,event,parm)
    jsonsuccess = """{"errno":"0","errmsg":"successful!" }""" 
    return jsonsuccess
@app.route('/dialog',methods=['POST'])
def dialog():

    content = request.get_json().get('content')
    #可复用代码------------------
    uid = request.get_json().get('uid')
    uid_cookie = request.headers.get("Authentication")
    if uid_cookie == None:
        uid_cookie = "-1"
    
    if uid == None or uid == "" or content == None or content == "":
        
        jsonerror = """{"errno":"2","errmsg":"Missing required parameter."   }"""
        return jsonerror
    userlist = GetUsersByUid(uid)
    if userlist == []:
        jsonerror = """{"errno":"3","errmsg":"User does not exist."   }"""
        return jsonerror
    #登陆鉴权
    if isLogin(uid,uid_cookie) == 0 :
        jsonerror = """{"errno":"4","errmsg":"Authentication failed."   }"""
        return jsonerror
    #---------------------------
    #TODO:将文字传给recognition,获取返回的操作码，操作参数，回复文字，返回给前端
    action = ContentInAndOut(content,uid)
    voicePath = action[1]
    url = url_for("voice",voicename=voicePath)
    jsonsuccess = """{"errno":"0","errmsg":"successful!","action": %s,"replyurl":"%s" }""" % (action[0],url)
    return jsonsuccess
@app.route('/voice',methods=['GET'])
def voice():
    name = request.values.get("voicename")
    if name == None or name == "":
        jsonerror = """{"errno":"2","errmsg":"Missing required parameter."   }"""
        return jsonerror
    name = "./voice/"+name
    print("--->")
    f = open(name,"rb")
    farray=f.read()
    f.close()
    b64 = base64.b64encode(farray)
    return b64
@app.route('/img',methods=['GET'])
def img():
    name = request.values.get("imgname")
    if name == None or name == "":
        jsonerror = """{"errno":"2","errmsg":"Missing required parameter."   }"""
        return jsonerror
    name = "./imgs/"+name
    print("--->")
    return send_file(name),200,[("Content-Type","images/jpeg")]
@app.route('/send/voice',methods=['GET','POST'])
def sendvoice():
    voice = request.files.get("voice")
    
    
    
    if voice == None :
        jsonerror = """{"errno":"2","errmsg":"Missing required parameter."   }"""
        return jsonerror
    randname = "".join(random.sample('zyxwvutsrqponmlkjihgfedcbaQWERTYUIOPASDFGHJKLZXCVBNM',20))

    randname = "./audios/" + randname + ".wav"
    voice.save(randname)
    textMessage = voiceToText.voiceToText(randname)
    
    jsonsuccess = """{"errno":"0","errmsg":"successful!","message":"%s" }""" % textMessage
    return jsonsuccess
@app.route('/msg/read',methods=['POST'])
def msgRead():
    mid = request.get_json().get('msg_id')
    #可复用代码------------------
    uid = request.get_json().get('uid')
    uid_cookie = request.headers.get("Authentication")
    if uid_cookie == None:
        uid_cookie = "-1"
    
    if uid == None or uid == "" or mid == None or mid == "":
        
        jsonerror = """{"errno":"2","errmsg":"Missing required parameter."   }"""
        return jsonerror
    userlist = GetUsersByUid(uid)
    if userlist == []:
        jsonerror = """{"errno":"3","errmsg":"User does not exist."   }"""
        return jsonerror
    #登陆鉴权
    if isLogin(uid,uid_cookie) == 0 :
        jsonerror = """{"errno":"4","errmsg":"Authentication failed."   }"""
        return jsonerror
    #---------------------------
    MsgHasReadById(mid)
    jsonsuccess = """{"errno":"0","errmsg":"successful!" }"""
    return jsonsuccess
@app.route('/msg/get',methods=['get'])
def msgGet():
    #可复用代码------------------
    uid = request.values.get('uid')
    uid_cookie = request.headers.get("Authentication")
    if uid_cookie == None:
        uid_cookie = "-1"
    
    if uid == None or uid == "":
        
        jsonerror = """{"errno":"2","errmsg":"Missing required parameter."   }"""
        return jsonerror
    userlist = GetUsersByUid(uid)
    if userlist == []:
        jsonerror = """{"errno":"3","errmsg":"User does not exist."   }"""
        return jsonerror
    #登陆鉴权
    if isLogin(uid,uid_cookie) == 0 :
        jsonerror = """{"errno":"4","errmsg":"Authentication failed."   }"""
        return jsonerror
    #---------------------------
    msgList = GetMsgsById(uid)
    msgListJson = MsgsListToJson(msgList)
    jsonsuccess = """{"errno":"0","errmsg":"successful!","msgs": %s }""" % msgListJson
    return jsonsuccess

@app.route('/test')
def test():
    

    s ="""
     <h1>接口测试</h1>
     <a href='/register?name=测试&address=&phone=12345678910&uname=test&passwd=test' >click here to register</>
     <br>
     <a href='/login?uname=test&passwd=test' >click here to login test</>
     <br>
     <a href='/logout' >click here to logout</>
     <br>
     <a href='/getfoodslist' >click here to get foods list</>
     <br>
     <a href='/cart/get?uid=3' >click here to get cart</>
     <br>
     <a href='/cart/add?uid=3&food_id=1' >click here to add food into cart</>
     <br>
     <a href='/cart/delete?uid=3&food_id=1' >click here to delete food from cart</>
     <br>
     <a href='/cart/delete?uid=3&food_id=-2' >click here to clear cart</>
     <br>
     <a href='/order/make?uid=3&remark=少放辣' >click here to make an order</>
     <br>
     <a href='/order/get/user?uid=3' >click here to get order</>
     <br>
     <a href='/order/update?uid=3&oid=1&event=' >click here to update order</>
     <br>
     <a href='/foods/update?uid=2&fid=1&event=name&parm=好吃小炒肉' >click here to update foods</>
     <br>
     <a href='/foods/add?uid=2&name=白面&type=主食&old_price=12.88&new_price=9.9&introduce=一份面&img=图片路径&state=1' >click here to add foods</>
     <br>
     <a href='/dialog?uid=3&content=退出登陆' >click here to test dialog</>
     <br>
     """
    #注意，数据插入函数不可在此处使用，此时只为测试用
    #InsertTableTest("13","TRUST ME")
    #InsertTableUsers("陈涛","云南","17874526781","CNeptune","ct5935836","22",'')
    #UpdateUsersByUname("CNeptune","table_number","14")
    

    #InsertTableFoods("五花肉","爆品","28.99","22.99","","/imgs/1211143.jpg",1)
    # UpdateFoodsByName("小炒肉花","state","0")
    # print(GetFoodsByName("小炒肉花"))
    # print(GetFoodsList())

    # l0 = InsertTableDialogs("1","20220312114824","0","","你好呀")
    # l1 = GetDialogsById("1")
    # l2 = GetDialogsByUid("1")
    # # UpdateDialogsById(str(l0),"content","我不好")
    # # UpdateDialogsById(str(l0),"msg_type","1")
    # l4 = GetDialogsByUid("1")
    # s = str(l1) + str(l2) + str(l4)
    
    return s

if __name__ == '__main__':
    app.run(debug=False,host="0.0.0.0",port=5000)