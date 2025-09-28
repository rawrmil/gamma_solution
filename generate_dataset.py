import bpy
import math
import os
import shutil
from random import random
import yaml

def obj_place(scene, obj_name, x, y, z):
    obj = scene.objects[obj_name]
    #dim = obj.dimensions
    new_obj = obj.copy()
    new_obj.data = obj.data.copy()  # optional, if you want a full copy
    bpy.context.collection.objects.link(new_obj)
    new_obj.location = (x, y, z)
    return (obj_name, new_obj.location, new_obj)

def rnd(rmin, rmax):
    return rmin+random()*(rmax-rmin)

def obj_random_place(scene, obj_name):
    return obj_place(scene, obj_name, rnd(-0.8, 0.8), rnd(-0.8, 0.8), rnd(0.0, 1.5))

# Vars

class_names = ['obj_tablet', 'obj_laptop', 'obj_group_box']

# Dataset resources

if os.path.isdir("./generated_dataset"):
    shutil.rmtree("./generated_dataset")
os.makedirs("./generated_dataset", exist_ok=True)
os.makedirs("./generated_dataset/images/train", exist_ok=True)
os.makedirs("./generated_dataset/images/val", exist_ok=True)
os.makedirs("./generated_dataset/labels/train", exist_ok=True)
os.makedirs("./generated_dataset/labels/val", exist_ok=True)

dataset_data = {
    'train': './generated_dataset/images/train',
    'val': './generated_dataset/images/val',
    'nc': len(class_names),
    'names': class_names
}

with open('./generated_dataset/data.yaml', 'w') as file:
    yaml.dump(dataset_data, file, default_flow_style=False)

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

def generate_render(dataset_entry_type):
    scene = main_scene.copy()
    bpy.context.window.scene = scene

    objs = []
    for j in range(10):
        objs.append(obj_random_place(scene, class_names[j%3]))

    fine_tuning_values_left = []
    fine_tuning_values_right = []
    for o in objs:
        obj_name, loc, dim = o[0], o[1], o[2].dimensions
        obj_index = class_names.index(obj_name)
        fine_tuning_values_left.append([
            obj_index,
            0,
            45,
            0,
            0,
            0,
            dim[0],
            dim[1],
            dim[2],
            +loc[0],
            +loc[1],
            +loc[2],
            0
        ])
        fine_tuning_values_right.append([
            obj_index,
            0,
            45,
            0,
            0,
            0,
            dim[0],
            dim[1],
            dim[2],
            -loc[0],
            -loc[1],
            +loc[2],
            0
        ])

    cam1 = scene.objects['camera1']
    cam2 = scene.objects['camera2']

    scene.render.filepath = f"./generated_dataset/values/{dataset_entry_type}/left{i}.png"
    scene.camera = cam1
    bpy.ops.render.render(write_still=True)
    save_label(f"./generated_dataset/labels/{dataset_entry_type}/left{i}.txt", fine_tuning_values_left)

    scene.render.filepath = f"./generated_dataset/values/{dataset_entry_type}/right{i}.png"
    scene.camera = cam2
    bpy.ops.render.render(write_still=True)
    save_label(f"./generated_dataset/labels/{dataset_entry_type}/right{i}.txt", fine_tuning_values_right)

    bpy.data.scenes.remove(scene)

for i in range(5):
    generate_render("train")
for i in range(2):
    generate_render("val")
