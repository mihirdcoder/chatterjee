#1 import numpy as np and find version

import numpy as np
print(np.__version__)


#2 Create 1D array

#way1
list1 = [0,1,2,3,4,5,6,7,8,9]
array1 = np.array(list1)
print(array1)
#way2
array2 = np.arange(10)
print(array2)

#3 How to create a boolean array
#way1
list2 = [[1,1,1],[1,1,1],[1,1,1]]
array3 = np.array(list2, dtype='bool')
print(array3)

#way2
array4 = np.full((3,3), True, dtype=bool)
print(array4)

#way3
array5 = np.ones((3,3), dtype=bool)
print(array5)

#4 Extract all odd numbers from array
#way1
list3 = []
for a in array1:
    if a%2 == 1:
        list3.append(a)
array6 = np.array(list3)
print(array6)

#way2
array7 = array1[array1 % 2 == 1]
print(array7)
print(array1)
#5 relpace terms satisfying condition
array1[array1 %2 == 1] = -1
print(array1)

'''The importatnt things from these 5 problems are:
1: Understand vectorized operations in numpy array. One of the important
   characterstic.
2: How to convert and iterarte over np array.

'''


