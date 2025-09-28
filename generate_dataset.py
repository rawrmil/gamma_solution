import bpy
import math
import os
from random import random


def obj_place(obj_name, x, y, z):
    obj = scene.objects[obj_name]
    #dim = obj.dimensions
    new_obj = obj.copy()
    new_obj.data = obj.data.copy()  # optional, if you want a full copy
    bpy.context.collection.objects.link(new_obj)
    new_obj.location = (x, y, z)
    return (obj_name, new_obj.location, new_obj)

def rnd(rmin, rmax):
    return rmin+random()*(rmax-rmin)

def obj_random_place(obj_name):
    return obj_place(obj_name, rnd(-0.8, 0.8), rnd(-0.8, 0.8), rnd(0.0, 1.5))

# Vars

class_names = ['obj_tablet', 'obj_laptop', 'obj_group_box']

# Render

bpy.ops.wm.open_mainfile(filepath="scene.blend")
scene = bpy.data.scenes["Scene"]

objs = []
for i in range(10):
    objs.append(obj_random_place(class_names[i%3]))

fine_tuning_values = []
for o in objs:
    obj_name, loc, dim = o[0], o[1], o[2].dimensions
    obj_index = class_names.index(obj_name)
    fine_tuning_values.append([obj_index, loc[0], loc[1], loc[2], dim[0], dim[1], dim[2]])
print(fine_tuning_values)

scene.render.engine = 'BLENDER_EEVEE_NEXT'
scene.render.resolution_x = 100
scene.render.resolution_y = 100
scene.eevee.taa_render_samples = 4

cam1 = scene.objects['camera1']
cam2 = scene.objects['camera2']

scene.render.filepath = './left.png'
scene.camera = cam1
bpy.ops.render.render(write_still=True)

scene.render.filepath = './right.png'
scene.camera = cam2
bpy.ops.render.render(write_still=True)
