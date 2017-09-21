import cv2
import numpy as np

from styx_msgs.msg import TrafficLight

class TLClassifier(object):
    def __init__(self):
        #TODO load classifier
        pass

    def get_classification(self, image):
        """Determines the color of the traffic light in the image

        Args:
            image (cv::Mat): image containing the traffic light

        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """
        #TODO implement light color prediction
        #return image
        return TrafficLight.UNKNOWN

    def get_test_classification(self, image):
        """Determines the color of the traffic light in the image

        Args:
            image (cv::Mat): image containing the traffic light

        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """
        #TODO implement light color prediction
        img = np.asarray(image) # convert cv::Mat image to numpy array
        #print img.shape
        #print img.size
        #print img.dtype

        # http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_colorspaces/py_colorspaces.html
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        low_red = np.array([175, 30, 8])
        upp_red = np.array([179, 255, 255])

        low_yel = np.array([20, 160, 0])
        upp_yel = np.array([30, 255, 255])

        low_grn = np.array([50, 179, 102])
        upp_grn = np.array([75, 255, 255])

        colors = ["red", "yellow", "green"]

        masks = np.array([
            [low_red, upp_red],
            [low_yel, upp_yel],
            [low_grn, upp_grn]
        ])

        ratios = np.array([0.0, 0.0, 0.0])

        for i, cmask in enumerate(masks):
            mask = cv2.inRange(hsv, cmask[0], cmask[1])
            res = cv2.bitwise_and(img, img, mask=mask)

            # num of pixels in mask / image size
            #
            # image size is divided by 3.0 twice:
            #
            #   1. First, because size is # pixels * # planes,
            #      we just want the number on a single plane
            #
            #   2. Second, because we want to know how much
            #      area is taken up in the 1/3 of the space a
            #      single "light" occupies
            #
            ratio = (cv2.countNonZero(mask) / ((img.size / 3.0) / 3.0))

            color = colors[i]

            #print color, 'percentage:', np.round(ratio * 100, 1), '%'

            ratios[i] = np.round(ratio * 100, 1)

            #cv2.imwrite('./images/' + color + '-testing.jpg', res)

        top = 0.0
        tlv = TrafficLight.UNKNOWN

        if ratios[0] > top:
            top = ratios[0]
            tlv = TrafficLight.RED

        if ratios[1] > top:
            top = ratios[1]
            tlv = TrafficLight.YELLOW

        if ratios[2] > top:
            top = ratios[2]
            tlv = TrafficLight.GREEN

        #print tlv, top

        return tlv
