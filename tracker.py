

# import the necessary packages
import time
import threading
import cv2

class Tracker:
    def track_loop(self):
        OPENCV_OBJECT_TRACKERS = {
            "csrt": cv2.TrackerCSRT_create,
            "kcf": cv2.TrackerKCF_create,
            "mil": cv2.TrackerMIL_create,
        }
        # grab the appropriate object tracker using our dictionary of
        # OpenCV object tracker objects

        tracker = OPENCV_OBJECT_TRACKERS["csrt"]()

        # initialize the bounding box coordinates of the object we are going
        # to track
        initBB = None

        #capture screen monitor
        vs = cv2.VideoCapture(0)

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

            # check to see if we are currently tracking an object
            if initBB is not None:
                # grab the new bounding box coordinates of the object
                (success, box) = tracker.update(frame)
                # check to see if the tracking was a success
                if success:
                    (x, y, w, h) = [int(v) for v in box]
                    cv2.rectangle(frame, (x, y), (x + w, y + h),
                        (0, 255, 0), 2)

                #get the x and y values
                self.x = x 
                self.y = y  

                # initialize the set of information we'll be displaying on
                # the frame
                info = [
                    ("Success", "Yes" if success else "No"),
                    ("X", str(x) if success else ""),
                    ("Y", str(y) if success else ""),
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

    def get_values(self):
        return (self.x, self.y)

    def __init__(self):
        self.x = 0
        self.y = 0
        x = threading.Thread(target=self.track_loop)
        x.start()
