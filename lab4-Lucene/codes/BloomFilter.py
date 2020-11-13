import random
import math


class Bitarray:
    def __init__(self, size):
        """ Create a bit array of a specific size """
        self.size = size
        self.bitarray = bytearray(math.ceil(size / 8.))
        #返回一个二进制数组，一个bit可以存一位信息，这样的确节省空间，向上取整，所以要用ceil，默认整除是向下取整

    def set(self, n):
        """ Sets the nth element of the bitarray """

        index = int(n / 8)
        #找到块位置
        position = n % 8
        #找到在块中的位置
        self.bitarray[index] = self.bitarray[index] | 1 << (7 - position)
        #对于1进行移位
        #进行或运算将其进行储存

    def get(self, n):
        """ Gets the nth element of the bitarray """

        index = int(n / 8)
        position = n % 8
        return (self.bitarray[index] & (1 << (7 - position))) > 0
        #进行且运算，如果重合，返回的是true，如果不重合，返回的是false

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
    #检验已放入单词经过后是否一定为True值

    e = 0
    for i in range(20):
        r = 0
        for j in range(100000):
            if Bfilter.check_keyword(get_random_string()):
                r += 1
        r = r/100000.
        e += r
        print(i)
    e /= 20
    print("the error rate should be about 0.000089")
    print("the error rate is {}".format(e))
    #得到冲突率