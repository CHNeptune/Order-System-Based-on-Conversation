"""模块调用方法测试与训练"""
from seq2seqDialog.dialogControl import dialog,train
content = input("输入>")
while content != "quit":
    if content == "train":
        train()
        break

    print("回复>",dialog(content))
    content = input("输入>")