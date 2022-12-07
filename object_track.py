
'''
Used to track a specific item
'''

# import the necessary packages
import argparse
#import imutils
import time
import cv2


def track_object():
	ap = argparse.ArgumentParser()
	ap.add_argument("-t", "--tracker", type=str, default="kcf",
		help="OpenCV object tracker type")
	args = vars(ap.parse_args())

	# initialize a dictionary that maps strings to their corresponding
	# OpenCV object tracker implementations
	OPENCV_OBJECT_TRACKERS = {
    	"csrt": cv2.TrackerCSRT_create,
    	"kcf": cv2.TrackerKCF_create,
    	"mil": cv2.TrackerMIL_create,
	}
	# grab the appropriate object tracker using our dictionary of
	# OpenCV object tracker objects

	tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()

	# initialize the bounding box coordinates of the object we are going
	# to track
	initBB = None

	vs = cv2.VideoCapture(0)
	# store previous midpoint of BB
	prevBBX = 0
	prevBBY = 0
	direction = None

	while True:
		# grab the current frame, then handle if we are using a
		# VideoStream or VideoCapture object
		frame = vs.read()
		frame = frame[1]
		# check to see if we have reached the end of the stream
		if frame is None:
			break
		# resize the frame (so we can process it faster) and grab the
		# frame dimensions
		(H, W) = frame.shape[:2]
		BtoT= cv2.line(frame, (W,0), (0,H), (0,0,0), 5)
		TtoB = cv2.line(frame, (0, 0), (W, H), (0, 0, 0), 5)
		# calculate linear function to split frame into 4 quadrants
		m1 = H/W
		m2 = H/W
		cX = W/2
		cY = H/2
		r = 75
		b1 = H
		b2 = 0
		# draw static circle, so that when a point is detected outside
		# we can determine direction it has moved in
		cv2.circle(frame, (int(cX), int(cY)), r, (255, 0, 0), 3)
		# check to see if we are currently tracking an object
		if initBB is not None:
			# grab the new bounding box coordinates of the object
			(success, box) = tracker.update(frame)
			# check to see if the tracking was a success
			if success:
				(x, y, w, h) = [int(v) for v in box]
				cv2.rectangle(frame, (x, y), (x + w, y + h),
					(0, 255, 0), 2)
			#decide if point breaches circle and if sowhich quadrant point belongs in 
			cv2.circle(frame, (int(x), int(y)), 5, (255, 0, 0), 3)
			cv2.circle(frame, (int(w+x), int(h+y)), 5, (255, 0, 0), 3)
			cv2.circle(frame, (int((w+2*x)/2), int((h+2*y)/2)), 5, (255, 0, 0), 3)


			midBBX = (w+2*x)/2
			midBBY = (h+2*y)/2
			y1 = -m1*midBBX + b1
			y2 = m2*midBBX + b2
			print("PrevBBX", (prevBBX - cX)**2 + (prevBBY - cY)**2, r**2)
			if (((midBBX - cX)**2 + (midBBY - cY)**2) > r**2) and (((prevBBX - cX)**2 + (prevBBY - cY)**2) <= r**2):
				if y1 >= midBBY and y2 >= midBBY:
					direction = "UP"
				elif y1 >= midBBY and y2 < midBBY:
					direction = "RIGHT"
				elif y1 < midBBY and y2 >= midBBY:
					direction = "LEFT"
				elif y1 < midBBY and y2 < midBBY:
					direction = "DOWN"
				print(y1, y2,midBBY, direction)
				with open("direction.txt", 'w') as txt:
						txt.write(direction)

			prevBBX = midBBX
			prevBBY = midBBY
			# initialize the set of information we'll be displaying on
			# the frame
			info = [
				("Tracker", args["tracker"]),
				("Success", "Yes" if success else "No"),
				("X", str(x) if success else ""),
				("Y", str(y) if success else ""),
				("Direction", str(direction) if success else "")
			]
			# loop over the info tuples and draw them on our frame
			for (i, (k, v)) in enumerate(info):
				text = "{}: {}".format(k, v)
				cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
			# show the output frame

		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF
		# if the 's' key is selected, we are going to "select" a bounding
		# box to track
		if key == ord("s"):
			# select the bounding box of the object we want to track (make
			# sure you press ENTER or SPACE after selecting the ROI)
			initBB = cv2.selectROI("Frame", frame, fromCenter=False,
				showCrosshair=True)
			# start OpenCV object tracker using the supplied bounding box
			# coordinates

			tracker.init(frame, initBB)
		elif key == ord('q'):
			break

	vs.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':
    track_object()