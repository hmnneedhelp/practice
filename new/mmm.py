import numpy

import matplotlib.pyplot as plt
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot()


# data_file=open('mnist_test_10.csv','r')
data_file=open('image_data.csv','r')
data_list=data_file.readlines()
data_file.close()
all_values=data_list[0].split(',')
print(all_values)
image_array=numpy.asfarray(all_values[0:]).reshape((70,70))
print(image_array)
# plt.imshow(image_array, cmap='Greys', interpolation='None')
ax.imshow(image_array,cmap='gray')
plt.show()


print(len(data_list))
# print(data_list[0])