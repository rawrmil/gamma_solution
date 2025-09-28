import bpy
import math
import os
import shutil
from random import random
from random import randint
import json

# Vars

class_names = ['obj_tablet', 'obj_laptop', 'obj_group_box']

def obj_place(scene, obj_name, x, y, z, y_rot):
    obj = scene.objects[obj_name]
    #dim = obj.dimensions
    new_obj = obj.copy()
    new_obj.data = obj.data.copy()  # optional, if you want a full copy
    bpy.context.collection.objects.link(new_obj)
    new_obj.location = (x, y, z)
    new_obj.rotation_euler[2] += math.radians(y_rot)
    return (obj_name, new_obj)

def rnd(rmin, rmax):
    return rmin+random()*(rmax-rmin)

def obj_random_place(scene):
    return obj_place(
        scene,
        class_names[randint(0, len(class_names)-1)],
        rnd(-0.8, 0.8),
        rnd(-0.8, 0.8),
        rnd(0.0, 1.5),
        90*randint(0, 1))

# Create dirs

if os.path.isdir("./generated_dataset"):
    shutil.rmtree("./generated_dataset")
os.makedirs("./generated_dataset", exist_ok=True)

# Render

bpy.ops.wm.open_mainfile(filepath="scene.blend")
main_scene = bpy.data.scenes["Scene"]
main_scene.render.engine = 'BLENDER_WORKBENCH'
main_scene.render.resolution_x = 100
main_scene.render.resolution_y = 100

main_scene.display.shading.light = 'STUDIO'
main_scene.display.shading.color_type = 'TEXTURE'
main_scene.display.shading.show_shadows = False
main_scene.display.shading.show_cavity = False

def save_label(fpath, fine_tuning_values):
    with open(fpath, "w") as f:
        s = ""
        for e in fine_tuning_values:
            s += " ".join(map(str, e))
            s += "\n"
        f.write(s)

def generate_render(dataset_type, dataset_data, i):
    scene = main_scene.copy()
    bpy.context.window.scene = scene

    objs = []
    for j in range(10):
        objs.append(obj_random_place(scene))

    #fine_tuning_values_left = []
    #fine_tuning_values_right = []
    class_count = [0]*len(class_names)
    for o in objs:
        obj_name, loc, dim = o[0], o[1].location, o[1].dimensions
        obj_index = class_names.index(obj_name)
        class_count[obj_index] += 1
        #fine_tuning_values_left.append([obj_index, +loc[0], +loc[1], loc[2], dim[0], dim[1], dim[2]])
        #fine_tuning_values_right.append([obj_index, -loc[0], -loc[1], loc[2], dim[0], dim[1], dim[2]])

    cam1 = scene.objects['camera1']
    cam2 = scene.objects['camera2']

    dataset_data["entries"].append({})

    scene.render.filepath = f"./generated_dataset/{dataset_type}/left{i}.png"
    scene.camera = cam1
    bpy.ops.render.render(write_still=True)
    dataset_data["entries"][-1]["left"] = scene.render.filepath

    scene.render.filepath = f"./generated_dataset/{dataset_type}/right{i}.png"
    scene.camera = cam2
    bpy.ops.render.render(write_still=True)
    dataset_data["entries"][-1]["right"] = scene.render.filepath

    dataset_data["entries"][-1]["class_count"] = class_count

    bpy.data.scenes.remove(scene)

def generate_dataset(dataset_type, count):
    dataset_data = {
        'classes': class_names,
        'entries': []
    }
    for i in range(count):
        generate_render(dataset_type, dataset_data, i)
    with open(f"./generated_dataset/{dataset_type}.json", "w") as f:
        json.dump(dataset_data, f)

generate_dataset("train", 10)
generate_dataset("val", 5)
