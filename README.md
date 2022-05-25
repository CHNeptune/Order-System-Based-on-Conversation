# -
订餐系统 语义识别 讯飞API

前端

缺少的依赖使用npm安装
使用了vue2，muse ui

开发目录为src

后端

tensorflow==1.5.0
python==3.6
提示缺少websocket库时，安装的是websocket-client
其它缺少的库，缺哪个安哪个就行

app.py flask主程序
recognition.py 语义识别
database.py 数据库
dialog.data 检索语料库
dict.data 自定义字典（自动生成）
function.py 功能函数
getVoice.py 文字转语音
query.data 询问语料库
seqTest.py seq2seq 模型训练和测试
stopwords.data 停用词
voiceToText.py 语音转文字
