from GeneralHashFunctions.GeneralHashFunctions import BKDRHash
from Bitarray import Bitarray
import random

def get_random_string():
    import random
    return ''.join(random.sample([chr(i) for i in range(48, 123)], 12))

class BloomFilter:
    def __init__(self,n):
        #对于基本参数进行设置
        self.k = 10
        self.m = n*20+1
        #这一步很关键，处以一个素数会让冲突减小一万倍
        self.bitarray = Bitarray(self.m)

    def hash_str(self,keyword,i):
        seed = eval("1313"+i*"13") # 31 131 1313 13131 131313 etc..
        hash = 0
        for i in range(len(keyword)):
            hash = (hash * seed) + ord(keyword[i])
        index = hash%self.m
        return index

    def add_keyword(self,keyword):
        for i in range(self.k):
            index = self.hash_str(keyword=keyword,i=i)
            self.bitarray.set(index)
        
    def check_keyword(self,keyword):
        for i in range(self.k):
            index = self.hash_str(keyword=keyword,i=i)
            if not self.bitarray.get(index):
                return False
        return True

if __name__ == "__main__":
    n = 1000
    word_list = []
    Bfilter = BloomFilter(n)
    for i in range(n):
        word = get_random_string()
        word_list.append(word)
        Bfilter.add_keyword(word)

    print(Bfilter.check_keyword(keyword=word_list[0]))

    r = 0
    for i in range(100000):
        if Bfilter.check_keyword(get_random_string()):
            r += 1
    r = r/100000.
    print(r)
    #得到冲突率