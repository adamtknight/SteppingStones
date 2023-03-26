# Stepping Stones Project README

## Project Description
This project uses QTM (Qualisys Tracking Manager), asyncio, and pygame to project stepping stone tiles on a treadmill and track the location of the tiles using QTM, a motion capture system that tracks the person walking on the stepping stones. The stepping stones can perturb (shift) during the experiment.

## Requirements
- Qualisys Motion Capture software installed and running
- Real-Time Protocol (RTP) enabled in Qualisys
- Python 3.7 or higher
- Installed Python libraries: asyncio, pygame, qtm, win32api

## Project Setup
1. Ensure the screen resolutions are set correctly for the two screens:
   - Screen 1 resolution = 1900x1200
   - Screen 2 resolution = 1280x800
2. Extend screens and ensure screen 2 (the projector) is in the top right corner. This can be found in the computer's display settings.
3. Make sure the four red dots displayed on the screen are on the bolts of the treadmill.

## Running the Experiment
To run the experiment, follow these steps:

1. Open the Command Prompt.
2. Navigate to the folder titled SteppingStones using cd command.
3. Run the command `code .` to open Visual Studio Code and edit the variables in stones.py.
4. Save the file.
5. Start a recording in Qualisys or open a realtime file by clicking the white paper marker in the top left corner.
6. In the Command Prompt, run the command `python stones.py` to execute the file.

## Adjusting Variables and Randomization
To adjust variables and randomization, follow these steps:

1. In Visual Studio Code, open the file createstudyrandomization.py.
2. Adjust the variables as needed.
3. Save the file.
4. Run the command `python createstudyrandomization.py` in the Command Prompt.

The createstudyrandomization.py file will save a new file with the randomized stepping stones in the specified FILE_DESTINATION_PATH. Update the FILEPATH_TO_STEPPATH variable in stones.py with the generated file's path.

## Variables in stones.py
Here is a description of the important variables in the stones.py file:

- TREADMILL_SPEED_RIGHT: The treadmill speed for the right foot (m/s)
- TREADMILL_SPEED_LEFT: The treadmill speed for the left foot (m/s)
- STEP_LENGTH_RIGHT: The step length for the right foot (m)
- STEP_LENGTH_LEFT: The step length for the left foot (m)
- STEP_WIDTH: The width between steps (m)
- STONE_WIDTH: The width of the stepping stone (m)
- STONE_HEIGHT: The height of the stepping stone (m)
- COLLECTION_TIME: The time for data collection (s)
- FREQUENCY: The frequency of the frames per second (frames/sec)

### Shift Distances
- RIGHT_SHIFT_BACK_DIST: The distance to shift the right stone back (m)
- RIGHT_SHIFT_FORWARD_DIST: The distance to shift the right stone forward (m)
- RIGHT_SHIFT_RIGHT_DIST: The distance to shift the right stone right (m)
- RIGHT_SHIFT_LEFT_DIST: The distance to shift the right stone left (m)
- LEFT_SHIFT_BACK_DIST: The distance to shift the left stone back (m)
- LEFT_SHIFT_FORWARD_DIST: The distance to shift the left stone forward (m)
- LEFT_SHIFT_RIGHT_DIST: The distance to shift the left stone right (m)
- LEFT_SHIFT_LEFT_DIST: The distance to shift the left stone left (m)

### Threshold Marker Settings
- USE_THRESHOLD_MARKER: This setting determines whether a threshold marker will be used or not

### Threshold Marker Settings
- USE_THRESHOLD_MARKER: This setting determines whether a threshold marker will be used or not. Set this to True if you want to use a threshold marker; otherwise, set it to False.
- DISTANCE_FROM_WALL: If USE_THRESHOLD_MARKER is set to False, you can specify the distance from the wall in meters. The stones will be perturbed when they reach this distance.
- LATENCY: If USE_THRESHOLD_MARKER is set to True, specify the latency in milliseconds between the time the threshold marker is detected and the actual perturbation.
- THRESHOLD_ARR: An array containing possible threshold values in meters. A random value from this array will be chosen as the threshold distance for each stone.
- PREDICTIVE: Set to True if you want the system to predict the position of the threshold marker; otherwise, set to False.
- THRESHOLD_MARKER_ID: The index of the threshold marker in the marker list, indexed at 0.
- FILEPATH_TO_STEPPATH: The file path to the stepping path file that contains perturbation information. This file can be generated using createstudyrandomization.py.
- FILEPATH_TO_OUTPUT_DATA: The file path where the output data will be saved as a CSV file.

## Running the Program
1. Adjust the variables in the stones.py file as needed and save the file.
2. If you want to create a new stepping path with random perturbations, adjust the variables in createstudyrandomization.py, run the file, and save the generated file to the specified path.
3. Ensure that the Qualisys Motion Capture system is open and that the real-time protocol is enabled.
4. Before starting the stepping stones, make sure a real-time file is open by clicking the white paper marker in the top left corner in Qualisys or by starting a recording.
5. Navigate to the command prompt, and navigate to the folder titled "Stepping Stones". Run 'code .' to open Visual Studio Code and edit the variables.
6. To execute the file, run `python stones.py` in the command prompt.

Ensure that the four red dots displayed on the screen are on the bolts of the treadmill to confirm that no screen resolutions have changed. Once you've confirmed that the four red dots are correctly positioned on the treadmill bolts, the stepping stones program will begin running. The stones will start moving along the treadmill, and participants will be prompted to step on them.

As the participants step on the stones, the Qualisys Motion Capture system will track their movements and provide real-time data. If the USE_THRESHOLD_MARKER setting is enabled, the system will detect the threshold marker and initiate perturbations accordingly.

During the experiment, monitor the participants and the system to ensure everything is working correctly. If any issues arise, stop the experiment and troubleshoot as needed.

Once the experiment is completed, the output data will be saved as a CSV file in the specified FILEPATH_TO_OUTPUT_DATA location. This data can be used for further analysis and interpretation.
