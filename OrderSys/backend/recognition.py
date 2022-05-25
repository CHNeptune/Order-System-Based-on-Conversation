
from datetime import datetime
from random import randint
from time import  time
from seq2seqDialog.dialogControl import dialog
import jieba
import threading
import database
import getVoice
ContentGroupDict = {}
"""
格式：
{
    ID:[timestamp,question,content1,...,content10]
}
timestamp:记录最后一次对话发来的时间戳
question:记录最后一次对话的询问码\n
询问码<在开发中自行增加>:
    not : 不是询问

    ...文档添加到此处


"""
TIME_INTERVAL = 4
"""定时函数运行间隔"""
CLEAR_INTERVAL = 120
"""上下文清理间隔"""
CONTEXT_SIZE = 10
"""上下文存储对话条数"""
TRUST_VALUE = 40
"""语句匹配采信度,0-100"""

def getSuitKey(query:dict,askCode:str)->dict:
    """query形式: {AskCode:[[语料一以及回复列表],[语料二以及回复列表]]}\n
        返回形式:{语料一:回复列表,语料2:回复列表}
    """
    re = {}
    for i in range(len(query[askCode])):
        re.update({query[askCode][i][0]:query[askCode][i][1:len(query[askCode][i])]})
    
    return re
def GetReplyOP(query:dict,AskCode:str,currentList:list):
    replyOps = getSuitKey(query,AskCode)
    #TODO:判断replyOps为空的情况
    replyOp = []
    if list(replyOps.keys())[0] != "*":
        #TODO:需要进行语料匹配分析,最匹配结果放入replyOp
        maxp = 0
        
        for k in replyOps.keys():
            p = suitPercent(k,currentList)
            if p > maxp and p > TRUST_VALUE:
                maxp = p
                replyOp = replyOps[k]
    else:
        replyOp = replyOps["*"].copy()
    return replyOp
def CharacterRecognition(ContentGroup:list,id:str):
    """
    入参形式:list[时间戳,询问码,上下文1,上下文2,...]
    返回形式: list[响应文字,操作码,操作参数1,操作参数2,...]
    操作码: user question anwser exit foods showcart addcart deletecart
    参数：
    
    """
    ##解释：
    #->返回操作码为question时，表明返回了一个询问，已经记录该条对话的询问码，下条文字到达时，优先检查上下文的询问码是否为询问
    #若是询问，则根据询问码进行专门匹配分析
    #若不是询问，则按下述流程分析
    #------------------------------------------------
    #需要先去掉中文停用词,生成语言list
    #然后匹配dialog文件（文字符合率高于某个值则认为匹配）
    #获得操作码和所有回答可能
    #★此处可能系统会向用户确认一些问题，可能修改询问码
    #根据操作码和语言list确定操作是否有效
    #返回接口形式的响应文字，操作码，操作参数
    #
    #如果dialog不匹配，则认为不是任务式对话
    
    contentList = ContentGroup.copy()
    current = contentList.pop()
    #去停用词，分词为list
    currentList = list(jieba.cut(current))
    RemoveStopWords(currentList)
    print("当前语句分词：",currentList)
    TheWord = PopTheWord(currentList)
    print("The Words:",TheWord)
    AskCode= ContentGroup[1]
    RE = []
    foodIDs = database.GetUsersByUid(id)[7]
    """购物车序列，未分割"""   

    #TODO:获取query文件的回复内容
    query = {}
    qf = open("query.data","r",encoding="utf-8")
    qList = qf.readlines()
    for q in qList:
        if q[0] == "#":
            continue
        q = q.split(" ")
        qkey = q[0]
        del q[0]
        
        if  qkey in query.keys():
            query[qkey].append(q)
        else:
            q=[q]    
            query.update({qkey:q})
    #print("query字典:",query)
    if foodIDs != "":
        foodIDsL = foodIDs.split(";")
    else:
        foodIDsL = []
    foodNames = foodIDsL.copy()
    
    for each in range(len(foodNames)):
        name =  database.GetFoodsById(foodIDsL[each])
        foodNames[each] = name[1]
    foodNamesDict = {}
    for f in foodNames:
        if foodNamesDict.get(f) == None:
            foodNamesDict.update({f:1})
        else:
            foodNamesDict.update({f:foodNamesDict.get(f)+1})
    fL = []
    for k in foodNamesDict.keys():
        fL.append(str(foodNamesDict[k])+"份"+k)
    foodNames = "，".join(fL)
    if AskCode == "not" :
        df = open("dialog.data","r",encoding="utf-8")
        dialogList = df.readlines()
        df.close()
        maxsp = 0
        maxEveryList = []
        for dl in dialogList:
            if dl[0] == "#":
                continue
            everyList = dl.split(" ")

            sp = suitPercent(everyList[0],currentList)

            if sp > maxsp and sp >= TRUST_VALUE:
                maxsp = sp
                maxEveryList = everyList
        #现在已经得到最匹配的语料行，和TheWord
        #根据操作码让系统走不同分支 
        #未匹配        
        if maxsp == 0:
            #TODO:进行开放式语料识别
            A = dialog(current)
            return [A,"anwser"]
            
        #已经匹配
        operate = maxEveryList[1]
        sureReply = maxEveryList[2]
        denyReply = maxEveryList[3]
        sureReply = sureReply.split("/")
        denyReply = denyReply.split("/")
#########单步无额外信息任务，可以在此处复用操作#########
        if operate == "logout" or operate == "exit" or operate == "opencontinue" or operate == "closecontinue":
            RE.append(sureReply[randint(0,len(sureReply)-1)])
            RE.append(operate)
            return RE       
        elif operate == "foods":
            #对sureReply list 做检查，若有%foods,替换
            #TODO:检查TheWord是否有类别参数，若无，随机选择类别报菜;若有,返回moreReply,选择指定类别报菜
            types = database.GetValidFoodsTypeList()
            hasType = False
            fType = ""
            if TheWord == []:
                hasType = False
            else:
                fType = TheWord[0]
                if fType in types:
                    hasType = True
                else:
                    hasType =False

            if hasType == False:
                
                randType = types[randint(0,len(types)-1)]
                names = database.GetTypeFoodsNameList(randType)
                names = "，".join(names)
                for i in range(len(sureReply)):
                    sureReply[i] = sureReply[i].replace("%foods",names)
                    sureReply[i] = sureReply[i].replace("%type",randType)
                RE.append(sureReply[randint(0,len(sureReply)-1)])
                RE.append(operate)
                RE.append(randType)
                return RE
            else:
                names = database.GetTypeFoodsNameList(fType)
                names = "，".join(names)
                moreReply = maxEveryList[4]
                moreReply = moreReply.split("/")
                for i in range(len(moreReply)):
                    moreReply[i] = moreReply[i].replace("%foods",names)
                    moreReply[i] = moreReply[i].replace("%type",fType)
                RE.append(moreReply[randint(0,len(moreReply)-1)])
                RE.append(operate)
                RE.append(fType)
                return RE
        elif operate == "showcart":
            #查询数据库获取购物车id，根据id获取名字
            
            if foodIDs == None or foodIDs == "":
                #购物车为空
                RE.append(denyReply[randint(0,len(denyReply)-1)])
                RE.append(operate)
                return RE
            #TODO:对foodsNames进行处理，合并为菜名+份数
            for i in range(len(sureReply)):
                sureReply[i] = sureReply[i].replace("%carts",foodNames)
            
            RE.append(sureReply[randint(0,len(sureReply)-1)])
            RE.append(operate)
            return RE
        elif operate == "deletecart":
            #获取食物名对应id，在购物车里查找是否存在，存在则回复删除指令，不存在就说不存在
            if TheWord == []:
                #TODO:采用附加回复，进入询问状态，获取菜名参数
                moreReply = maxEveryList[4]
                ContentGroup[1] = "deletecartneedname"
                RE.append(moreReply)
                RE.append("question")
                return RE
            fList = database.GetFoodsByName(TheWord[0])
            if fList == []:
                RE.append(denyReply[randint(0,len(denyReply)-1)])
                RE.append("anwser")
                return RE
            fid = str(fList[0])
            if fid not in foodIDs.split(";"):
                RE.append(denyReply[randint(0,len(denyReply)-1)])
                RE.append("anwser")
                return RE
            else:
                RE.append(sureReply[randint(0,len(sureReply)-1)])
                RE.append(operate)
                RE.append(fid)
                return RE
        elif operate == "addcart":
            #获取食物名对应id，在购物车查找是否存在，存在则回复又添加了一份该菜，不存在则回复已经为您添加
            #若TheWord为空，则说没听清，转入询问处理
            if TheWord == []:
                #TODO:采用附加回复，进入询问状态，获取菜名参数
                moreReply = maxEveryList[4]
                ContentGroup[1] = "addcartneedname"
                RE.append(moreReply)
                RE.append("question")
                return RE
            fidList = database.GetFoodsByName(TheWord[0])
            if fidList == []:
                RE.append(denyReply[randint(0,len(denyReply)-1)])
                RE.append("anwser")
                return RE
            fid = str(fidList[0])


            if fid in foodIDs.split(";"):
                MoreReply = maxEveryList[5]
                MoreReply = MoreReply.replace("%food",TheWord[0])
                RE.append(MoreReply)
                RE.append(operate)
                RE.append(fid)
                return RE
            else:
                for i in range(len(sureReply)):
                    sureReply[i] = sureReply[i].replace("%food",TheWord[0])
                RE.append(sureReply[randint(0,len(sureReply)-1)])
                RE.append(operate)
                RE.append(fid)
                return RE
        elif operate == "clearcart":
            if foodIDs == None or foodIDs == "":
                #购物车为空
                RE.append(denyReply[randint(0,len(denyReply)-1)])
                RE.append("anwser")
                return RE
            RE.append(sureReply[randint(0,len(sureReply)-1)])
            RE.append(operate)
            return RE
        elif operate == "makeorder":
            #执行下单操作，若购物车为空，返回anwser说先添加到购物车
            #直接转到询问（桌号是多少，是否准确）
            #回复带上购物品车的菜，预计花费，确认吗
            if foodIDs == None or foodIDs == "":
                #购物车为空
                RE.append(denyReply[randint(0,len(denyReply)-1)])
                RE.append("anwser")
                return RE
            
            table_number = database.GetUsersByUid(id)[6]
            if table_number == None:
                ContentGroup[1] = "orderquestion_1"
                RE.append(sureReply[randint(0,len(sureReply)-1)] + maxEveryList[4])
                RE.append("question")
                return RE
            else:
                ContentGroup[1] = "orderquestion_2"
                moreReply = maxEveryList[5].replace("%table_number",str(table_number))
                RE.append(sureReply[randint(0,len(sureReply)-1)] + moreReply)
                RE.append("question")
                return RE
        elif operate == "anwser":
            RE = []
            RE.append(sureReply[randint(0,len(sureReply)-1)])
            RE.append(operate)
            return RE
    elif AskCode == "orderquestion_1":#桌号是多少
        replyOp = GetReplyOP(query,AskCode,currentList)
        ContentGroup[1] = "not"
        if replyOp == []:
            RE.append("抱歉,我不理解你的意思")
            RE.append("anwser")
            return RE
        num = None
        for c in currentList:
            try:
                num = int(c)
            except:
                pass
        if num == None:
            RE.append(replyOp[2])
            RE.append("anwser")
            return RE
        else:
            database.UpdateUsersByUid(id,"table_number",num)
            sureReply = replyOp[1].replace("%foods",foodNames)
            price = 0.0
            for f in foodIDsL:
                price += float(database.GetFoodsById(f)[4])
            price = round(price,2)
            sureReply = sureReply.replace("%price",str(price)) 
            RE.append(sureReply)
            RE.append("question")
            ContentGroup[1] = "orderconfirm"
            return RE   
    elif AskCode == "orderquestion_2":#桌号是否为已有值
        replyOp = GetReplyOP(query,AskCode,currentList)
        ContentGroup[1] = "not"
        if replyOp == []:
            RE.append("抱歉,我不理解你的意思")
            RE.append("anwser")
            return RE
        if replyOp[0] == "yes":
            ContentGroup[1] = "orderconfirm"
            sureReply = replyOp[1].replace("%foods",foodNames)
            price = 0.0
            for f in foodIDsL:
                price += float(database.GetFoodsById(f)[4])
            price = round(price,2)
            sureReply = sureReply.replace("%price",str(price)) 
            RE.append(sureReply)
            RE.append("question")
            return RE
        elif replyOp[0] == "no":
            RE.append(replyOp[1])
            ContentGroup[1] = "orderquestion_1"
            RE.append("question")
            return RE     
    elif AskCode == "orderconfirm":
        replyOp = GetReplyOP(query,AskCode,currentList)
        ContentGroup[1] = "not"
        if replyOp == []:
            RE.append("抱歉,我不理解你的意思")
            RE.append("anwser")
            return RE
        if replyOp[0] == "yes":
            RE.append(replyOp[1])
            RE.append("makeorder")
            return RE
        elif replyOp[0] == "no":
            RE.append(replyOp[1])
            RE.append("anwser")
            return RE
    elif AskCode == "deletecartneedname":
        replyOp = GetReplyOP(query,AskCode,currentList)
        ContentGroup[1] = "not"
        if replyOp == []:
            RE.append("抱歉,我不理解你的意思")
            RE.append("anwser")
            return RE
        if TheWord == []:
            #还是没有获取回答
            RE.append(replyOp[2])
            RE.append("anwser")
            return RE
        
        fList = database.GetFoodsByName(TheWord[0])
        if fList == []:
            RE.append(replyOp[3])
            RE.append("anwser")
            return RE
        fid = str(fList[0])
        if fid not in foodIDs.split(";"):
            RE.append(replyOp[3])
            RE.append("anwser")
            return RE
        else:
            RE.append(replyOp[1])
            RE.append("deletecart")
            RE.append(fid)
            return RE
    elif AskCode == "addcartneedname":   

        replyOp = GetReplyOP(query,AskCode,currentList)
        ContentGroup[1] = "not"
        if replyOp == []:
            RE.append("抱歉,我不理解你的意思")
            RE.append("anwser")
            return RE

        if TheWord == []:
            #还是没有获取回答
            RE.append(replyOp[2])
            RE.append("anwser")
            return RE
        
        fList = database.GetFoodsByName(TheWord[0])
        for r in range(len(replyOp)):
            replyOp[r] = replyOp[r].replace("%food",TheWord[0])
        if fList == []:
            RE.append(replyOp[3])
            RE.append("anwser")
            return RE
        fid = str(fList[0])
        if fid in foodIDs.split(";"):
            RE.append(replyOp[4])
            RE.append("addcart")
            RE.append(fid)
            return RE
        else:
            RE.append(replyOp[1])
            RE.append("addcart")
            RE.append(fid)
            return RE
    return ["我还不理解你的意思","anwser"]
def ContentInAndOut(content:str,id:str):
    """
    维护一个用户id的上下文(字典<列表<字符串>>结构)
    返回处理后的json回应序列
    """
    global ContentGroupDict
    contentList = ContentGroupDict.get(id)
    now = int(time())
    if contentList == None :
        listNow = []
        listNow.append(now)
        listNow.append("not")
        listNow.append(content)
        ContentGroupDict.update({id:listNow})
    else :
        contentList = list(contentList).copy()
        contentList[0]=now
        
        if len(contentList) >= CONTEXT_SIZE + 2:
            del contentList[2]
        contentList.append(content)
        ContentGroupDict.update({id:contentList})
    #文字处理，直接传入该用户指针
    resultList =  CharacterRecognition(ContentGroupDict[id],id)
    reply = resultList[0]
    opcode = resultList[1]
    parm = []
    for i in range(2,len(resultList)):
        parm.append(resultList[i])
    parm = " ".join(parm)
    #将对话存入数据库，包括用户的和系统的
    timess = datetime.now().strftime("""%Y%m%d%H%M%S""")
    database.InsertTableDialogs(id,timess,"user","",content)
    database.InsertTableDialogs(id,timess,opcode,parm,reply)

    jsonstr = """{
        "reply": "%s",
        "opcode": "%s",
        "parm": "%s"

    }
    
    """ % (reply,opcode,parm)

    
    voicePath = getVoice.getVoice(reply)
    return (jsonstr,voicePath)
def clear():
    """定时清理上下文字典"""
    keys = list(ContentGroupDict.keys())
    for k in keys :
        contentList = ContentGroupDict.get(k)
        if(contentList == None):
            continue
        last_time = contentList[0]
        now = int(time())
        if now - last_time >= CLEAR_INTERVAL :
            del ContentGroupDict[k]
def suitPercent(keywords:str,content:list)-> int:
    """入参：
            关键词语料(格式: AA-BB/CC-DD),文本词组
        出参：
            匹配度
        入参需要去除标点，自定义词典(临时存放作为操作参数)的内容，
        出参输出匹配度(100为满,0为最小)
    """
    kList = keywords.split("/")
    maxpercent = 0
    for i in range(len(kList)):
        kList[i] = kList[i].split("-")
        kl = kList[i].copy()
        
        suit = 0
        notsuit = 0
        for c in content:
            if c in kl:
                suit += len(c)
                i = 0
                j = len(kl)
                while(i<j):
                    if kl[i] == c:
                        del kl[i]
                        break
                    i+=1
            else :
                notsuit += len(c)
        no = 0
        for kn in kl:
            no += len(kn)
        notsuit += no
        if suit == notsuit == 0:
            continue
        percent = int(suit / (suit + notsuit) * 100)
        if percent > maxpercent:
            maxpercent = percent
    return maxpercent
    #TODO
def PopTheWord(currentList:list)->list:
    TheWord = []
    keyWords = []
    f = open("dict.data","r",encoding='utf-8')
    strs = f.readlines()
    f.close()
    for s in strs:
        keyWords.append(s.split(" ")[0])

    i = 0
    lk = len(currentList)
    while(i<lk):
        if currentList[i] in keyWords:
            TheWord.append(currentList[i])
            del currentList[i]
            i-=1
            lk-=1

        i+=1
    return TheWord   
def RemoveStopWords(content:list)->list:
    f = open("stopwords.data","r",encoding="utf-8")
    s = f.read()
    stopList = s.split("\n")
    
    l = len(content)
    c = 0
    while(c<l):

        
        if content[c] in stopList:
            del content[c]
            c -= 1
            l -= 1
        c += 1

#-------------------定时执行函数-------------------------------
def run_timer():
    """定时执行"""
    #--------功能区-----------
    #print(ContentGroupDict)
    clear()

    f = open("dict.data","r+",encoding='utf-8')
    strs = f.read()
    words = strs.split("\n")
    FL = database.GetFoodsList()
    for F in FL:
        s = F[1]
        if s + " 99999 n" not in words :
            f.write(s+ " 99999 n\n")
    TP = database.GetValidFoodsTypeList()
    TP = set(TP)
    for T in TP:
        if T + " 99999 n" not in words :
            f.write(T+ " 99999 n\n")

    f.close()
    jieba.load_userdict("dict.data")
    #--------000000-----------
    threading.Timer(TIME_INTERVAL,run_timer).start()
run_timer()


#-------------------------------------------------------------
#print(suitPercent("你-是谁",["你","到底","是谁"]))

