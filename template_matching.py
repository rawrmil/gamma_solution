import cv2
import numpy as np
import os
import dataset
import math 

ds = dataset.get_dataset()

def get_result_points(templ, res, sens):
    res_points = [] # (x, y)
    threshold = sens
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        res_points.append((pt[0], pt[1]))
    return res_points

def show_matching_results(img, templ, res_points, col):
    h, w = templ.shape[:-1]
    for i, e in enumerate(res_points):
        cv2.rectangle(img, e, (e[0]+w, e[1]+h), tuple(col), 2)

def load_templates(tdir):
    templs = []
    files = [f for f in os.listdir(tdir)]
    for e in files:
        templs.append(cv2.imread(f"{tdir}/{e}"))
    return templs

def find_templates(img, templ_group, thr, col):
    templs = load_templates(templ_group)
    for e in templs:
        ls_template = e
        ls_results = cv2.matchTemplate(img, ls_template, cv2.TM_CCOEFF_NORMED)
        res_points = get_result_points(ls_template, ls_results, thr)
        dis = min(ls_template.shape[:-1])
        for i in range(len(res_points)-1, -1, -1):
            for j in range(len(res_points)-1):
                if i != j and math.dist(res_points[i], res_points[j]) < dis:
                    res_points.pop(i)
                    break
                
        show_matching_results(img, ls_template, res_points, col)
        cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Image', 800, 600)

for i in range(len(ds)):
    for k in ['left', 'right']:
        test_entry = ds[i][0]
        print(f"{test_entry}/{k}.png")
        img = cv2.imread(f"{test_entry}/{k}.png")
        img = img[0:1041, 405:1464]
        #find_templates(img, './templates/tablet_sticker', 0.75, (255, 0, 0))
        find_templates(img, './templates/laptop_sticker', 0.75, (255, 0, 0))
        find_templates(img, './templates/laptop_top', 0.75, (0, 255, 0))
        cv2.imshow('Image', img)
        while True:
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
cv2.destroyAllWindows()
