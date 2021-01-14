import pandas as pd
import cv2

import multiprocessing as mp
import logging
import csv
import os

from click_coord import get_click_coord

dir_path = os.path.dirname(__file__)
data_path = os.path.join(dir_path, 'data')


def process(detect_writer, word_writer, start=0):
    data = pd.read_csv('data_v1.csv')
    paths = data['Image'].to_numpy().tolist()
    labels = data['Label'].to_numpy().tolist()

    total = len(paths)
    print("Total {} images".format(total))

    end = start + 10
    for idx in range(start, end):
        folder = str(idx // 1000)
        folder_path = os.path.join(data_path, folder)
        if idx % 1000 == 0:
            os.mkdir(folder_path)

        print("Process image {:} / {:} : ".format(idx + 1, total))

        path = paths[idx]
        label = labels[idx]

        # Show label divided
        l = label.split()
        present = ' | '.join(l)
        print("\tLabel: ", present)

        # Get coordinates to divide image
        img = cv2.imread(path)
        coords = get_click_coord(path, img.shape[1], img.shape[0])

        # t = multiprocess(img)

        # print(len(coords))
        if len(l) != len(coords):
            print("Labeling fail!")
            continue

        detect_writer.writerow({'Idx': idx, 'Image': path, 'Sep': str(coords)})

        # img = cv2.imread(path)
        coords.append(img.shape[1])
        for i in range(len(l)):
            try:
                sub_img = img[:, coords[i]:coords[i + 1], 1]
                img_file = str(idx) + '_' + str(i) + '_' + l[i] + '.jpg'
                img_path = os.path.join(folder_path, img_file)
                cv2.imwrite(img_path, sub_img)
                word_writer.writerow({"Image": img_path, "Label": l[i]})
            except Exception as ex:
                print(ex)
                continue
    return end


def main(start=0):
    if start == 0:
        detect_f = open('csv/detect.csv', 'w')
        writer_1 = csv.DictWriter(detect_f, fieldnames=['Idx', 'Image', 'Sep'], delimiter=';')
        writer_1.writeheader()

        words_f = open('csv/words.csv', 'w')
        writer_2 = csv.DictWriter(words_f, fieldnames=['Image', 'Label'], delimiter=';')
        writer_2.writeheader()
    else:
        detect_f = open('csv/detect.csv', 'a')
        writer_1 = csv.DictWriter(detect_f, fieldnames=['Idx', 'Image', 'Sep'], delimiter=';')
        words_f = open('csv/words.csv', 'a')
        writer_2 = csv.DictWriter(words_f, fieldnames=['Image', 'Label'], delimiter=';')

    end = process(writer_1, writer_2, start=start)

    detect_f.close()
    words_f.close()
    return end


if __name__ == '__main__':
    f = open('logs.txt', 'r')
    text = f.read()
    f.close()

    s = int(text.split()[-1])
    print(s)

    e = main(start=s)

    f = open('logs.txt', 'a')
    f.write(str(e))
    f.write('\n')
    f.close()
