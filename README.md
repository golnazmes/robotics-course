# CMPUT503 (Robotics)
Cancel changes
This Repository is for sharing codes and exercises of CMPUT 503 course at the UofA. \
More information can be found on this personal website: https://golnazmes.github.io/Robotics.html

## Running the Codes

Each exercise has its own directory. \
All the exercises follow the format of this repository.: https://github.com/duckietown/template-ros \
This template provides a boilerplate repository for developing ROS-based software in Duckietown. 

To run the code, you need to cd to the directory of that exercise, and build and run the code on duckiebot with the following commands: 

```bash
cd ExerciseX
dts devel build -f -H DUCKIEBOT_NAME
dts devel run -H DUCKIEBOT_NAME
```

## Description of Exercises
### Exercise 1

This exercise was about building the duckiebot and running some simple code on it.(make the duckiebot say hello!)

### Exercise 2
This exercise was about the introduction to ROS and kinematics.
We built the following tasks for this lab: \
1- Make the duckiebot move in a multi-state task \
2- Make the duckiebot change its LED colors \
3- Estimate the robot’s pose in the world frame, and an introduction to odometry \


