cmake_minimum_required(VERSION 3.5)
project(sam_bot_description)

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)
find_package(geometry_msgs REQUIRED)
#find_package(glm REQUIRED)
# find_package(example_interfaces REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rcl_interfaces REQUIRED)
#find_package(rcutils)
#find_package(rmw REQUIRED)
#find_package(rosidl_cmake REQUIRED)
#find_package(rosidl_default_generators REQUIRED)
# find_package(rosidl_typesupport_cpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_geometry_msgs REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(visualization_msgs REQUIRED)


# Install the python module for this package
ament_python_install_package(${PROJECT_NAME})

# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

#add_executable(initialPose src/InitialPoseNode.cpp)
#ament_target_dependencies(initialPose rclcpp std_msgs geometry_msgs tf)

install(
  DIRECTORY src launch rviz config worlds maps scripts
  DESTINATION share/${PROJECT_NAME}
)

#file(GLOB SCRIPT_FILES scripts/*)
#install(PROGRAMS ${SCRIPT_FILES}
#  DESTINATION lib/${PROJECT_NAME})
install(PROGRAMS scripts/initPose.py DESTINATION bin)
#install(TARGETS
#  initialPose
#  DESTINATION lib/${PROJECT_NAME})

if(BUILD_TESTING)

  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # uncomment the line when a copyright and license is not present in all source files
  #set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # uncomment the line when this package is not in a git repo
  #set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()
# Export package dependencies
ament_export_dependencies(ament_cmake)
ament_export_dependencies(ament_cmake_python)
ament_export_dependencies(rclcpp)
#ament_export_dependencies(rclpy)
#ament_export_include_directories(include ${rclcpp_INCLUDE_DIRS})
#ament_export_libraries(${PROJECT_NAME} ${rclcpp_LIBRARIES})

ament_package()
