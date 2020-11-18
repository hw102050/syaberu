#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import rospy
# from sensor_msgs.msg import Image
from std_msgs.msg import String


class Listener(object):
    def __init__(self):
        pass

    def hear(self, content):
        """    hear it say    """
        rospy.loginfo(">>It say...: {}".format(content))


class ClbkFuncs(object):
    def __init__(self, listener_obj):
        self.__listener_obj = listener_obj

    def hear_it_say(self, say):
        self.__listener_obj.hear(say.data)



def ros_node():
    # initial node
    rospy.init_node('listener', anonymous=True)

    listener = Listener()
    clbk_obj = ClbkFuncs(listener)

    sub_talker = rospy.Subscriber('talking', String, clbk_obj.hear_it_say)


if __name__ == "__main__":
    try:
        ros_node()
        rospy.spin()
    except rospy.ROSInterruptException as e:
        pass
