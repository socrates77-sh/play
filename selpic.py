import os
import imghdr
from tkinter import *
from PIL import Image, ImageTk
import shutil

SHOW_WIDTH = 1200
SHOW_HEIGHT = 800
MIN_HEIGHT = 600

VERSION = 'v1.1'


# def search_img(imgdir):
#     img_list = []
#     for imgfile in os.listdir(imgdir):
#         imgfile_full = os.path.join(imgdir, imgfile)
#         if (os.path.isfile(imgfile_full)):
#             if (imghdr.what(imgfile_full)):
#                 pil_image = Image.open(imgfile_full)
#                 w0, h0 = pil_image.size
#                 pil_image.close()
#                 if h0 >= MIN_HEIGHT:
#                     img_list.append(imgfile_full)
#                     print(imgfile_full)
#                 else:
#                     move_img(imgdir, '2', imgfile)
#                     print('%s [skip]' % imgfile)
#             else:
#                 move_img(imgdir, '2', imgfile)
#                 print('%s [skip]' % imgfile)
#     return img_list

def search_img(imgdir):
    img_list = []
    for imgfile in os.listdir(imgdir):
        imgfile_full = os.path.join(imgdir, imgfile)
        if os.path.isfile(imgfile_full) and (not imgfile_full.endswith('.py')):
            try:
                w0, h0 = (0, 0)
                pil_image = Image.open(imgfile_full)
                w0, h0 = pil_image.size
                pil_image.close()
            except Exception as e:
                # pil_image.close()
                print(e)
                # move_img(imgdir, '2', imgfile)

            if h0 >= MIN_HEIGHT:
                img_list.append(imgfile_full)
                print(imgfile_full)
            else:
                move_img(imgdir, '2', imgfile)
                print('%s [bad]' % imgfile_full)
    return img_list


def move_img(imgdir, destdir, imgfile):
    target_dir = os.path.join(imgdir, destdir)
    os.makedirs(target_dir, exist_ok=True)
    shutil.move(imgfile, target_dir)
    # print(imgfile)


def resize(w0, h0, w_box, h_box, pil_image):
    f1 = 1.0 * w_box / w0  # 1.0 forces float division in Python2
    f2 = 1.0 * h_box / h0
    factor = min([f1, f2])
    if factor < 1.0:
        width = int(w0 * factor)
        height = int(h0 * factor)
        return factor, pil_image.resize((width, height), Image.ANTIALIAS)
    else:
        return 1, pil_image


class ImageShow(Frame):

    def __init__(self, parent=None, picdir='.', **args):
        Frame.__init__(self, parent, **args)
        self.lbl = Label(self)
        # initial size: lines,chars
        self.lbl.config(height=1, anchor='w')
        self.lbl.pack(expand=YES, fill=BOTH)
        self.canvas = Canvas(
            self, bg='gray', height=SHOW_HEIGHT, width=SHOW_WIDTH)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=YES)

        self.pack(expand=YES, fill=BOTH)
        self.files = search_img(picdir)
        self.drawn = None
        self.num = 0
        self.parent = parent
        self.picdir = picdir
        self.w0 = 0
        self.h0 = 0
        self.w1 = 0
        self.h1 = 0
        self.factor = 1.0
        self.lbl.bind("<Right>", self.onRightKey)
        self.lbl.bind("<Left>", self.onLeftKey)
        self.lbl.bind("<Key-space>", self.onSpaceKey)
        self.lbl.bind("<Delete>", self.onDelKey)
        self.lbl.focus()
        self.drawImage()
        # self.num = 1

    def onRightKey(self, event):
        if self.num == len(self.files) - 1:
            self.num = 0
            self.bell()
        else:
            self.num += 1
        self.drawImage()
        # print('right', self.num)

    def onLeftKey(self, event):
        if self.num == 0:
            self.num = len(self.files) - 1
            self.bell()
        else:
            self.num -= 1
        self.drawImage()
        # print('left', self.num)

    def onSpaceKey(self, event):
        # self.bell()
        move_img(self.picdir, '1', self.files[self.num])
        del self.files[self.num]
        if self.num == len(self.files):
            self.num -= 1
        self.drawImage()
        # print('return', self.num)

    def onDelKey(self, event):
        # self.bell()
        move_img(self.picdir, '2', self.files[self.num])
        del self.files[self.num]
        if self.num == len(self.files):
            self.num -= 1
        self.drawImage()
        # print('return', self.num)

    def proc_img(self):
        pil_image = Image.open(self.files[self.num])
        w0, h0 = pil_image.size
        factor, pil_image_resized = resize(
            w0, h0, SHOW_WIDTH, SHOW_HEIGHT, pil_image)
        self.img = ImageTk.PhotoImage(pil_image_resized)
        w1, h1 = pil_image_resized.size
        self.factor = factor
        self.h0 = h0
        self.w0 = w0
        self.h1 = h1
        self.w1 = w1

    # def center_cor(self):
    #     x = (SHOW_WIDTH - self.w1) / 2
    #     y = (SHOW_HEIGHT - self.h1) / 2
    #     return x, y

    def drawImage(self):
        if len(self.files) == 0:
            self.bell()
            self.lbl['text'] = 'Nothing left!'
            sys.exit(1)

        if self.drawn:
            self.canvas.delete(self.drawn)
        # self.img = PhotoImage(file=self.files[self.num])
        self.proc_img()
        # print(factor, w1, h1)
        # x, y = self.center_cor()
        self.drawn = self.canvas.create_image(
            SHOW_WIDTH / 2, SHOW_HEIGHT / 2, image=self.img, anchor=CENTER)
        self.canvas.update()
        self.show_title()

    def show_title(self):
        str_title = '[%d/%d] %dx%d (%d%%) %s ' % (
            self.num + 1, len(self.files), self.w0,
            self.h0, int(self.factor * 100),
            os.path.basename(self.files[self.num]))
        self.lbl['text'] = str_title


def main():
    maindir = os.path.curdir
    # maindir = 'e:\\temp\\gifs'
    # maindir = 'E:\\download\\b'

    win = Tk()
    win.title('selpic %s' % VERSION)
    # win.state("zoomed")
    win.resizable(0, 0)
    ImageShow(parent=win, picdir=maindir)
    win.mainloop()


if __name__ == '__main__':
    main()
