import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as FA
from matplotlib.animation import FFMpegWriter
import numpy as np
import mpl_toolkits.mplot3d.axes3d as axes3d
from scipy.special import sph_harm
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# MpegWriter and format
mpl.rcParams['animation.ffmpeg_path'] = r'C:\\Program Files\\ffmpeg-7.1-full_build\\bin\\ffmpeg.exe'
rc_update = {'font.size': 10, 'font.family': 'serif',
			 'font.serif': ['Times New Roman', 'FreeSerif'], 'mathtext.fontset': 'cm'}
plt.rcParams.update(rc_update)
plt.style.use('dark_background')

def animate(fig, updater, total_frames: int, fps: float, filename: str):
	animation = FA(fig, updater, frames=list(range(total_frames)), repeat=False)
	writer = FFMpegWriter(fps=fps)
	animation.save(filename, writer=writer)

def animation_progress(total_frames, frame):
	'''Prints progress of animation.'''
	# Progress bar str
	frame += 1
	done = frame / total_frames
	remaining = (total_frames - frame) / total_frames
	done = int(np.ceil(20 * done)) * '#'
	remaining = int(np.ceil(20 * remaining)) * '_'
	progress_bar = "[" + done + remaining + "]"

	# Print
	print(f"Animated: {frame} / {total_frames} frames")
	print(progress_bar + '\n')

	if frame == total_frames:
		print("Animation done!\n")


def polar(r, a):
	'''Polar coordinates to Cartesian (r: r, a: theta, b: phi).'''
	return r * np.cos(a), r * np.sin(a)

def spherical(r, a, b):
	'''Spherical coordinates to Cartesian (r: r, a: theta, b: phi).'''
	return r * np.sin(a) * np.cos(b), r * np.sin(a) * np.sin(b), r * np.cos(a)

def main():

	fig, ax = plt.subplots(subplot_kw = {'projection': '3d'})
	empty_2d = np.array([[], []])
	a = np.linspace(0, np.pi, 50)
	b = np.linspace(0, 2 * np.pi, 50)
	A, B = np.meshgrid(a, b)
	C = 2
	C2 = 1
	C3 = 0.75
	#R = lambda a, b, t: C  + np.cos(a - t)
	#R = lambda a, b, t: C + C2 * (np.cos(a) * np.sin(a))**2 + C3 * np.cos(a) * np.sin(a) * np.cos(b - t)
	#R = lambda a, b, t: np.abs(sph_harm(1, 2, A, B - t))
	#R = lambda a, b, t: C * np.cos(a)**5 + C2 * (np.cos(a) * np.sin(a))**2 + C3 * np.cos(a) * np.sin(a) * np.cos(b - t) + np.cos(a - 2 * t)

	#ax.plot_surface(*spherical(R(A, 0), A, B), rstride=1, cstride=1, cmap=plt.get_cmap('jet'),
    #linewidth=0, antialiased=False, alpha=0.5)
	#plt.show()

	
	def updater(frame):
		t = accel * frame / fps
		ax.clear()
		ax.set(xlim=lims, ylim=lims, zlim=lims)
		ax.plot_surface(*spherical(R(A, B, t), A, B), rstride=1, cstride=1, cmap=plt.get_cmap('jet'),
    	linewidth=0, antialiased=False, alpha=0.5)
		animation_progress(total_frames, frame)
		return

	
	filename = 'weird_thing.gif'
	total_frames = 120
	accel = 3
	fps = 30
	lims = (-3.5, 3.5)
	animate(fig, updater, total_frames, fps, filename)


# %% Cube rotation
def rotation_matrix(angle, a):
		M = np.array([[np.cos(angle), -np.sin(angle), 0],
		 			   [np.sin(angle), np.cos(angle), 0],
		 			   [0, 0, 1]])

		b = np.array([-a[1], a[0], a[2]])
		c = np.cross(a, b)
		A = np.array([b, c, a])

		return np.linalg.inv(A) @ M @ A

def rotate(M, X):
		new_X = np.zeros(X.shape)

		for i, (x, y, z) in enumerate(zip(X[0, :], X[1, :], X[2, :])):
			x, y, z = M @ np.array([x, y, z])
			new_X[:, i] = [x, y, z]
		return new_X

# Face IDs
def draw_cube(X):
	vertices = [[0,1,2,3],[1,5,6,2],[3,2,6,7],[4,0,3,7],[5,4,7,6],[4,5,1,0]]

	tupleList = list(zip(X[0, :], X[1, :], X[2, :]))

	poly3d = [[tupleList[vertices[ix][iy]] for iy in range(len(vertices[0]))] for ix in range(len(vertices))]
	ax.scatter(X[0, :], X[1, :], X[2, :])
	ax.add_collection3d(Poly3DCollection(poly3d, facecolors='r', linewidths=5, alpha=0.1))

def main2():
	# Original cube
	global X
	X = np.array([
			[-1, 1, 1, -1, -1, 1, 1, -1],
			[-1, -1, 1, 1, -1, -1, 1, 1],
			[-1, -1, -1, -1, 1, 1, 1, 1]
		])
	X = X / 3
	zero = np.array([0, 0, 0])

	global ax
	fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
	angle = np.pi / 4

	def updater(frame):
		ax.clear()
		ax.set(xlim=lims, ylim=lims, zlim=lims)
		ax.set(xlabel='x', ylabel='y', zlabel='z')

		# Time
		t = accel * frame / fps
		angle = t + 1
		a = np.array([-t, 0, 0])
		a = a / np.linalg.norm(a)
		M = rotation_matrix(angle, a)
		rot_X = rotate(M, X)
		ax.plot(zero, angle * a, color='k', marker='^')
		draw_cube(rot_X)
		
		animation_progress(total_frames, frame)
		return

	
	filename = 'cube.mp4'
	total_frames = 150
	accel = 1
	fps = 30
	lims = (-0.5, 0.5)
	animate(fig, updater, total_frames, fps, filename)



if __name__ == '__main__':
	main2()
