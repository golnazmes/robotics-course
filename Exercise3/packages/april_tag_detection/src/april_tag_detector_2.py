#!/usr/bin/env python3

import cv2
import numpy as np
import rospy
from duckietown.dtros import DTROS, NodeType
from sensor_msgs.msg import CompressedImage
from duckietown_msgs.srv import ChangePattern
from std_msgs.msg import String
import apriltag

import tf
from geometry_msgs.msg import Quaternion, Vector3, TransformStamped, Transform
from tf2_ros import TransformBroadcaster


<<<<<<< HEAD:Lab2/april_tag_and_pid/packages/april_tag_detection/src/april_tag_detector.py
 #references I used:
#https://blog.jethro.dev/posts/camera_calibration_apriltag/
#https://github.com/duckietown/dt-core/blob/daffy/packages/apriltag/src/apriltag_detector_node.py
=======
# references I used:
# https://blog.jethro.dev/posts/camera_calibration_apriltag/
# https://github.com/duckietown/dt-core/blob/daffy/packages/apriltag/src/apriltag_detector_node.py
>>>>>>> 63f296b6ae0889edd1b6c9ff41bfdf9b2f248159:Lab3/april_tag_and_pid/packages/april_tag_detection/src/april_tag_detector_2.py
def _matrix_to_quaternion(r):
    T = np.array(((0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 1)), dtype=np.float64)
    T[0:3, 0:3] = r
    return tf.transformations.quaternion_from_matrix(T)

<<<<<<< HEAD:Lab2/april_tag_and_pid/packages/april_tag_detection/src/april_tag_detector.py

=======
>>>>>>> 63f296b6ae0889edd1b6c9ff41bfdf9b2f248159:Lab3/april_tag_and_pid/packages/april_tag_detection/src/april_tag_detector_2.py

TINTERSECTION = [133, 153, 62, 58]
STOP = [169, 162]
UOATAG = [94, 93, 200, 201]
NODETECTION = -1


class ImageDimensionNode(DTROS):

    def __init__(self, node_name):
        # initialize the DTROS parent class
        super(ImageDimensionNode, self).__init__(node_name=node_name, node_type=NodeType.GENERIC)
        # construct publisher
        self.time = 0
        self.sub_image = rospy.Subscriber('/csc22938/camera_node/image/compressed', CompressedImage, self.callback)
        self.image_pub = rospy.Publisher("/csc22938/camera_node/april_tags/compressed",
                                         CompressedImage)
        self.detector = apriltag.Detector()
        self.braodcaster = TransformBroadcaster()
        rospy.wait_for_service("/csc22938/led_emitter_node/set_pattern")
        self.changePattern = rospy.ServiceProxy("/csc22938/led_emitter_node/set_pattern", ChangePattern)

    def callback(self, data):
        self.time = (self.time + 1) % 1000
        if (self.time % 10 == 0):
            np_arr = np.frombuffer(data.data, np.uint8)
            img = cv2.imdecode(np_arr, 1)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            result = self.detector.detect(img)
            img = cv2.putText(img, "Apriltag", (20, 20), cv2.FONT_HERSHEY_SIMPLEX,
                              1, 255, 2, cv2.LINE_AA)
            max_area = -1000
            max_area_id = NODETECTION
            for r in result:
<<<<<<< HEAD:Lab2/april_tag_and_pid/packages/april_tag_detection/src/april_tag_detector.py
                
    
=======

>>>>>>> 63f296b6ae0889edd1b6c9ff41bfdf9b2f248159:Lab3/april_tag_and_pid/packages/april_tag_detection/src/april_tag_detector_2.py
                c1 = [int(x - 10) for x in r.corners[0]]
                c2 = [int(x + 10) for x in r.corners[2]]
                area = abs(c1[0] - c2[0]) * abs(c1[1] - c2[1])
                if (area > max_area):
                    max_area = area
                    max_area_id = int(r.tag_id)
                cv2.rectangle(img, tuple(c1), tuple(c2), 255, 6)
                center = tuple([int(x) for x in r.center])
                img = cv2.putText(img, str(r.tag_id), center, cv2.FONT_HERSHEY_SIMPLEX,
                                  1, 255, 2, cv2.LINE_AA)
                
                 # #####################broadcast transform from camera to apriltag###############################
                t = TransformStamped()

                t.header.stamp = rospy.Time.now()
                t.header.frame_id = "camera_optical_frame"
                t.child_frame_id = "apriltag_" + str(r.tag_id)

                q = _matrix_to_quaternion(r.pose_R) 
                p = r.pose_t.T[0]
                t.transform = Transform(
                    translation=Vector3(p[0], p[1], p[2]), rotation=Quaternion(x=q[0], y=q[1], z=q[2], w=q[3]))

<<<<<<< HEAD:Lab2/april_tag_and_pid/packages/april_tag_detection/src/april_tag_detector.py
                self.broadcaster.sendTransform(t)
                ###################################################################################################
=======
                # #####################broadcast transform from camera to apriltag###############################
                t = TransformStamped()

                t.header.stamp = rospy.Time.now()
                t.header.frame_id = "camera_optical_frame"
                t.child_frame_id = "apriltag_" + str(r.tag_id)
>>>>>>> 63f296b6ae0889edd1b6c9ff41bfdf9b2f248159:Lab3/april_tag_and_pid/packages/april_tag_detection/src/april_tag_detector_2.py

                q = _matrix_to_quaternion(r.pose_R)
                p = r.pose_t.T[0]
                t.transform = Transform(
                    translation=Vector3(p[0], p[1], p[2]), rotation=Quaternion(x=q[0], y=q[1], z=q[2], w=q[3]))

                self.broadcaster.sendTransform(t)
                ###################################################################################################

            # detector = apriltag.Detector()
            # result = detector.detect(img)
            # img = cv2.resize(img, (320, 240))
            # edges = cv2.Canny(img, 100, 200)

            #### Create CompressedIamge ####
            msg = CompressedImage()
            msg.header.stamp = rospy.Time.now()
            msg.format = "jpeg"
            msg.data = np.array(cv2.imencode('.jpg', img)[1]).tobytes()
            self.image_pub.publish(msg)
            msg = String()

            if (max_area_id in STOP):
                msg.data = "RED"
                self.changePattern(msg)
            elif (max_area_id in UOATAG):
                msg.data = "GREEN"
                self.changePattern(msg)
            elif (max_area_id in TINTERSECTION):
                msg.data = "BLUE"
                self.changePattern(msg)
            elif (max_area_id == NODETECTION):
                if (self.time % 100 == 0):
                    msg.data = "WHITE"
                    self.changePattern(msg)


if __name__ == '__main__':
    # create the node
    node = ImageDimensionNode(node_name='april_tag_node')
    # keep spinning
    rospy.spin()
