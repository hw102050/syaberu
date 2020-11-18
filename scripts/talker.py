#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import rospy
# from sensor_msgs.msg import Image
from std_msgs.msg import String
from std_srvs.srv import SetBool, SetBoolResponse


class Talker(object):
    def __init__(self):
        self.shutup_flg = False
        self.parrot_has_good_memory = "Hell world!!!!"    # store string for talker
    
    def mute(self, is_mute):
        """    shut f*** up    """
        self.shutup_flg = is_mute
        rospy.loginfo(">>Setting mute: {}".format(is_mute))

    def let_parrot_speak(self, command):
        """    parrot can record your command    """
        self.parrot_has_good_memory = command
        rospy.loginfo(">>Calling parrot say: {}".format(command))


class ClbkFuncs(object):
    def __init__(self, talker_obj):
        self.__talker_obj = talker_obj

    def set_mute(self, setting):
        self.__talker_obj.mute(setting.data)

    def call_parrot(self, command):
        self.__talker_obj.let_parrot_speak(command.data)


def ros_node():
    # initial node
    rospy.init_node('talker', anonymous=True)

    talker = Talker()
    clbk_obj = ClbkFuncs(talker)

    pub_talker = rospy.Publisher("talking", String, queue_size=10)
    srv_mute = rospy.Service('mute', SetBool, clbk_obj.set_mute)
    sub_parrot = rospy.Subscriber('parrot', String, clbk_obj.call_parrot)

    # keeping speak
    durationT = rospy.Duration.from_sec(3)
    while not rospy.is_shutdown():
        talk_sentence = String()
        talk_sentence.data = talker.parrot_has_good_memory
        pub_talker.publish(talk_sentence)
        rospy.loginfo("Talker say: {}".format(talker.parrot_has_good_memory))
        rospy.sleep(durationT)


if __name__ == "__main__":
    try:
        ros_node()
        rospy.spin()
    except rospy.ROSInterruptException as e:
        pass
