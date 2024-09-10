import subprocess
import os
pipe_root_dir = os.environ.get("pipe_root_dir")
siku_root_dir = os.environ.get("siku_root_dir")
siku_py_dir = os.environ.get("siku_py_dir")
from cnocr import CnOcr
def shf(fdn): subprocess.call(['open', '-R', fdn])
def opf(fdn): subprocess.call(['open', fdn]) #]o

import pyperclip

ocr = CnOcr()



def im2txt(imfdn, th=0.25):
    txt_lst = []
    out = ocr.ocr(imfdn)
    scores = []
    for detect in out:
        if detect['score']<th:
            continue
        detect['position']   # np.array, shape=[4,2]
        txt = detect['text']
        if not txt:
            continue
        txt_lst.append(txt)
        scores.append(detect['score'])
    return txt_lst, scores


def newest_fdn_in_static(folder, howmany=1, suff=''):
    all_files = [[os.path.join(folder, x), os.path.getmtime(os.path.join(folder, x))] for x in os.listdir(folder) if x[0] != '.']
    if suff:
        all_files = [[f,t] for f,t in all_files if f.endswith(suff)]
        
    if howmany==1:
        if not all_files:
            return ''
        latest_fdn = max(all_files, key=lambda x: x[1])[0]
        return latest_fdn
    else:
        latest_fdn = sorted(all_files, key=lambda ft: ft[1], reverse=1)[:howmany]
        latest_fdn = [ft[0] for ft in latest_fdn]
        return latest_fdn
def save_txt(txt, fdirname, insert_head=0):
    if not insert_head:
        with open(fdirname, 'w') as file:
            file.write(txt)
    else:
        with open(fdirname, 'r+') as file:
            content = file.read()
            file.seek(0, 0)
            file.write(txt + '\n' + content)


def tmp_cvt_name():

    imfdn = newest_fdn_in_static(siku_root_dir, suff='png')

    txts, scores = im2txt(imfdn)
    fn = '_'.join(txts).replace(' ', '_')
    fn2 = f'imgs/{fn}.png'
    tarf = f'/Users/wenqingzheng/Desktop/___0___/vitagpt/{fn2}'
    pyperclip.copy(f'"{fn2}",')

    from PIL import Image
    import numpy as np

    def make_color_transparent(fdn, outfn, color):
        img = Image.open(fdn)
        
        img = img.convert("RGBA")
        
        data = np.array(img)
        
        target_color = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        
        mask = np.all(data[:,:,:3] == target_color, axis=-1)
        
        data[mask, 3] = 0
        
        result = Image.fromarray(data)
        
        result.save(outfn, "PNG")
    
    make_color_transparent(imfdn, tarf, '191B1E')




import os
from PIL import Image

def trim_transparent_left(image):
    width, height = image.size
    left = 0
    for x in range(width):
        if any(image.getpixel((x, y))[3] != 0 for y in range(height)):
            left = x
            break
    if left > 0:
        return image.crop((left, 0, width, height))
    return image

def process_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.png'):
            file_path = os.path.join(folder_path, filename)
            try:
                with Image.open(file_path) as img:
                    if img.mode != 'RGBA':
                        img = img.convert('RGBA')
                    
                    trimmed_img = trim_transparent_left(img)
                    
                    if trimmed_img.size != img.size:
                        trimmed_img.save(file_path, 'PNG')
            except Exception as e:
                pass


if __name__=='__main__':
    
    # process_folder('/Users/wenqingzheng/Desktop/___0___/vitagpt/imgs')

    tmp_cvt_name()
