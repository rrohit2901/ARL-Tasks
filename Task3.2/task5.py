import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys

def distance(x,y):
    return (((x[0][0]-y[0])**2 + (x[1][0]-y[1])**2 + (x[2][0]-y[2])**2)**0.5)

class plane:
    def __init__(self):
        self.x = np.array([[0.0],
                        [0.0],
                        [0.0],
                        [0.05],
                        [0.05],
                        [0.02],
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

planes = []

# #   Calculating variance of data
# sum_x = 0.0
# sum_y = 0.0
# sum_z = 0.0
# sum2_x = 0.0
# sum2_y = 0.0
# sum2_z = 0.0
# count = 0 
# for i in range(19999):
#     for j in range(0,24,3):
#         if data.iloc[i][j] == 0:
#             break
#         sum_x += data.iloc[i][j]
#         sum_y += data.iloc[i][j+1]
#         sum_z += data.iloc[i][j+2]
#         sum2_x += data.iloc[i][j] ** 2
#         sum2_y += data.iloc[i][j+1] ** 2
#         sum2_z += data.iloc[i][j+2] ** 2
#         count += 1
# mean_x = sum_x/count
# mean_y = sum_y/count
# mean_z = sum_z/count
# mean2_x = sum2_x/count
# mean2_y = sum2_y/count
# mean2_z = sum2_z/count
# var_x = -mean_x**2 + mean2_x
# var_y = -mean_y**2 + mean2_y
# var_z = -mean_z**2 + mean2_z

#   Constant props
thre = 0.015
dt = 1
R = np.array([[0.00083303,0,0],
                [0,0.00392254,0],
                [0,0,0.00017298]])
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
for i in range(6000):
    print("Current is {} and i is {}".format(len(planes),i))
    for p in planes:
        if p.in_bounds:
            coordi = []
            for k in range(3):
                coordi.append((p.x)[k][0])
            p.predict(F)
            coordi = []
            for k in range(3):
                coordi.append((p.x)[k][0])
            (p.path).append(coordi)
            for k in range(3):
                if coordi[k] > 1 or coordi[k] < -1:
                    p.in_bounds = 0

    
    if data.iloc[i][0] == 0:
        continue
    
    for j in range(0,24,3):
        if data.iloc[i][j] == 0:
            break
        measure = np.array([[data.iloc[i][j]],
                            [data.iloc[i][j+1]],
                            [data.iloc[i][j+2]]])
        flag = 0
        for p in planes:
            coordi = []
            for k in range(3):
                coordi.append((p.x)[k][0])
            if distance(measure, coordi) < thre:
                flag = 1
                p.measurement(measure,H,R,I)
                p.visited += 1
                break
        if flag == 0:
            temp = plane()
            temp.measurement(measure,H,R,I)
            planes.append(temp)
true_planes = []  
for p in planes:
    if p.visited == 0:
        continue
    true_planes.append(p)

print("Number of true planes detected are :- {}".format(len(true_planes)))

for p in true_planes:
    xs = []
    ys = []
    zs = []
    for i in range(len(p.path)):
        xs.append(p.path[i][0])
        ys.append(p.path[i][1])
        zs.append(p.path[i][2])
    fig = plt.figure
    ax = plt.axes(projection="3d")
    ax.scatter(xs = xs, ys = ys, zs = zs, zdir='z', s=20, c=None, depthshade=True)
    plt.show()
