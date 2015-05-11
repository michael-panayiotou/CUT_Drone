#!/bin/bash 
cd ~/catkin_ws;
	source devel/setup.bash
	
	rosrun tum_ardrone publish_command _xCoordinate:=$1
	sleep 5
	rosrun tum_ardrone takePicture
	exit