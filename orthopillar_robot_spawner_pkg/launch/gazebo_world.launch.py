# Copyright 2019 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
 
"""
Demo for spawn_entity.
Launches Gazebo and spawns a model
"""
# A bunch of software packages that are needed to launch ROS2
import os
import launch
import launch_ros
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.substitutions import Command, LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import ThisLaunchFileDir, LaunchConfiguration
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
from ament_index_python.packages import get_package_share_directory
import xacro
 
def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    world_file_name = 'room.world'
    spaw_dir = get_package_share_directory('orthopillar_robot_spawner_pkg')
    orto_dir = get_package_share_directory('orto_nav')
    sam_dir = get_package_share_directory('sam_bot_description')
    
    default_rviz_config_path = os.path.join(orto_dir, 'rviz/config.rviz')

    os.environ["GAZEBO_MODEL_PATH"] = os.path.join(orto_dir, 'models')
 
    world = os.path.join(orto_dir, 'worlds', world_file_name)
    launch_file_dir = os.path.join(spaw_dir, 'launch')

    urdf_file = os.path.join(sam_dir, 'src/description', 'sam_bot_description.urdf')
    
    doc = xacro.parse(open(urdf_file))
    xacro.process_doc(doc)
    robot_description = {'robot_description': doc.toxml()}


    """
    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen', 
        parameters=[robot_description]
    )
    
    
    joint_state_publisher_node = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        #condition=launch.conditions.UnlessCondition(LaunchConfiguration('gui'))
    )"""


    gazebo = ExecuteProcess(
            cmd=['gazebo', '--verbose', world, '-s', 'libgazebo_ros_init.so', 
            '-s', 'libgazebo_ros_factory.so'],
            output='screen')
 
    #GAZEBO_MODEL_PATH has to be correctly set for Gazebo to be able to find the model
    #spawn_entity = Node(package='gazebo_ros', node_executable='spawn_entity.py',
    #                    arguments=['-entity', 'demo', 'x', 'y', 'z'],
    #                    output='screen')
    spawn_entity = Node(package='orthopillar_robot_spawner_pkg', executable='spawn_demo',
                        arguments=['orthopillar', 'demo', '0.0', '0.0', '0.0'],
                        output='screen')

    #robot_state_publisher = Node( package='robot_state_publisher', 
    #                            executable='robot_state_publisher',
     #                           name='robot_state_publisher',
      #                          output='screen',
       #                         parameters=[{'use_sim_time': use_sim_time, 'robot_description': robot_description}],
        #                        arguments=[urdf])

    #state_publisher = Node( package='orthopillar_robot_spawner_pkg',
     #                       executable='state_publisher',
      #                      name='state_publisher',
       #                     output='screen')
 
    return launch.LaunchDescription([

        gazebo,
        spawn_entity,
        #robot_state_publisher_node,
        #joint_state_publisher_node,
        #joint_state_publisher_gui_node,
        
        #state_publisher
        #rviz_node
    ])
