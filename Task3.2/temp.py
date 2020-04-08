import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys

class plane:
    def __init__(self):
        self.x = np.array([[0.0],
                        [0.0],
                        [0.0],
                        [0.0],
                        [0.0],
                        [0.0],
                        [0.0],
                        [0.0],
                        [0.0]])
        self.P = np.array([[1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
                        [0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0],
                        [0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0],
                        [0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0],
                        [0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0],
                        [0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0],
                        [0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0],
                        [0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0],
                        [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0]])
        self.path = []
        self.visited = 0
        self.in_bounds = 1
    def predict(self, F):
        self.x = F.dot(self.x)
        self.P = F.dot((self.P).dot(F.transpose()))
    def measurement(self,z,H,R,I):
        S = R + H.dot((self.P).dot(H.transpose()))
        K = (self.P).dot((H.transpose()).dot(np.linalg.inv(S)))
        y = z - H.dot((self.x))
        self.x = self.x + K.dot(y)
        self.P = (I - K.dot(H)).dot(self.P)


matplotlib.use('TkAgg')

data = pd.read_excel(r'radar_dump.xlsx')
data = data.fillna(value = 0)
print(data)

xs = []
ys = []
zs = []

xs.append(data.iloc[71,0])
xs.append(data.iloc[72,0])
xs.append(data.iloc[74,0])
xs.append(data.iloc[75,0])
xs.append(data.iloc[77,0])

ys.append(data.iloc[71,1])
ys.append(data.iloc[72,1])
ys.append(data.iloc[74,1])
ys.append(data.iloc[75,1])
ys.append(data.iloc[77,1])


zs.append(data.iloc[71,2])
zs.append(data.iloc[72,2])
zs.append(data.iloc[74,2])
zs.append(data.iloc[75,2])
zs.append(data.iloc[77,2])

sum_x = 0.0
sum_y = 0.0
sum_z = 0.0
sum2_x = 0.0
sum2_y = 0.0
sum2_z = 0.0
count = 0 
for i in range(len(xs)):
        sum_x += xs[i]
        sum_y += ys[i]
        sum_z += zs[i]
        sum2_x += xs[i] ** 2
        sum2_y += ys[i] ** 2
        sum2_z += zs[i] ** 2
        count += 1
mean_x = sum_x/count
mean_y = sum_y/count
mean_z = sum_z/count
mean2_x = sum2_x/count
mean2_y = sum2_y/count
mean2_z = sum2_z/count
var_x = -mean_x**2 + mean2_x
var_y = -mean_y**2 + mean2_y
var_z = -mean_z**2 + mean2_z

thre = 0.01
dt = 1
R = np.array([[var_x,0,0],
                [0,var_y,0],
                [0,0,var_z]])
F = np.array([[1,0,0,dt,0,0,(dt**2)/2.0,0,0],
                [0,1,0,0,dt,0,0,(dt**2)/2.0,0],
                [0,0,1,0,0,dt,0,0,(dt**2)/2.0],
                [0,0,0,1,0,0,dt,0,0],
                [0,0,0,0,1,0,0,dt,0],
                [0,0,0,0,0,1,0,0,dt],
                [0,0,0,0,0,0,1,0,0],
                [0,0,0,0,0,0,0,1,0],
                [0,0,0,0,0,0,0,0,1]])
H = np.array([[1,0,0,0,0,0,0,0,0],
                [0,1,0,0,0,0,0,0,0],
                [0,0,1,0,0,0,0,0,0]])
I = np.array([[1,0,0,0,0,0,0,0,0],
                [0,1,0,0,0,0,0,0,0],
                [0,0,1,0,0,0,0,0,0],
                [0,0,0,1,0,0,0,0,0],
                [0,0,0,0,1,0,0,0,0],
                [0,0,0,0,0,1,0,0,0],
                [0,0,0,0,0,0,1,0,0],
                [0,0,0,0,0,0,0,1,0],
                [0,0,0,0,0,0,0,0,1]])

print(R)
p = plane()
for i in range(len(xs)):
    measure = np.array([[xs[i]],
                        [ys[i]],
                        [zs[i]]])
    p.measurement(measure,H,R,I)
    p.predict(F)

print(p.P)
print(p.x)

fig = plt.figure
ax = plt.axes(projection="3d")
ax.scatter(xs = xs, ys = ys, zs = zs, zdir='z', s=20, c=None, depthshade=True)
plt.show()