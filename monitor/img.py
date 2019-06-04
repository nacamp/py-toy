#!/usr/bin/python3
import sys
import time
from PIL import Image
import tkinter
from multiprocessing import Process

'''
https://blog.iconfinder.com/detecting-duplicate-images-using-python-cb240b05a3b6
https://sangwook.github.io/2014/04/21/detecting-duplicate-images-using-python.html
'''


def dhash(image, hash_size=8):
    # Grayscale and shrink the image in one step.
    image = image.convert('L').resize(
        (hash_size + 1, hash_size),
        Image.ANTIALIAS,
    )

    pixels = list(image.getdata())
    # Compare adjacent pixels.
    difference = []
    for row in range(hash_size):
        for col in range(hash_size):
            pixel_left = image.getpixel((col, row))
            pixel_right = image.getpixel((col + 1, row))
            difference.append(pixel_left > pixel_right)
    # Convert the binary array to a hexadecimal string.
    decimal_value = 0
    hex_string = []
    for index, value in enumerate(difference):
        if value:
            decimal_value += 2 ** (index % 8)
        if (index % 8) == 7:
            hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
            decimal_value = 0
    return ''.join(hex_string)


def compare(img1, img2):
    a = Image.open(img1)
    b = Image.open(img2)
    same_cnt = 0
    diff_cnt = 0
    for i in zip(dhash(a), dhash(b)):
        if i[0] == i[1]:
            same_cnt += 1
        else:
            diff_cnt += 1
    return same_cnt * 100 / (same_cnt + diff_cnt)


def beef():
    for _ in range(25):
        time.sleep(0.2)
        print('\a')


def alert():
    p = Process(target=beef, args=())
    p.start()

    window = tkinter.Tk()
    window.title("Changed1")
    window.geometry("300x150+100+100")
    window.configure(background="blue")
    window.resizable(False, False)
    label = tkinter.Label(window, text="Site changed", background="blue")
    label.pack()
    window.mainloop()


if __name__ == '__main__':
    img1 = sys.argv[1]
    img2 = sys.argv[2]
    # img1 = '/Users/jimmy/test/1.png'
    # img2 = '/Users/jimmy/test/3.png'
    score = compare(img1, img2)
    print("score =", score)
    if compare(img1, img2) < 98:
        alert()
