import launch
from launch import action
from ament_index_python import get_package_share_directory
from launch.substitutions import Command, LaunchConfiguration
#from launch.launch_description_sources import PythonLaunchDescriptionSource
import launch_ros
import os
## NEW
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import ExecuteProcess, IncludeLaunchDescription

def generate_launch_description():
    #world_file_name = 'room.world'

    pkg_share = launch_ros.substitutions.FindPackageShare(package='sam_bot_description').find('sam_bot_description')
    default_model_path = os.path.join(pkg_share, 'src/description/sam_bot_description.urdf')
    default_rviz_config_path = os.path.join(pkg_share, 'rviz/urdf_config.rviz')
    gazebo_dir = os.path.join(get_package_share_directory('gazebo_ros'), 'launch')
    world = os.path.join(pkg_share, 'worlds', 'room.world')

    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': Command(['xacro ', LaunchConfiguration('model')])}]
    )
    joint_state_publisher_node = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        condition=launch.conditions.UnlessCondition(LaunchConfiguration('gui'))
    )
    
    #rviz_node = launch_ros.actions.Node(
    #    package='rviz2',
    #    executable='rviz2',
    #    name='rviz2',
    #    output='screen',
    #    arguments=['-d', LaunchConfiguration('rvizconfig')],
    #)
    
    #gzclient = ExecuteProcess(
    #    cmd=['killall', '-q', 'gzclient'],
    #    output='screen'
    #)

    #gzserver = ExecuteProcess(
    #    cmd=['killall', '-q', 'gzserver'],
    #    output='screen'
    #)


    #gazebo = ExecuteProcess(
    #        cmd=['gazebo', '--verbose', world, '-s', 'libgazebo_ros_init.so', 
    #        '-s', 'libgazebo_ros_factory.so'],
    #        output='screen')
    
    spawn_entity = launch_ros.actions.Node(
    	package='gazebo_ros', 
    	executable='spawn_entity.py',
        #arguments=['-entity', 'sam_bot', '-topic', 'robot_description', '-x','1.0','-y','1.0'],
        arguments=['-entity', 'sam_bot', '-topic', 'robot_description'],
        output='screen'
    )
    robot_localization_node = launch_ros.actions.Node(
         package='robot_localization',
         executable='ekf_node',
         name='ekf_filter_node',
         output='screen',
         parameters=[os.path.join(pkg_share, 'config/ekf.yaml'), {'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )


    
    return launch.LaunchDescription([

        ExecuteProcess(
            cmd=['killall','-q', 'gzserver'],
            output='screen'),
        ExecuteProcess(
            cmd=['killall','-q', 'gzclient'],
            output='screen'),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([gazebo_dir, '/gzserver.launch.py']),
            launch_arguments={
                 'world': world
                 }.items(),
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([gazebo_dir ,'/gzclient.launch.py'])),

        launch.actions.DeclareLaunchArgument(name='gui', default_value='True',
                                            description='Flag to enable joint_state_publisher_gui'),
        launch.actions.DeclareLaunchArgument(name='model', default_value=default_model_path,
                                            description='Absolute path to robot urdf file'),
        launch.actions.DeclareLaunchArgument(name='rvizconfig', default_value=default_rviz_config_path,
                                            description='Absolute path to rviz config file'),
        launch.actions.DeclareLaunchArgument(name='use_sim_time', default_value='True',
                                            description='Flag to enable use_sim_time'),
        #launch.actions.ExecuteProcess(cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so'], output='screen'),        
        #gazebo,
        #gzclient,
        #gzserver,
        joint_state_publisher_node,
        robot_state_publisher_node,
        spawn_entity,
        robot_localization_node,
        #rviz_node
    ])
