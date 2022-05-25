import jieba
jieba.load_userdict("./dict.data")
while(True):
    s = input("输入>")
    print("分词>","|".join(list(jieba.cut(s))))