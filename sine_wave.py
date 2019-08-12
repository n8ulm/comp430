# Nathan Ulmer
# Comp430, Interactive Computer Graphics

import bpy
import colorsys
from math import sqrt, pi, sin, ceil
from random import TWOPI

# select all objects and delete,
# ensures the scene is cleared each time
# the script is ran
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# object count
count = 50

# scale of the model
scale = 10.0

# padding between objects
padding = 0.002

# size of individual objects,
# height of each object will change for each key frame
size = (scale / count) - padding
min_size = size * 0.25
max_size = size * scale * 10
size_difference = max_size - min_size

# j and k percent convert abstract grid position within loop to real-world coordinate.
# scale difference = scale - -scale, simplifies to scale*2
j_percent = 0.0
k_percent = 0.0
count_fraction = 1.0 / (count - 1)
scale_difference = scale * 2

# position of each object
y = 0.0
x = 0.0

# center of model
center_x = 0.0
center_y = 0.0
center_z = 0.0

# distance of object from center
# the maximum possible distance is used to normalize the distance.
rise = 0.0
run = 0.0
normalized_distance = 0.0
max_distance = sqrt(2 * scale * scale)

# for animation, track current frame, specify desired number of key frames,
# and invert frame count.
current_frame = 0
keyframe_count = 50
inverted_frame_count = 1.0 / (keyframe_count - 1)

# if the frame range of the secne is 0, set frame range from 0 to 150
frame_range = bpy.context.scene.frame_end - bpy.context.scene.frame_start
if frame_range == 0:
    bpy.context.scene.frame_end = 150
    bpy.context.scene.frame_start = 0
    frame_range = 150

# number of keyframes per frame
frame_increment = ceil(frame_range * inverted_frame_count)

# off_set and angle for generating wave.
off_set = 0.0
angle = 0.0

# for loop creates and set properties of each object based on the object count
for j in range(0, count, 1):
    # calculate position for current object along x and y axis
    k_percent = j * count_fraction
    x = -scale + k_percent * scale_difference

    j_percent = j * count_fraction
    y = -scale + j_percent * scale_difference

    # calculate rise and run for calculating height offset between objects
    rise = y - center_y
    rise *= rise

    run = x - center_x
    run *= run

    # calculate normalized distance using Pythogorean theorem
    # remap the normalized distance to a range -pi to pi
    normalized_distance = sqrt(rise + run) / max_distance
    off_set = -TWOPI * normalized_distance + pi

    # add icosphere and initialize position and size
    bpy.ops.mesh.primitive_ico_sphere_add(location=(center_x + x, center_y, center_z), size=size)

    # set current object, rename and apply mesh
    current = bpy.context.object
    current.name = 'Cube ({0:0>2d})'.format(j)
    current.data.name = 'Mesh ({0:0>2d})'.format(j)

    # create new material based from normalized_distance value
    # apply to current object
    mat = bpy.data.materials.new(name='Material ({0:0>2d})'.format(j))
    mat.diffuse_color = colorsys.hsv_to_rgb(normalized_distance, 1.0, 1.0)
    current.data.materials.append(mat)

    # for loop sets height of current object for each key frame
    # initial height is based off of off_set
    # track the current key frame.
    current_frame = bpy.context.scene.frame_start
    for f in range(0, keyframe_count, 1):

        # convert the keyframe into an angle.
        f_percent = f * inverted_frame_count
        angle = TWOPI * f_percent

        # set the scene to the current frame.
        bpy.context.scene.frame_set(current_frame)

        # change the scale on the y axis (located at objects scale[2]).
        # sin returns a value in the range -1 to 1. abs changes the range to 0 to 1.
        # the values are remapped to the desired scale with min + percent * (max - min).
        current.scale[2] = min_size + abs(sin(off_set + angle)) * size_difference

        # insert the key frame for the scale property.
        current.keyframe_insert(data_path='scale', index=2)

        # advance by the keyframe increment to the next keyframe.
        current_frame += frame_increment
