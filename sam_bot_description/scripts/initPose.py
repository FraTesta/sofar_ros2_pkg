#!/usr/bin/env python3

# ROS Client Library for Python
import rclpy
 
# Handles the creation of nodes
from rclpy.node import Node
 
# Enables usage of the String message type
from std_msgs.msg import String
from geometry_msgs.msg import PoseWithCovarianceStamped

from time import sleep

class PosePublisher(Node):
  """
  Create a PosePublisher class, which is a subclass of the Node class.
  """
  def __init__(self):
    """
    Class constructor to set up the node
    """
    # Initiate the Node class's constructor and give it a name
    super().__init__('pose_publisher')
     
    # Create the publisher. This publisher will publish a String message
    # to the addison topic. The queue size is 10 messages.
    self.publisher_pose = self.create_publisher(PoseWithCovarianceStamped, "/initialpose", 1)
    
    self.pose_publisher()

  def pose_publisher(self):

    msg = PoseWithCovarianceStamped()
    msg.header.frame_id = "/map"
    msg.pose.pose.position.x = 0.0
    msg.pose.pose.position.y = 0.0
    msg.pose.pose.position.z = 0.0
    msg.pose.pose.orientation.x = 0.0
    msg.pose.pose.orientation.y = 0.0
    msg.pose.pose.orientation.z = 0.0
    msg.pose.pose.orientation.w = 1.0
    msg.pose.covariance=[0.25, 0.0, 0.0, 0.0, 0.0, 0.0,
                        0.0, 0.25, 0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 
                        0.0, 0.0, 0.0, 0.0, 0.0, 0.06853891945200942]

    while self.publisher_pose.get_subscription_count() < 1:
      self.get_logger().info('waiting..')
      sleep(1)

    self.publisher_pose.publish(msg)
    self.get_logger().info('AO')
  
  #def goal_publisher()

def main(args=None):

  rclpy.init(args=args)
  node = PosePublisher()
  rclpy.spin(node)
  rclpy.shutdown()
  
if __name__ == "__main__":
    main()
