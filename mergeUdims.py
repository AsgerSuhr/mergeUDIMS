
def combineMergeUdims(prefix_name, flder, image_type):
    flderDic = {}
    for nr, i in enumerate(flder):
        try:
            var = re.findall(r'\d{4}.\w*$', i)[0]
            if var[-3:] == image_type:
                var = var[:4]
                var = str(var)
                print(var)
                flderDic[var] = []
            else:
                print(i, ' not a ', image_type, ' file')
                pass
        except:
            pass


    items = {}
    for item in flder:
        try:
            var = re.findall(r'\d{4}.\w*$', item)[0]
            if var[-3:] == image_type:
                var = var[:4]
                var = str(var)
                for k, i in flderDic.items():
                    if k == var:
                        i.append(item)
                        items[k] = i
            else:
                pass
        except:
            pass


    for key, item in items.items():
        if image_type == 'tif':
            im = cv2.imread(item[0], -1)
        elif image_type == 'exr':
            im = cv2.imread(item[0], cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
        imarray = np.array(im)
        for i in item[1:]:

            if image_type == 'tif':
                im2 = cv2.imread(i, -1)
            elif image_type == 'exr':
                im2 = cv2.imread(i, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
            imarray2 = np.array(im2)

            fnd = np.where(imarray2 != 0)

            lst = []
            for nr, i in enumerate(fnd[0]):
                lst.append([i, fnd[1][nr]])


            for i in lst:
                var = imarray2[i[0]][i[1]]
                imarray[i[0]][i[1]] = var
            print(i)

        if image_type == 'tif':
            try:
                tf.imsave(prefix_name + '_' + key + '.tif', imarray, compress=0)
            except:
                pass
        elif image_type == 'exr':
            try:
                cv2.imwrite(prefix_name + '_' + key + '.exr', imarray)
            except:
                pass
        print('succesfully created file: ', prefix_name + '_' + key)
        print('continueing...')
    input('Done')


if __name__ == '__main__':

    import subprocess
    try:
        import cv2
    except ModuleNotFoundError:
        subprocess.check_call(['python', '-m', 'pip', 'install', 'opencv-python'])
        subprocess.check_call(['python', '-m', 'pip', 'install', 'numpy'])
        subprocess.check_call(['python', '-m', 'pip', 'install', 'tiffile'])
    import numpy as np
    import re
    import os
    import time
    import tifffile as tf

    print('Make sure that the path to the folder only has the files that you want to'\
          ' merge, \nand only one filetype (either exr or tif)\n')

    flder = input('Please input the path: ')
    prefix_name = input('please input the final merged filename prefix: ')
    image_type = None
    while image_type != 'exr' and image_type != 'tif':
        image_type = input('are the files tif or exr?')
        image_type = image_type.lower()