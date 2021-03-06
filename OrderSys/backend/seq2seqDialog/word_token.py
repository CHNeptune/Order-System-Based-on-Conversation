# coding:utf-8

import jieba
class WordToken(object):
    """
    功能：加载问答语料数据,jieba分词,词频统计,word2id,id2word
    """
    def __init__(self):
        # 最小起始id号, 保留的用于表示特殊标记
        self.START_ID = 4
        self.word2id_dict = {}
        self.id2word_dict = {}
    def load_file_list(self, file_list, min_freq):
        """
        加载样本文件列表，全部切词后统计词频，按词频由高到低排序后顺次编号
        并存到self.word2id_dict和self.id2word_dict中
        """
        words_count = {}
        for file in file_list:
            
            with open(file, 'r',encoding='utf-8') as file_object:
                for line in file_object.readlines():
                    
                    line = line.strip()
                    seg_list = jieba.cut(line)
                    for str in seg_list:
                        if str in words_count:
                            words_count[str] = words_count[str] + 1
                        else:
                            words_count[str] = 1
        
        sorted_list = [[v[1], v[0]] for v in words_count.items()]
        sorted_list.sort(reverse=True)
        
        for index, item in enumerate(sorted_list):
            word = item[1]
            if item[0] < min_freq:
                break
            self.word2id_dict[word] = self.START_ID + index
            self.id2word_dict[self.START_ID + index] = word
        
        return index

    def word2id(self, word):
        if word in self.word2id_dict:
            return self.word2id_dict[word]
        else:
            return None

    def id2word(self, id):
        id = int(id)
        if id in self.id2word_dict:
            return self.id2word_dict[id]
        else:
            return None
    def testDict1(self):
        return self.id2word_dict
    def testDict2(self):
        return self.word2id_dict
