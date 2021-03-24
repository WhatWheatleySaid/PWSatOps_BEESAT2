"""
Written by Alexander M. Bauer (BSc. , Technical University Berlin)

This Script takes CSV-File and converts contained positions and quaternions into keyframes for
rotation and translation. It was used to visualize the recorded data in an experiment with the Cubesat BEESAT-2 (TU-Berlin)
"""


import bpy

import csv
import math
 
def euler_from_quaternion(x, y, z, w):
        """
        Convert a quaternion into euler angles (roll, pitch, yaw)
        roll is rotation around x in radians (counterclockwise)
        pitch is rotation around y in radians (counterclockwise)
        yaw is rotation around z in radians (counterclockwise)
        """
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll_x = math.atan2(t0, t1)
     
        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = math.asin(t2)
     
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = math.atan2(t3, t4)
     
        return roll_x, pitch_y, yaw_z # in radians

time_list = []
x_quat = []
y_quat = []
z_quat = []
w_quat = []
x_ef = []
y_ef= []
z_ef = []

#read the CSV to lists 
with open(r'.\beesat2_quaternions_full.csv') as csvfile:
    csvreader = csv.reader(csvfile, delimiter = ';')
    for row in csvreader:
        print(row)
        time_list.append(row[0])
        x_quat.append(row[1])
        y_quat.append(row[2])
        z_quat.append(row[3])
        w_quat.append(row[4])
        x_ef.append(row[5])
        y_ef.append(row[6])
        z_ef.append(row[7])

      
#get the scene object and get the object refering to BEESAT-2
scene = bpy.context.scene
beesat2 = bpy.data.objects['BeeSat2']

frames_per_second = 1
number_of_frame = 0

earth_diameter = 2*6371

for x,y,z, qx,qy,qz,qw in zip(x_ef,y_ef,z_ef, x_quat, y_quat, z_quat, w_quat):
    
    #set current frame of scene
    scene.frame_set(number_of_frame)
    
    #use last available data in case of missing data in TM Frame:
    if x == '':
        x = last_x
    if y == '':
        y = last_y
    if z == '':
        z = last_z
      
    #set location and keyframe it to the current frame
    #(location normalised from 0 to 1 to improve animation quality and accuracy (earth radius in 3D viewport is 1))  
    beesat2.location = (float(x)/earth_diameter,float(y)/earth_diameter,float(z)/earth_diameter)
    beesat2.keyframe_insert(data_path = 'location', index = -1)
    
    #use last available data in case of missing data in TM Frame:
    if qx == '' or qy == '' or qz == '' or qw == '':
        qx = last_qx
        qy = last_qy
        qz = last_qz
        qw = last_qw
    
    #convert quaternion to euler angles as Blender only likes Euler format (in radians):
    euler_x, euler_y, euler_z = euler_from_quaternion(float(qx),float(qy),float(qz),float(qw))
    
    #rotate beesat2 (always relative to ECEF system, angles do not sum up)
    beesat2.rotation_euler = (euler_x, euler_y , euler_z)
    beesat2.keyframe_insert(data_path="rotation_euler", index=-1)
    
    #increase frame counter by FPS amount
    number_of_frame += frames_per_second
    
    last_x = x
    last_y = y
    last_z = z
    last_qx = qx
    last_qy = qy
    last_qz = qz
    last_qw = qw