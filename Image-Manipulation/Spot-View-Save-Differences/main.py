from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os

from PIL import Image
import json


def spot_dif(first_img, second_img, size) -> list[tuple[int, int]]:
    difs = []
    for x in range(size[0]):
        for y in range(size[1]):
            if first_img[x, y] != second_img[x, y]:
                difs.append((x, y))
    print(f"{len(difs)} differences spoted !")
    """
    for coor in difs:
        print(f"x = {coor[0]} | y = {coor[1]}\n")
    """
    return difs


def show_dif(difs, first_img, size) -> None:
    new_img = Image.new(
        mode='RGBA',
        size=size
    )
    new_img_px = new_img.load()
    for x in range(size[0]):
        for y in range(size[1]):
            if first_img[x, y][3] - 150 < 0:
                opacity = 0
            else:
                opacity = first_img[x, y][3] - 150
            new_img_px[x, y] = (
                first_img[x, y][0],
                first_img[x, y][1],
                first_img[x, y][2],
                opacity
            )

    for dif in difs:
        new_img_px[dif[0], dif[1]] = (255, 0, 0, 255)
    else:
        new_img.show()


def save_dif(_diffs: list[tuple[int, int]], first_image: str, second_image: str) -> None:
    dif_json = {
        "differences": _diffs.sort()
    }

    file_name = f"differences-{first_image}-{second_image}.json"

    with open(file_name, 'w') as file:
        json.dump(dif_json, file)
    print(f"{file_name} created !")


# tkinter window to select the images
window = Tk()
window.geometry("500x300")
window.resizable(False, False)

first_image_label = ""
second_image_label = ""


def select_image():
    global first_image_path
    first_image_path = filedialog.askopenfilename(
        initialdir=os.getcwd(),
        title="Select first image",
        filetypes=(("png files", "*.png"), ("jpg files", "*.jpg"), ("jpeg files", "*.jpeg"))
    )
    first_image_label.config(text=first_image_path)


def select_image2():
    global second_image_path
    second_image_path = filedialog.askopenfilename(
        initialdir=os.getcwd(),
        title="Select second image",
        filetypes=(("png files", "*.png"), ("jpg files", "*.jpg"), ("jpeg files", "*.jpeg"))
    )
    second_image_label.config(text=second_image_path)


def start():
    if first_image_path == "" or second_image_path == "":
        messagebox.showerror("Error", "Please select two images.")
    else:
        os.system(f"python3 main.py {first_image_path} {second_image_path}")
        quit_window()


def quit_window():
    window.destroy()


def image_path_window_selection(title: str) -> list[str]:
    global first_image_label
    global second_image_label

    window.title(title)

    first_image_label = Label(window, text="First image path")
    first_image_label.pack()

    first_image_button = Button(window, text="Select first image", command=select_image)
    first_image_button.pack()

    second_image_label = Label(window, text="Second image path")
    second_image_label.pack()

    second_image_button = Button(window, text="Select second image", command=select_image2)
    second_image_button.pack()

    start_button = Button(window, text="Start", command=start)
    start_button.pack()

    quit_button = Button(window, text="Quit", command=quit_window)
    quit_button.pack()

    window.mainloop()

    return [first_image_path, second_image_path]


if __name__ == "__main__":

    # while True:
    #    first_file_path = input("""Path of the first image ?
    #    >> """)
    #    second_file_path = input("""Path of the second image ?
    #    >> """)
    first_file_path, second_file_path = image_path_window_selection("Image path selection")
    first_image_name = first_file_path.split("/")[-1]
    second_image_name = second_file_path.split("/")[-1]

    try:
        with Image.open(first_file_path) as img:
            first_img_size = img.size
            first_img_px = img.load()
        with Image.open(second_file_path) as img:
            second_img_size = img.size
            second_img_px = img.load()
    except Exception as e:
        print(f"{e}\n")
        exit(1)

    if first_img_size != second_img_size:
        raise Exception("The two images are not the same size !")

    difs = spot_dif(first_img_px, second_img_px, first_img_size)

    if input("""do you want to display the differences (y/n) ?
        >> """) == "y":
        show_dif(difs, first_img_px, first_img_size)

    if input("""do you want to save the differences in a .json ? (y/n) ?
    (differences.json will be overwrited if it already exist)
        >> """) == "y":
        save_dif(difs, first_image_name, second_image_name)

    input("""Thanks, see you next time !
    Press 'ENTER' to leave.""")
    exit(0)
