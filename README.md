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

# ROS2_ortopillar_packages


1. clone this pkgs into your ros 2 workspace

2. install: 
   ```
   pip3 install xacro
   sudo apt install ros-foxy-xacro
   ros-foxy-joint-state-publisher-gui
   sudo apt install ros-foxy-robot-localization
   ```

3. colcon build at the root of the workspace
## Run 

1. run the command to spawn the robot in gazebo: 
   ```
   ros2 launch sam_bot_description display.launch.py 
   ```
2. in another shell: ros2 launch orthopillar_robot_controller_pkg controller_estimator.launch.py (make the robot move using odometry and lidar).

3.  in another shell type < rviz2 > and load the configuration or create a new one.

# Nav2 installation
  Install the slam toolbox and navigation2 packages
  ```
  sudo apt-get install ros-foxy-slam-toolbox
  sudo apt-get install ros-foxy-navigation2
  sudo apt-get install ros-foxy-nav2-bringup


  ```
   ## Run 
   1. launch the ortopillar simulation:
   ```
   ros2 launch sam_bot_description display.launch.py
   ```
   2. **Add some obstacles in the environment from Gazebo.**

   3. In another __sourced__ (. install/setup.bash) terminal launch the slam node:
   ```
   ros2 launch orto_nav slam.launch.py
   ```
   4. In the final terminal (__sourced__) launch the teleop in order to drive the robot and build the whole map :
   ```
   ros2 run teleop_twist_keyboard teleop_twist_keyboard
   ```
   5. Save the map (il primo comando la salva nella WS con il secondo dovrebbe salvarla in nav2_bringup)
  ```
   ros2 run nav2_map_server map_saver_cli -f map
   ros2 run nav2_map_server map_saver_cli -f /home/francescotesta/prove_ws/src/navigation2/nav2_bringup/bringup/maps/map
   ```
   
   6. Launch the navigation node keeping the robot and slam nodes active (non so se serve ribuildare la WS di navigation2 per aggiornare la mappa)
   ```
   ros2 launch nav2_bringup navigation_launch.py
   ```
   7. Finally in another terminal you can give a goal position to the robot using the nav2 action server (Non va ancora però riceve i goal msg, riprovare con una mappa completa):
   ```
   ros2 topic pub /goal_pose geometry_msgs/PoseStamped "{header: {stamp: {sec: 0}, frame_id: 'map'}, pose: {position: {x: 0.2, y: 0.0, z: 0.0}, orientation: {w: 1.0}}}"
   ```

# Comandi Utili
```
ros2 run tf2_ros tf2_echo <frame1> <frame2>  # per vedere le pubblicazioni tra frame
ros2 run tf2_tools view_frames.py    # per generare l'albero dei frame 
ros2 run topic pub /demo/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"   # per muovere il robot 
```
# Problems
```
[rviz2-5] [ERROR] [1621514855.514780670] [rviz2]: Vertex Program:rviz/glsl120/indexed_8bit_image.vert Fragment Program:rviz/glsl120/indexed_8bit_image.frag GLSL link result : 
[rviz2-5] active samplers with a different type refer to the same texture image unit
```

Ogni volta che compare questo errore [**display.launch.py**] da rviz2 sparisce la mappa:

```
[rviz2-5] [INFO] [1622370093.323633856] [rviz2]: Trying to create a map of size 155 x 155 using 1 swatches
```