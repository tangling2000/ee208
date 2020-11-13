# SJTU EE208

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


if __name__ == "__main__":
    bitarray_obj = Bitarray(32000)
    for i in range(5):
        print("Setting index %d of bitarray .." % i)
        bitarray_obj.set(i)
        print("bitarray[%d] = %d" % (i, bitarray_obj.get(i)))
