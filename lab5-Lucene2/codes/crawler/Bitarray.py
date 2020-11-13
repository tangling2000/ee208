# SJTU EE208

import math
import GeneralHashFunctions
import copy
import random

def get_random_string(k):  #取得一个长度为k的随机字符串
    import random
    return ''.join(random.sample([chr(i) for i in range(48, 123)], k))


class Bitarray:
    def __init__(self, size):
        """ Create a bit array of a specific size """
        self.size = size
        self.bitarray = bytearray(math.ceil(size / 8.))

    def set(self, n):
        """ Sets the nth element of the bitarray """

        index = int(n / 8)
        position = n % 8
        self.bitarray[index] = self.bitarray[index] | 1 << (7 - position)

    def get(self, n):
        """ Gets the nth element of the bitarray """

        index =int( n / 8)
        position = n % 8
        return (self.bitarray[index] & (1 << (7 - position))) >0


if __name__ == "__main__":

#本实验调用了GeneralHashFunctions 中的全部10个函数
#实验数据 随机字符串n个 取其中的m个进行测试

    n = 10**5
    m = 1000
    bitarray_obj = Bitarray((20*n))

    print("Initialized Data")
    datastring = [get_random_string(random.randint(8,24)) for i in range(n)] #bitarray中存储的数据
    teststring = copy.deepcopy(datastring[0:m]) #拷贝部分数据用于测试
    teststring = teststring + list(set([get_random_string(random.randint(8,24)) for i in range (n-m)])-set(datastring)) #生成若干个数据，除去超过m个，来自datastring的数据

    print("Setting...")

    for i in range(n):
        string = datastring.pop(0)
        for func in dir(GeneralHashFunctions):
            if func.endswith('Hash'):
                bitarray_obj.set(abs(getattr(GeneralHashFunctions,func)(string))%(20*n))
    
    print("Matching...")
    matchnum=0 #匹配个数
    for i in range (n):
        string = teststring.pop(0)
        f=0
        for func in dir(GeneralHashFunctions):
            if  func.endswith("Hash"):
                if bitarray_obj.get(abs(getattr(GeneralHashFunctions,func)(string))%(20*n))==1:
                    continue
                else :
                    f=1
                    break
        
        if f==0:
            matchnum+=1
    
    print("matchnum:{}".format(matchnum))
    print("FPR:{:.8f}".format((matchnum-m)/(matchnum))) #计算 false positiv rate

