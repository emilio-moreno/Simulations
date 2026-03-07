from mpl_toolkits.mplot3d import Axes3D 
import matplotlib.pyplot as plt 
import numpy as np

a = 1
e0 = np.array([0, 0, 0])
e1 = a * np.array([1, 0, 0])
e2 = a * np.array([0, 1, 0])
e3 = a * np.array([0, 0, 1])
a1 = (a/2) * np.array([0, 1, 1])
a2 = (a/2) * np.array([1, 0, 1])
a3 = (a/2) * np.array([1, 1, 0])
b1 = np.array([0, 0, 0])
b2 = (a/4) * np.array([1, 1, 1])

b1_points = []
b2_points = []
for n1 in range(0, 2):
	for n2 in range(0, 2):
		for n3 in range(0, 2):
			b1_points.append(n1*e1 + n2*e2 + n3*e3)

for n in range(0, 2):
	for e, a in zip([e1, e2, e3], [a1, a2, a3]):
		b1_points.append(a + n*e)

for a in [e0, a1, a2, a3]:
	b2_points.append(a + b2)
b1_points = np.array(b1_points)
b2_points = np.array(b2_points)

neighbour_directions = []
neighbour_connections = []
for a in [e0, a1, a2, a3]:
	neighbour_directions.append(a - b2)

for b2_point in b2_points:
	for neighbour_direction in neighbour_directions:
		neighbour_connections.append((*b2_point, *neighbour_direction))
neighbour_connections = np.array(neighbour_connections)

fig = plt.figure() 
ax = fig.add_subplot(111, projection='3d')
ax.scatter(b1_points[:,0], b1_points[:,1], b1_points[:,2],
		   s=200, color='b', alpha=1)
ax.scatter(b2_points[:,0], b2_points[:,1], b2_points[:,2],
		   s=100, color='r', alpha=1)

ax.quiver(neighbour_connections[:, 0], neighbour_connections[:, 1], neighbour_connections[:, 2],
		  neighbour_connections[:, 3], neighbour_connections[:, 4], neighbour_connections[:, 5],
		  color='k', arrow_length_ratio=0, lw=3)

plt.savefig('diamond_cell.png')