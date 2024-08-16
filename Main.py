from tkinter import Button, Canvas, Tk, N, S, W, E
from PIL import Image, ImageTk


##### CONFIG

CANVAS_WIDTH = 250
CANVAS_HEIGHT = 250

#####


window = Tk()

canvas = Canvas(window, bg="white", width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bd=1, relief="solid")
brushColor = "black"


def brushColorDraw():
    global brushColor
    brushColor = "black"


def brushColorErase():
    global brushColor
    brushColor = "white"


drawImg = ImageTk.PhotoImage(Image.open("./drawing.png").resize((25, 25), Image.Resampling.LANCZOS))
eraseImg = ImageTk.PhotoImage(Image.open("./eraser.png").resize((25, 25), Image.Resampling.LANCZOS))
drawButton = Button(window, command=brushColorDraw, width=50, height=50, image=drawImg)
eraseButton = Button(window, command=brushColorErase, width=50, height=50, image=eraseImg)


def savePos(event):
    global lastX, lastY
    lastX, lastY = event.x, event.y


def addLine(event):
    canvas.create_line((lastX, lastY, event.x, event.y), fill=brushColor)
    savePos(event)


def addCanvas():
    canvas.pack()

    canvas.grid(column=0, row=0, sticky=(N, W, E))
    canvas.bind("<Button-1>", savePos)
    canvas.bind("<B1-Motion>", addLine)


def addButtons():
    drawButton.place(x=50, y=50)
    drawButton.grid(column=0, row=1, sticky=(N, E, S))

    eraseButton.place(x=50, y=50)
    eraseButton.grid(column=0, row=1, sticky=(N, S))


if __name__ == "__main__":
    addCanvas()
    addButtons()
    window.mainloop()
