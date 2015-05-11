#!/bin/bash

cd ~/catkin_ws
source devel/setup.bash
rosrun ardrone_autonomy ardrone_driver &
rosrun tum_ardrone drone_stateestimation & 
rosrun tum_ardrone drone_autopilot &
rosrun tum_ardrone drone_gui &
gnome-terminal -x sh -c "cd /home/michael/CUT_Drone/scripts; ./matlab_deamon.sh; bash"&
rosrun tum_ardrone takePicture 
gnome-terminal -x sh -c "python ~/CUT_Drone/scripts/forward_pass.py"