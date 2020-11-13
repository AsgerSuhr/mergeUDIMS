
def combineMergeUdims(prefix_name, flder_path, image_type, midValue):
    flder_path = Path(flder_path)
    flder = os.listdir(flder_path)
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
            im = cv2.imread(str(flder_path / item[0]), -1)
        elif image_type == 'exr':
            im = cv2.imread(str(flder_path / item[0]), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
        imarray = np.array(im)
        for i in item[1:]:
            if image_type == 'tif':
                im2 = cv2.imread(str(flder_path / i), -1)
            elif image_type == 'exr':
                im2 = cv2.imread(str(flder_path / i), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
            imarray2 = np.array(im2)

            fnd = np.where(imarray2 != midValue)

            lst = []
            for nr, i in enumerate(fnd[0]):
                lst.append([i, fnd[1][nr]])


            for i in lst:
                var = imarray2[i[0]][i[1]]
                imarray[i[0]][i[1]] = var
            print(i)

        if image_type == 'tif':
            try:
                saving_name = '%s_%s%s' % (prefix_name, key, '.tif')
                tf.imsave(str(flder_path / saving_name), imarray, compress=0)
            except Exception as err:
                print(err)
        elif image_type == 'exr':
            try:
                saving_name = '%s_%s%s' % (prefix_name, key, '.exr')
                cv2.imwrite(str(flder_path / saving_name), imarray)
            except Exception as err:
                print(err)
        print('succesfully created file: ', prefix_name + '_' + key)
        print('continueing...')
    input('Done')


if __name__ == '__main__':

    # Python 3.7+

    import subprocess
    try:
        import cv2
        import numpy as np
        import tifffile as tf
    except ModuleNotFoundError:
        subprocess.check_call(['python', '-m', 'pip', 'install', 'opencv-python'])
        subprocess.check_call(['python', '-m', 'pip', 'install', 'numpy'])
        subprocess.check_call(['python', '-m', 'pip', 'install', 'tiffile'])
        import numpy as np
        import tifffile as tf
        import cv2
    from pathlib import Path
    import time
    import os
    import re

    print('Make sure that the path to the folder only has the files that you want to'\
          ' merge, \nand only one filetype (either exr or tif)\n')

    flder_path = str(Path(input('Please input the path: ')))
    flder = os.listdir(flder_path)
    prefix_name = input('please input the final merged filename prefix: ')
    image_type = None
    while image_type != 'exr' and image_type != 'tif':
        image_type = input('are the files tif or exr?')
        image_type = image_type.lower()

    midValue = 10.0
    while midValue > 1.0 or midValue < 0.0:
        midValue = input('what is the mid value [please input float value between 0 - 1]: ')
        midValue = float(midValue)

    combineMergeUdims(prefix_name, flder, image_type, midValue)
