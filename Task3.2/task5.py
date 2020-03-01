import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# def distance():

matplotlib.use('TkAgg')
count = 0
thre_distance = 0.01

data = pd.read_excel(r'radar_dump.xlsx')
data = data.fillna(value = 0)
print(data)
xs = []
ys = []
zs = []
temp = []
obj_path = []

for i in range(19999):
    for j in range(0,24,3):
        if(data.iloc[i][j] == 0):
            break
        else:
            temp1 = []
            temp1.append(data.iloc[i][j])
            temp1.append(data.iloc[i][j+1])
            temp1.append(data.iloc[i][j+2])
            temp1.append(i)
            temp1.append(1)
    temp.append(temp1)

for i in range(1, temp.size()):
    time_gap = temp[i][3] - temp[i-1][3]
    x, y, z = predict()



fig = plt.figure
ax = plt.axes(projection="3d")
ax.scatter(xs = xs, ys = ys, zs = zs, zdir='z', s=20, c=None, depthshade=True)
plt.show()
