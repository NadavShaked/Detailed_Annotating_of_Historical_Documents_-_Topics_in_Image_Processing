from numpy import *
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfile
from PIL import ImageTk, Image, ImageGrab
from numpy import deg2rad, cos, sin, matmul

root = Tk()
root.title('Kim')
root.geometry('800x600')

w = 1600
h = 800
x = w / 2
y = h / 2

my_canvas = Canvas(root, width=w, heigh=h, bg="white")
my_canvas.pack(pady=20)

img = PhotoImage(file="img.png")    #todo: delete?

polygon = None
rotatePreVal = 0
resizePreVal = 0
region = (-50, -50, 1000, 800)

addImgBtn = Button(text="Add image", command=lambda: addImage(), anchor=NW)
addImgBtn.configure(width=9, activebackground="#33B5E5", relief=FLAT)
addImgBtn_window = my_canvas.create_window(0, 0, anchor=NW, window=addImgBtn)

addImgBtn = Button(text="Load Polygon", command=lambda: addImage(), anchor=NW)
addImgBtn.configure(width=9, activebackground="#33B5E5", relief=FLAT)
addImgBtn_window = my_canvas.create_window(150, 0, anchor=NW, window=addImgBtn)

quitBtn = Button(text="Quit", command=quit, anchor=NW)
quitBtn.configure(width=5, activebackground="#33B5E5", relief=FLAT)
quitBtn_window = my_canvas.create_window(73, 0, anchor=NW, window=quitBtn)

quitBtn = Button(text="Save", command=lambda: save(), anchor=NW)
quitBtn.configure(width=5, activebackground="#33B5E5", relief=FLAT)
quitBtn_window = my_canvas.create_window(200, 0, anchor=NW, window=quitBtn)


quitBtn = Button(text="Rotate", command=lambda: rotate(None), anchor=NW)
quitBtn.configure(width=5, activebackground="#33B5E5", relief=FLAT)
quitBtn_window = my_canvas.create_window(300, 0, anchor=NW, window=quitBtn)


quitBtn = Button(text="Resize", command=lambda: resize(None), anchor=NW)
quitBtn.configure(width=5, activebackground="#33B5E5", relief=FLAT)
quitBtn_window = my_canvas.create_window(400, 0, anchor=NW, window=quitBtn)


quitBtn = Button(text="+10%", command=lambda: resizePolygonPlus(None), anchor=NW)
quitBtn.configure(width=5, activebackground="#33B5E5", relief=FLAT)
quitBtn_window = my_canvas.create_window(450, 0, anchor=NW, window=quitBtn)


quitBtn = Button(text="-10%", command=lambda: resizePolygonMinus(None), anchor=NW)
quitBtn.configure(width=5, activebackground="#33B5E5", relief=FLAT)
quitBtn_window = my_canvas.create_window(500, 0, anchor=NW, window=quitBtn)


class Polygon(object):
    def prepare_points(self, poly_points):
        print("prepare_points")
        i = 0
        list_x = []
        list_y = []
        for point in poly_points:
            if i % 2 == 0:
                list_x.append(point)
            else:
                list_y.append(point)
            i += 1
        self.points.append(list_x)
        self.points.append(list_y)
        for i in self.points:
            print(*i)

    def calc_signed_area(self):
        print("calc_signed_area")
        wrap_around = 0
        for i in range(int(self.point_count)):
            if i + 1 == self.point_count:
                wrap_around = 0
            else:
                wrap_around = i + 1
            self.a += self.points[0][i] * self.points[1][wrap_around] - self.points[0][wrap_around] * self.points[1][i]
            print(str(i) + ": " + str(self.a) + ", (x_i, y_i): (" + str(self.points[0][i]) + ", " + str(
                self.points[1][i]) + "), (x_i+1, y_i+1): (" + str(self.points[0][wrap_around]) + ", " + str(
                self.points[1][wrap_around]) + ")")

        self.a = self.a * 0.5
        print("A = " + str(self.a))

    def calc_centroid(self):
        print("calc_centroid")
        self.calc_signed_area()
        print("calc_centroid")

        wrap_around = 0
        for i in range(int(self.point_count)):
            if i + 1 == self.point_count:
                wrap_around = 0
            else:
                wrap_around = i + 1
            self.centroid[0] += (self.points[0][i] + self.points[0][wrap_around]) * (
                        self.points[0][i] * self.points[1][wrap_around] - self.points[0][wrap_around] * self.points[1][
                    i])  # x
            self.centroid[1] += (self.points[1][i] + self.points[1][wrap_around]) * (
                        self.points[0][i] * self.points[1][wrap_around] - self.points[0][wrap_around] * self.points[1][
                    i])  # y
            print(str(i) + ": (x, y): (" + str(self.centroid[0]) + ", " + str(self.centroid[1]) + ")")
        self.centroid[0] = self.centroid[0] * (1 / (6 * self.a))
        self.centroid[1] = self.centroid[1] * (1 / (6 * self.a))

        temp_x = []
        temp_y = []

        for i in range(int(self.point_count)):
            temp_x.append(self.centroid[0])
            temp_y.append(self.centroid[1])

        self.centroid_2xn.append(temp_x)
        self.centroid_2xn.append(temp_y)

        print("(x, y): (" + str(self.centroid[0]) + ", " + str(self.centroid[1]) + ")")
        print("centroid 2xn: " + str(self.centroid_2xn))

    def apply_rotate(self, new_points):
        print("apply_rotate")
        apply_points = []
        j = 0
        for i in range(int(self.point_count)):
            apply_points.append(new_points[j % 2][i])
            j += 1
            apply_points.append(new_points[j % 2][i])
            j += 1

        print(tuple(apply_points))
        self.canvas.coords(self.polygon, tuple(apply_points))

    def calculate_rotate(self, degree):
        print("calculate_rotate")
        degree = deg2rad(degree)
        R = []
        r1 = [cos(degree), -sin(degree)]
        r2 = [sin(degree), cos(degree)]
        R.append(r1)
        R.append(r2)

        print("R: " + str(R))

        sub_x = []
        sub_y = []
        sub = []

        for i in range(int(self.point_count)):
            sub_x.append(self.points[0][i] - self.centroid_2xn[0][i])
            sub_y.append(self.points[1][i] - self.centroid_2xn[1][i])
        sub.append(sub_x)
        sub.append(sub_y)

        print("sub: " + str(sub))

        P = (matmul(R, sub))

        print("P: " + str(P))

        add_x = []
        add_y = []

        for i in range(int(self.point_count)):
            add_x.append(P[0][i] + self.centroid_2xn[0][i])
            add_y.append(P[1][i] + self.centroid_2xn[1][i])
        self.rotP.insert(0, add_x)
        self.rotP.insert(1, add_y)

        print("rotP:")
        for i in range(int(self.point_count)):
            print("x " + str(i) + ": " + str(self.rotP[0][i]))
            print("y " + str(i) + ": " + str(self.rotP[1][i]))
        return self.rotP

    def rotate(self, degree, canvas_obj=None, poly_obj=None):
        print("rotate")
        if canvas_obj != None and poly_obj != None:
            self.canvas = canvas_obj
            self.polygon = poly_obj
            self.poly_points = self.canvas.coords(self.polygon)
            self.point_count = len(self.poly_points) / 2
            self.prepare_points(self.poly_points)
            self.calc_centroid()
        self.apply_rotate(self.calculate_rotate(degree))

    def __init__(self, canvas_obj=None, poly_obj=None):
        self.a = 0  # polygon's signed area
        self.centroid = [0, 0]  # polygon's centroid x and y
        self.centroid_2xn = []  # centroid 2xn matrix for dot product
        self.points = []  # polygon's points in 2xn matrix
        self.point_count = 0  # number of points in polygon
        self.rotP = []  # polygon's new rotated points in 2xn matrix
        self.polygon = None  # polygon object
        self.canvas = None  # canvas object
        if canvas_obj != None and poly_obj != None:
            self.canvas = canvas_obj
            self.polygon = poly_obj
            self.poly_points = self.canvas.coords(self.polygon)
            self.point_count = len(self.poly_points) / 2
            self.prepare_points(self.poly_points)
            self.calc_centroid()


def createPolygon(event):
    global polygon
    polygon = my_canvas.create_polygon([150, 75, 225, 0, 300, 75, 225, 150], outline='gray', fill='gray', width=2)
    print(polygon)


def addImage():
    Tk().withdraw()
    filename = askopenfilename(title="Choose a file", filetypes=[('image files', ('.png', '.jpg'))])
    img = Image.open(filename)
    uploadedImg = ImageTk.PhotoImage(img)
    root.geometry(f"{uploadedImg.width()}x{uploadedImg.height() + 25}")
    my_canvas.image = uploadedImg  # <--- keep reference of your image
    r = my_canvas.create_image(0, 25, anchor=NW, image=uploadedImg)
    my_canvas.pack()


def rotate(event):
    if polygon is not None:
        sl = Tk()
        sl.title('rotate')
        sl.geometry('200x50')
        rotate_canvas = Canvas(sl, width=w, heigh=h, bg="white")
        slide = Scale(rotate_canvas, from_=0, to=360, orient=HORIZONTAL, command=rotatePolygon)
        rotate_canvas.pack()
        slide.pack()
        sl.mainloop()


def rotatePolygon(val):
    if polygon is not None:
        global rotatePreVal
        rotateVal = int(val) - rotatePreVal
        poly = Polygon(my_canvas, polygon)
        poly.rotate(rotateVal)
        rotatePreVal = int(val)
        my_canvas.pack()


def resize(event):
    if polygon is not None:
        sl = Tk()
        sl.title('resize')
        sl.geometry('200x50')
        rotate_canvas = Canvas(sl, width=w, heigh=h, bg="white")
        slide = Scale(rotate_canvas, from_=0, to=300, orient=HORIZONTAL, command=resizePolygon)
        slide.set(100)
        rotate_canvas.pack()
        slide.pack()
        sl.mainloop()


def resizePolygon(val):
    if polygon is not None:
        global region
        global resizePreVal
        resizePreVal = int(val) - int(resizePreVal)
        x1, y1, x2, y2 = region
        canvas_breadth = max(x2 - x1, y2 - y1)
        _region = region
        region = tuple(float(x) for x in _region)
        x1, y1, x2, y2 = region
        breadth = max(x2 - x1, y2 - y1)
        if breadth == 0:
            return
        r = float(val) / 100
        if r < 0.01 or r > 30:
            return
        s = r / (float(breadth) / canvas_breadth)
        my_canvas.scale(polygon, 0, 0, s, s)
        nregion = tuple(x * r for x in region)
        region = nregion
        resizePreVal = int(val)


def resizePolygonPlus(event):
    if polygon is not None:
        global region
        global resizePreVal
        x1, y1, x2, y2 = region
        canvas_breadth = max(x2 - x1, y2 - y1)
        _region = region
        region = tuple(float(x) for x in _region)
        x1, y1, x2, y2 = region
        breadth = max(x2 - x1, y2 - y1)
        if breadth == 0:
            return
        r = float(110) / 100
        if r < 0.01 or r > 30:
            return
        s = r / (float(breadth) / canvas_breadth)
        my_canvas.scale(polygon, 0, 0, s, s)
        nregion = tuple(x * r for x in region)
        region = nregion


def resizePolygonMinus(event):
    if polygon is not None:
        global region
        global resizePreVal
        x1, y1, x2, y2 = region
        canvas_breadth = max(x2 - x1, y2 - y1)
        _region = region
        region = tuple(float(x) for x in _region)
        x1, y1, x2, y2 = region
        breadth = max(x2 - x1, y2 - y1)
        if breadth == 0:
            return
        r = float(90) / 100
        if r < 0.01 or r > 30:
            return
        s = r / (float(breadth) / canvas_breadth)
        my_canvas.scale(polygon, 0, 0, s, s)
        nregion = tuple(x * r for x in region)
        region = nregion


def left(event):
    if polygon is not None:
        x = -10
        y = 0
        my_canvas.move(polygon, x, y)


def right(event):
    if polygon is not None:
        x = 10
        y = 0
        my_canvas.move(polygon, x, y)


def down(event):
    if polygon is not None:
        x = 0
        y = 10
        my_canvas.move(polygon, x, y)


def up(event):
    if polygon is not None:
        x = 0
        y = -10
        my_canvas.move(polygon, x, y)


def save():
    x2 = root.winfo_rootx() + my_canvas.winfo_x()
    y2 = root.winfo_rooty() + my_canvas.winfo_y() + 25
    x1 = x2 + my_canvas.winfo_width()
    y1 = y2 + my_canvas.winfo_height() - 25
    f = asksaveasfile(mode='w', title="Save As", filetypes=[('.jpg', '.jpg')])
    if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
        return
    ImageGrab.grab().crop((x2, y2, x1, y1)).save(f)
    f.close()


root.bind("<Left>", left)
root.bind("<Right>", right)
root.bind("<Up>", up)
root.bind("<Down>", down)
root.bind("<c>", createPolygon)
root.bind("<r>", rotate)
root.bind("<s>", resize)
root.bind("<p>", resizePolygonPlus)
root.bind("<m>", resizePolygonMinus)

root.mainloop()
