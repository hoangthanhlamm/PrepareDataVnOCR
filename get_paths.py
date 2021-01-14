import os
import codecs

import pandas as pd
from tqdm import tqdm

dir_path = os.path.dirname(__file__)
folders = ['vi_00', 'vi_01']

chars = codecs.open('chars.txt', 'r', 'utf-8').read()
vn_chars = codecs.open('vnchars.txt', 'r', 'utf-8').read()


def get_paths(folder):
    data = []
    cnt = 0
    files = os.listdir(os.path.join(dir_path, folder))
    print("Folder: ", folder)
    for f in tqdm(files):
        # Ignore txt file
        f_type = str(f).count('.txt')
        if f_type:
            continue

        img_path = folder + '/' + str(f)
        txt_path = img_path.replace('.jpg', '.txt')
        try:
            with open(os.path.join(dir_path, txt_path), 'r') as f_out:
                label = f_out.read()
                label = label.upper()

                # Filter image and label with non-word character
                if not label_filter(label):
                    continue
        except FileNotFoundError:
            continue

        data.append([img_path, label])
        cnt += 1
    print("Filter ratio: ", cnt / len(files))
    return data


def label_filter(label):
    vn_check = False
    for c in label:
        # Check invalid character
        if c not in chars:
            return False

        # Check vietnamese character
        if c in vn_chars:
            vn_check = True
    return vn_check


def main():
    data = []
    for folder in folders:
        data.extend(get_paths(folder))

    df = pd.DataFrame(data, columns=['Image', 'Label'])
    df.to_csv(os.path.join(dir_path, 'data_v1.csv'), index=False)


# if __name__ == '__main__':
#     main()
