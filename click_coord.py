from tkinter import *
from PIL import Image, ImageTk


def get_click_coord(img_path, width, height):
    def print_coords(event):
        # outputting x and y coords to console
        coords.append(event.x)
        print(event.x, end=" ")

    root = Tk()
    size = str(width) + 'x' + str(height)
    root.geometry(size)
    coords = [0]

    # setting up a tkinter canvas with scrollbars
    frame = Frame(root, bd=2, relief=SUNKEN)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    # x_scroll = Scrollbar(frame, orient=HORIZONTAL)
    # x_scroll.grid(row=1, column=0, sticky=E + W)
    # y_scroll = Scrollbar(frame)
    # y_scroll.grid(row=0, column=1, sticky=N + S)
    # canvas = Canvas(frame, bd=0, xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set)
    canvas = Canvas(frame, bd=0)
    canvas.grid(row=0, column=0, sticky=N + S + E + W)
    # x_scroll.config(command=canvas.xview)
    # y_scroll.config(command=canvas.yview)
    frame.pack(fill=BOTH, expand=1)

    img = ImageTk.PhotoImage(Image.open(img_path))
    canvas.create_image(0, 0, image=img, anchor="nw")
    canvas.config(scrollregion=canvas.bbox(ALL))

    # mouseclick event
    canvas.bind("<Button 1>", print_coords)

    root.mainloop()

    print()
    return coords


if __name__ == '__main__':
    results = get_click_coord('/home/vegeta/Downloads/TestOCR/data/0_0_BRIGGS.jpg')
    print(results)
