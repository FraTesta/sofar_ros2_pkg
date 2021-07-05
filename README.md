# ROS2_ortopillar

# ROS 2 Foxy installation
1. follow the tutorial : https://docs.ros.org/en/foxy/Installation/Ubuntu-Install-Debians.html
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

# Ortopillar_packages

Currently the model of the ortopillar is defined in the _sam_bot_description_ package, which contains the xacro model and the localization_robot definition. This last one provides the transformations needed w.r.t. the odom frame and an ekf for the odometry.
1. clone this pkgs into your ros 2 workspace

2. install: 
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
## Run 

1. run the command to spawn the robot in gazebo: 
   ```
   ros2 launch sam_bot_description display.launch.py 
   ```

2.  in another shell type < rviz2 > and load the configuration or create a new one.

# Nav2 installation
  The Navigation2 package provides several tools for the autonomous navigation. But it needs a slam package to build a map to use in its navigation algorithm.
  Therefore install the slam toolbox and navigation2 packages:
  ```
  sudo apt-get install ros-foxy-slam-toolbox
  sudo apt-get install ros-foxy-navigation2
  sudo apt-get install ros-foxy-nav2-bringup
  ```
  Since the navigation2 pkg requires the setting of several configuration file in order to adapt the application to a custom robot, it's necessary to build the navigation2 pkg that we have provided in this project using the following commands: 
   ```

  ```

   ## Run 
   ### Map Generation
   As already said first of all we need to build a map to send to the navigation2, thus use the following commands to crate the map of the provided world. Please notice that a map is already provided in the map directory of the nav2_bringup pkg so you can skip the following commands and go to the _Launch_Navigation_.

   1. launch the ortopillar simulation:
   ```
   ros2 launch sam_bot_description display.launch.py
   ```
   2. In another __sourced__ terminal launch the slam node:
   ```
   ros2 launch orto_nav slam.launch.py
   ```
   3. In the final terminal (__sourced__) launch the teleop in order to drive the robot and build the whole map :
   ```
   ros2 run teleop_twist_keyboard teleop_twist_keyboard
   ```
   4. Save the map (il primo comando la salva nella WS con il secondo dovrebbe salvarla in nav2_bringup)
  ```
   ros2 run nav2_map_server map_saver_cli -f /home/<username>/<workspace_name>/src/navigation2/nav2_bringup/bringup/maps/map
   ```
   ### Launch Navigation

   1. launch the ortopillar simulation:
   ```
   ros2 launch sam_bot_description display.launch.py
   ```

   2. Launch the navigation nodes
   ```
   ros2 launch orto_nav bringup_launch.py use_sim_time:=True autostart:=True \map:=/home/<username>/<workspace_name>/src/orto_nav/maps/map.yaml
   ```
   3. In another terminal launch rviz2 with the proper project configuration
  ```
    ros2 run rviz2 rviz2 -d $(ros2 pkg prefix nav2_bringup)/share/nav2_bringup/rviz/nav2_default_view.rviz
  ```
  4. In a new terminal start a node that publish to the topic /initialpose in order tu define an initial estimated pose without using Rviz Tool.

  ```
    ros2 run sam_bot_descrition initPose.py
  ```
   1. Finally you can set a goal position just placing the _Nav2d Goal_ Rviz graphic tool in the desired position. Or you can set it from another terminal using:
   ```
   ros2 topic pub /goal_pose geometry_msgs/PoseStamped "{header: {stamp: {sec: 0}, frame_id: 'map'}, pose: {position: {x: 0.2, y: 0.0, z: 0.0}, orientation: {w: 1.0}}}"
   ```

# Useful Commands
```
ros2 run tf2_ros tf2_echo <frame1> <frame2>  # to see the tf publications between two frames
ros2 run tf2_tools view_frames.py    # to build the frames tree 
```
# Problems
Il modello su rviz *blinka*
# To Do
1. Find a way to compute and store the distance between the robot and the current goal in order to send it to the ROS1 simulation. 
2. Implement a node that handle the robot-goal distance and sent this information ROS1 using the ros_bridge.
3. Unico launch (opzionale)
4. Sistemare i parametri della navigazione soprattutto per la recovery mode
