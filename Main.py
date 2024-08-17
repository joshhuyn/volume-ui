from tkinter import Button, Canvas, Label, StringVar, Tk, N, S, W, E
import time
import threading
import pyvolume
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


volumeContent = StringVar()
volumeLabel = Label(window, textvariable=volumeContent)


def getDrawnPixelCount():
    width = int(canvas["width"])
    height = int(canvas["height"])
    drawnCount = 0

    for x in range(width):
        for y in range(height):
            ids = canvas.find_overlapping(x, y, x, y)

            if len(ids) > 0:
                fill = canvas.itemcget(ids[-1], "fill").upper()

                if len(ids) > 1 and fill == "WHITE" and canvas.itemcget(ids[-2], "fill").upper() == "BLACK":
                    canvas.delete(ids[-2])

                if fill == "BLACK":
                    drawnCount = drawnCount + 1

    return drawnCount


def updateVolume():
    pixel = getDrawnPixelCount()

    canvasArea = CANVAS_HEIGHT * CANVAS_WIDTH
    percentage = 100 / canvasArea * pixel

    volumeContent.set(str(round(percentage)) + "%")
    pyvolume.custom(percent=round(percentage))


def addLine(event):
    if (brushColor.upper() == "BLACK"):
        canvas.create_oval((event.x, event.y, event.x, event.y), fill=brushColor, outline=brushColor, width=5)
    else:
        ids = canvas.find_overlapping(event.x, event.y, event.x, event.y)
        if len(ids) > 0:
            canvas.delete(ids[-1])


def addCanvas():
    canvas.pack()

    canvas.grid(column=0, row=0, sticky=(N, W, E))
    canvas.bind("<B1-Motion>", addLine)


def addButtons():
    drawButton.grid(column=0, row=1, sticky=(N, E, S))
    eraseButton.grid(column=0, row=1, sticky=(N, S))


def addLabel():
    volumeLabel.grid(column=0, row=1, sticky=(N, W, S))


def frameUpdate():
    while True:
        time.sleep(60 / 1000)
        updateVolume()


if __name__ == "__main__":
    addCanvas()
    addButtons()
    addLabel()

    threading.Thread(target=frameUpdate).start()

    window.mainloop()
