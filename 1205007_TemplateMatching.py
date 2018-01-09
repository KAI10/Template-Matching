# TemplateMatching.py

# Created by: Ashik <ashik@KAI10>
# Created on: Thu, 20 Apr 2017

import cv2
import math

########## read from input video file ##############

print("Reading from input video ...")

vidcap = cv2.VideoCapture('input.MOV')
success, img = vidcap.read()
count = 0

success,img = vidcap.read()

while success:
	# save frame as JPEG file
    cv2.imwrite("frame%d.jpg" % count, img)
    count += 1
    
    success, img = vidcap.read()

print("# of frames: ", count)

######### track reference image ####################

ref = cv2.imread('reference.jpg', 0)
cur_frame = cv2.imread('frame0.jpg', 0)

(ref_rows, ref_cols) = ref.shape
(frame_rows, frame_cols) = cur_frame.shape

print(frame_rows, frame_cols, ref_rows, ref_cols)

################# METHODS ######################################

def drawBorder(frame, fm , fn):
	frame[fm:fm+1, fn:fn+ref_cols] = 0
	frame[fm+ref_rows-1:fm+ref_rows, fn:fn+ref_cols] = 0

	frame[fm:fm+ref_rows, fn:fn+1] = 0
	frame[fm:fm+ref_rows, fn+ref_cols-1:fn+ref_cols] = 0


def mismatch(frame, ref, m, n):
	(M, N) = ref.shape

	ret = 0
	for i in range(m, m+M):
		for j in range(n, n+N):
			val = int(frame.item(i, j)) - int(ref.item(i-m, j-n)) # taking only value of blue
			ret += val*val

	return ret


################# SEARCH METHODS ###############################

def exhaustive_search(frame, ref, rmin, rmax, cmin, cmax):
	minSum = 100000000000
	for m in range(rmin, rmax+1):
		for n in range(cmin, cmax+1):
			Sum = mismatch(frame, ref, m, n)
			if(Sum < minSum):
				minSum = Sum
				(fm, fn) = (m, n)

	return fm, fn


def TDLS(frame, ref, rmid, cmid, midCost, d):

	minCost = midCost
	(fm, fn) = (rmid, cmid)
	for r in range(rmid-d, rmid+d+1, d):
		for c in range(cmid-d,  cmid+d+1, d):
			if r == rmid and c == cmid: continue
			cost = mismatch(frame, ref, r, c)
			if cost < minCost:
				minCost = cost
				(fm, fn) = (r, c)

	if d == 1: return fm, fn
	return TDLS(frame, ref, fm, fn, minCost, int(d/2))


def hieararchial_search(frame, ref, rmid, cmid, p, cur_level, limit):

	if cur_level == 0:
		subFrame = frame
		subRef = ref
	
	else:
		# create sub-sampled images
		subFrame = cv2.pyrDown(frame)
		subRef = cv2.pyrDown(ref)

	if cur_level < limit:

		fm, fn = hieararchial_search(subFrame, subRef, int(rmid/2), int(cmid/2), int(p/2), cur_level+1, limit)

		fr_mid = rmid + 2*fm
		fc_mid = cmid + 2*fn

		minCost = 100000000000
		for r in range(rmid-1, fr_mid+1+1):
			for c in range(cmid-1, fc_mid+1+1):
				cost = mismatch(subFrame, subRef, r, c)
				if cost < minCost:
					minCost = cost
					(fm, fn) = (r, c)

		if cur_level > 0: return (fm-rmid, fn-cmid)
		return fm, fn

	else:
		'''
		fm, fn = exhaustive_search(subFrame, subRef, rmid-p, rmid+p, cmid-p, cmid+p, p)
		return fm-rmid, fn-cmid
		'''
		k = math.ceil(math.log(p, 2))
		d = 2**(k-1)
		midCost = mismatch(subFrame, subRef, rmid, cmid)

		fm, fn = TDLS(subFrame, subRef, int(rmid), int(cmid), midCost, int(d))
		return (fm-rmid, fn-cmid)

###############################################################


# searching in initial image
print("Searching in frame 0 ...")
fm, fn = exhaustive_search(cur_frame, ref, 0, frame_rows-ref_rows-1, 0, frame_cols-ref_cols-1)
#print("found at: ", fm, fn)

# update frame 0
#fm = 240
#fn = 141

print(cur_frame[240,141])
print(mismatch(cur_frame, ref, 240, 141))

drawBorder(cur_frame, fm, fn)
cv2.imwrite("frame0.jpg", cur_frame)

p = 7

for frame in range(1, count):
	print("processing frame: ", frame)

	name = 'frame'+str(frame)+'.jpg'
	cur_frame = cv2.imread(name, 0)

	(rmin, rmax) = (fm - p, fm + p)
	(cmin, cmax) = (fn - p, fn + p)

	rmin = max(0, rmin)
	rmax = min(frame_rows-ref_rows, rmax)

	cmin = max(0, cmin)
	cmax = min(frame_cols-ref_cols, cmax)

	############# SEARCH METHODS CALLED HERE ##########################

	# EXHAUSTIVE SEARCH
	#fm, fn = exhaustive_search(cur_frame, ref, rmin, rmax, cmin, cmax)

	
	rmid = int((rmin+rmax)/2)
	cmid = int((cmin+cmax)/2)

	# 2D LOGARITHMIC SEARCH
	'''
	k = math.ceil(math.log(p, 2))
	d = 2**(k-1)
	midCost = mismatch(cur_frame, ref, rmid, cmid)

	fm, fn = TDLS(cur_frame, ref, rmid, cmid, midCost, d)
	'''
	# HIERARCHIAL SEARCH
	fm, fn = hieararchial_search(cur_frame, ref, rmid, cmid, p, 0, 1)
	
	####################################################################

	drawBorder(cur_frame, fm, fn)
	cv2.imwrite(name, cur_frame)


#################### write to output video #############################

print("Writing to output video file ...")

img = cv2.imread('frame0.jpg')
height , width , layers =  img.shape

fourcc = cv2.VideoWriter_fourcc(*'XVID') # for video encoding
video = cv2.VideoWriter('output.MOV', fourcc, 50, (width,height)) # 50 fps
video.write(img)

for i in range(1, count):
	name = 'frame'+str(i)+'.jpg'
	img = cv2.imread(name)
	video.write(img)

cv2.destroyAllWindows()
video.release()
