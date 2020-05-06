import numpy as np
import cv2
import argparse
import os 
import math
import sympy
import warnings


def church(a, b, A, B, S, _S, USE_DIFF, h, w):
	
	a, b, A, B = np.array(a+[0.]), np.array(b+[0.]), np.array(A+[0.]), np.array(B+[0.])
	
	# in camera coordinates
	o = np.array([h/2*0.00016, w/2*0.00016, _S])
	aob = math.acos(np.dot(a-o, b-o) / (dis(o, a)*dis(o, b)))
		
	# in world coordinates
	H_init = A[0] + (a[0] - h/2*0.00016) / _S * S
	W_init = A[1] - (a[1] - w/2*0.00016) / _S * S
	O = np.array([H_init, W_init, S])
	min_diff = 1000
	#print('O init: ', O)

	# Iterative method
	if not USE_DIFF:
		eta = np.array((0.1, 0.1, 0.01))
		iters = 100
		directions = np.array([[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]], dtype = float)
		directions = directions * eta
		pre_d = np.array([0, 0, 0])
	
		for i in range(iters):
			min_diff = 100
			gradient = np.array([0, 0, 0])
			for d in directions:
				_O = O + d
				AOB = math.acos(np.dot(A - _O, B - _O) / (dis(_O, A)*dis(_O, B)))
				diff = abs(aob - AOB)
				if diff < min_diff and (d!=-pre_d).any():
					min_diff = diff
					gradient = d 
		
			O = O + eta * gradient
			#print('iter: ', i+1, '  diff: ', min_diff, '   grad: ', gradient, '  O: ', O)
			pre_d = gradient
			if min_diff <= 0.0001:

				#print('iter: ', i+1, '  diff: ', min_diff, ' O: ', O)
				return O
	
	# Differentail method
	else:

		eta = np.array((0.1, 0.1, 0.01))
		iters = 100
		x, y, z = sympy.symbols('x, y, z')
		_O = np.array([x, y, z])
		_AOB = sympy.acos(np.dot(A-_O, B-_O)/(dis(_O, A)*dis(_O, B)))
		_diff = (aob - _AOB)
		pre_diff = 100

		# Partial differential
		for i in range(iters):
			
			delta_x = sympy.diff(_diff, x).subs([(x, O[0]), (y, O[1]), (z, O[2])])
			delta_y = sympy.diff(_diff, y).subs([(x, O[0]), (y, O[1]), (z, O[2])])
			delta_z = sympy.diff(_diff, z).subs([(x, O[0]), (y, O[1]), (z, O[2])])

			gradient = np.array([delta_x, delta_y, delta_z])

			New_O = O - eta * gradient
			AOB = math.acos(np.dot(A - O, B - O) / (dis(O, A)*dis(O, B)))
			diff = abs(aob - AOB)
			if pre_diff < diff:
				#print('iter: ', i+1, ' grad: ', gradient, ' diff: ', diff, ' O: ', O)
				return O

			O = New_O
			pre_diff = diff

			#if  (i+1) % 10 == 0:
				#print('iter: ', i+1, ' grad: ', gradient, ' diff: ', diff, ' O: ', O)

			if diff < 0.1:
				#print('iter: ', i+1, '  diff: ', min_diff, ' O: ', O)
				return O

	#print('iter: ', i+1, '  diff: ', min_diff, ' O: ', O)
	return O

def dis(A, B):
	if len(A) == 3:
		return ((A[0] - B[0])**2 + (A[1] - B[1])**2 + (A[2] - B[2])**2)**(1/2) 
	else:
		return ((A[0] - B[0])**2 + (A[1] - B[1])**2)**(1/2)

def imaging(h, _h):

	iters = 0
	f = 0.473
	_S = f
	S  = _S * h / _h
	
	
	for i in range(iters):
	
		_S = 1 / ((1/f) - (1/S))
		S  = _S * h / _h
	
	return S, _S

def point_detection(img):
	
	height, width = img.shape[:2]
	A = (np.where((img[:, :, 0] == 0) & (img[:, :, 1] == 0) & (img[:, :, 2] == 255)))
	A = [float(A[0]*0.00016), float(A[1])*0.00016]
	B = (np.where((img[:, :, 0] == 0) & (img[:, :, 1] == 100) & (img[:, :, 2] == 255)))
	B = [float(B[0]*0.00016), float(B[1])*0.00016]
	C = (np.where((img[:, :, 0] == 255) & (img[:, :, 1] == 0) & (img[:, :, 2] == 0)))
	C = [float(C[0]*0.00016), float(C[1])*0.00016]

	return A, B, C


def main(args):
	
	# World coordinates
	A = [0, 0]
	B = [5.8, 27.5]

	img_list = ['AR/Short.png', 'AR/Mid.png', 'AR/Long.png', 'AR/test_data_1.png', 'AR/test_data_2.png', 'AR/test_data_3.png']
	for input_dir in img_list:
		img = cv2.imread(os.path.join(input_dir))
		cor = point_detection(img)
		Z, _Z = imaging(dis(A, B), dis(cor[0], cor[1]))
		O_cor = church(cor[0], cor[1], A, B, Z, _Z, args.differential, img.shape[0], img.shape[1])
		O_cor[0], O_cor[1] = O_cor[1], O_cor[0]
		print(input_dir.replace('.png', '').replace('AR/', ''), 'coordinates: ', O_cor)


if __name__ == '__main__':


	warnings.filterwarnings("ignore")
	parser = argparse.ArgumentParser(description='Input Parameters')
	parser.add_argument('input_dir', type = str,
						help = 'Directory to the input images')
	parser.add_argument('-d', '--differential', action="store_true",
						help = 'Enable differential method')
	args = parser.parse_args()
	main(args)
