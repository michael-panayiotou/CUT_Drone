#!/bin/bash   

first=$(date +%s -r /home/michael/CUT_Drone/raw_data/raw_image.jpg);
temp=$first;
while [ true ]
do 
	if [ $first != $temp ]; then
		
		cd ~/CUT_Drone/scripts;
		sudo ./open_matlab_command.sh;
		
		
		first=$(date +%s -r /home/michael/CUT_Drone/raw_data/raw_image.jpg);
	fi

	temp=$(date +%s -r /home/michael/CUT_Drone/raw_data/raw_image.jpg);
done
