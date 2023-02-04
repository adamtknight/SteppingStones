import os
import random
import shutil
import time

RIGHT_SHIFT_BACK = False 
RIGHT_SHIFT_FORWARD = False
RIGHT_SHIFT_RIGHT = True
RIGHT_SHIFT_LEFT =True

LEFT_SHIFT_BACK = False
LEFT_SHIFT_FORWARD = False
LEFT_SHIFT_RIGHT = True
LEFT_SHIFT_LEFT = True

PERTRUBED_STEP_ARRAY = [4, 5, 6]

NUMBER_OF_STEPS = 100

FILENAME = "TEST"
FILE_DESTINATION_PATH = "C:/Users/Neurolab/Documents/Projects/Knight/SteppingStones/code/Temp_Main"
BACKUP_FILE_PATH = "C:/Users/Neurolab/Documents/Projects/Knight/Back_Up_Stepping_Stones_Paths"



num_steps = NUMBER_OF_STEPS
shift_arr = []
p_step_arr = []
shift_array_len = 0
p_step_arr_len = 0
filename = FILENAME
path = FILE_DESTINATION_PATH

if RIGHT_SHIFT_BACK:
    shift_arr.append(1)
if RIGHT_SHIFT_FORWARD:
    shift_arr.append(2)
if RIGHT_SHIFT_RIGHT:
    shift_arr.append(3)
if RIGHT_SHIFT_LEFT:
    shift_arr.append(4)
if LEFT_SHIFT_BACK:
    shift_arr.append(5)
if LEFT_SHIFT_FORWARD:
    shift_arr.append(6)
if LEFT_SHIFT_RIGHT:
    shift_arr.append(7)
if LEFT_SHIFT_LEFT:
    shift_arr.append(8)

shift_arr_len = len(shift_arr)
p_step_arr = PERTRUBED_STEP_ARRAY
p_step_arr_len = len(p_step_arr)


filepath = os.path.join(path, filename)

if not os.path.exists(path):
    print("WARNING: Invalid path or path does not exist.")
    exit()

if os.path.exists(filepath):
    user_input = input("WARNING: File already exists, press y to continue and overwrite the file or any other key to exit...")
    if user_input.lower() == 'y':
        file = open(filepath, "w").close()
        file = open(filepath, "w")
    else:
        exit()
else:
    file = open(filepath, "w")
i = 0
while(i < num_steps):
    rand_num_p_steps = random.choice(p_step_arr)
    for j in range(rand_num_p_steps):
        file.write("0 ")
        i+=1
        if i >= num_steps:
            break
    if i >= num_steps:
            break
    
    timeout = 5 # set timeout value in seconds
    start_time = time.time()
    random_p_step = random.choice(shift_arr)
    while((random_p_step <= 4 and (i)%2==1) or (random_p_step > 4 and (i)%2 ==0)):
        random_p_step = random.choice(shift_arr)
        if time.time() - start_time > timeout:
            print("Invalid Pertrubed Step Array, ensure that the array has an odd and even number if only pertrubing one side")
            file = open(filepath, "w").close()
            exit(1)   
    file.write(str(random_p_step) + " ")
    i+=1

num_backup = 0
backuppath = BACKUP_FILE_PATH + "/" + filename + "_backup" + "_"
while os.path.exists(backuppath):
    backuppath = backuppath + str(num_backup)
    num_backup += 1
shutil.copy2(filepath, backuppath)

file.close()





