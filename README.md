![Unige Logo](https://raw.githubusercontent.com/FraTesta/sofar_ros2_pkg/blob/main/Pic/unige_stemma.png)
# __ROS2_ortopillar__
This repository contains all packages and files related to the ROS2 part of the __Banxter__ SOFAR project. Follow all the links to the sections of the repository description.

## **Table Of Contents**
  - [__ROS 2 Foxy installation__](#ros-2-foxy-installation)
  - [__Ortopillar packages installation__](#ortopillar-packages-installation)
  - [__Navigation2 installation__](#navigation2-installation)
  - [__Project Execution__ ](#project-execution)
    - [__Map Generation__](#map-generation)
    - [__Launch Navigation__](#launch-navigation)
  

## __ROS 2 Foxy installation__
This section explain you how to properly install ROS2 Foxy on your Ubuntu 20 machine.  
1. Follow the tutorial: https://docs.ros.org/en/foxy/Installation/Ubuntu-Install-Debians.html
2. install also the following dependencies:
```
sudo apt update && sudo apt install -y \
  build-essential \
  cmake \
  git \
  libbullet-dev \
  python3-colcon-common-extensions \
  python3-flake8 \
  python3-pip \
  python3-pytest-cov \
  python3-rosdep \
  python3-setuptools \
  python3-vcstool \
  wget

python3 -m pip install -U \
  argcomplete \
  flake8-blind-except \
  flake8-builtins \
  flake8-class-newline \
  flake8-comprehensions \
  flake8-deprecated \
  flake8-docstrings \
  flake8-import-order \
  flake8-quotes \
  pytest-repeat \
  pytest-rerunfailures \
  pytest

sudo apt install --no-install-recommends -y \
  libasio-dev \
  libtinyxml2-dev

sudo apt install --no-install-recommends -y \
  libcunit1-dev

  sudo apt-get install -y python3-rosgraph

  sudo apt install ros-foxy-gazebo-ros-pkgs



   ```

## __Ortopillar packages installation__

Currently the model of the ortopillar is defined in the __sam_bot_description__ package, which contains the model description (SDF and URDF) and the __localization_robot__ script. This last script provides all the transformations needed w.r.t. the odom frame and an EKF for the odometry estimation.
1. Clone this pkgs into your ros 2 workspace
2. Install: 
   ```
   pip3 install xacro
   sudo apt install ros-foxy-xacro
   ros-foxy-joint-state-publisher-gui
   sudo apt install ros-foxy-robot-localization
   ```

3. At the root of the workspace:
```
rosdep install -y -r -q --from-paths src --ignore-src --rosdistro foxy
```

4. Then:
```
colcon build --symlink-install
```
**Please Note** : If the command above does not work simply run:

```
colcon build 
```
### Run 

1. Run the command to spawn the robot in gazebo: 
   ```
   ros2 launch sam_bot_description display.launch.py 
   ```

2.  In another shell type <rviz2> and load the configuration or create a new one.

You should see the following simulated environement on Gazebo

![Robot Model](https://raw.githubusercontent.com/FraTesta/sofar_ros2_pkg/blob/main/Pic/robotModel.png)


## __Navigation2 installation__
  The Navigation2 package provides several tools for the autonomous navigation. But it needs a slam package to build a map to use in its navigation algorithm.
  Therefore install the slam toolbox and navigation2 packages:
  ```
  sudo apt-get install ros-foxy-slam-toolbox
  sudo apt-get install ros-foxy-navigation2
  sudo apt-get install ros-foxy-nav2-bringup
  ```
  Since the navigation2 pkg requires the setting of several configuration file in order to adapt the application to a custom robot, it's necessary to build the navigation2 pkg that we have provided in this project using the following commands: 
   ```
  colcon build
  ```

   ## __Project Execution__ 
   ### __Map Generation__
   As already mantioned, first of all we need to build a map to send to the navigation2 nodes, thus use the following commands to generate a map of the provided simulation world. __Please notice that a map is already provided in the map folder of the _nav2_bringup_ pkg, so you can skip the following steps and go to the _Launch_Navigation_ section__ !!!.

   1. Launch the ortopillar simulation:
   ```
   ros2 launch sam_bot_description display.launch.py
   ```
   2. In another __sourced__ terminal launch the slam node:
   ```
   ros2 launch orto_nav slam.launch.py
   ```
   3. In the final terminal (__sourced__) launch the teleoperation node in order to drive the robot and build the whole map:
   ```
   ros2 run teleop_twist_keyboard teleop_twist_keyboard
   ```
   4. Save the map in the proper foulder. __Remember to change the path with your folders__.
  ```
   ros2 run nav2_map_server map_saver_cli -f /home/<username>/<workspace_name>/src/navigation2/nav2_bringup/bringup/maps/map
   ```
   ### __Launch Navigation__

   1. Launch the ortopillar simulation:
   ```
   ros2 launch sam_bot_description display.launch.py
   ```

   2. Launch the navigation nodes loading the map as well. __Remember to change the path with your folders__.
   ```
   ros2 launch orto_nav bringup_launch.py use_sim_time:=True autostart:=True \map:=/home/<username>/<workspace_name>/src/orto_nav/maps/map.yaml
   ```
   3. In another terminal launch rviz2 with the proper project configuration
  ```
    ros2 run rviz2 rviz2 -d $(ros2 pkg prefix nav2_bringup)/share/nav2_bringup/rviz/nav2_default_view.rviz
  ```
  4. In a new terminal start a node that publish to the topic /initialpose the current position of the robot.

  ```
    ros2 run sam_bot_description initPose.py
  ```
  > :bangbang: Se non viene trovato l'eseguibile dello script `initPose.py` modificare `CMakeLists.txt` (line 57) del pkg **sam_bot_description** nel seguente modo:
  > ```
  >install(PROGRAMS scripts/initPose.py DESTINATION lib/${PROJECT_NAME})
  > ```
 
   5. Finally you can send a goal position just placing the _Nav2d Goal_ Rviz graphic tool in the desired position. Or you can send it from another sourced terminal using:
   ```
   ros2 topic pub /goal_pose geometry_msgs/PoseStamped "{header: {stamp: {sec: 0}, frame_id: 'map'}, pose: {position: {x: 0.2, y: 0.0, z: 0.0}, orientation: {w: 1.0}}}"
   ```
  At the end, you should see the generated path as shown in the following figure
    ![Navigation ](https://raw.githubusercontent.com/FraTesta/sofar_ros2_pkg/blob/main/Pic/navigationPath.png)

# Useful Commands
```
ros2 run tf2_ros tf2_echo <frame1> <frame2>  # to see the tf publications between two frames
ros2 run tf2_tools view_frames.py    # to build the frames tree 
```

# To Do
1. Find a way to compute and store the distance between the robot and the current goal in order to send it to the ROS1 simulation. 
2. Implement a node that handle the robot-goal distance and sent this information ROS1 using the ros_bridge.
3. Unico launch (opzionale)

## __Autors and Contacts__
Roberto Albanese 

Luca Covizzi

Chiara Terrile 

Francesco Testa   francesco.testa.ge@gmail.com

Andrea Tiranti    andrea.tiranti97@gmail.com