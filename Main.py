from tkinter import Button, Canvas, Label, StringVar, Tk, N, S, W, E
import pyvolume
from PIL import Image, ImageTk


##### CONFIG

CANVAS_WIDTH = 250
CANVAS_HEIGHT = 250

UPDATE_INTERVAL = 100

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


saveCounter = 0


def savePos(event):
    global lastX, lastY
    lastX, lastY = event.x, event.y

    global saveCounter
    saveCounter = saveCounter + 1


def getDrawnPixelCount():
    width = int(canvas["width"])
    height = int(canvas["height"])
    drawnCount = 0

    test = 0

    for x in range(width):
        for y in range(height):
            ids = canvas.find_overlapping(x, y, x, y)
            if len(ids) > 0:
                test = test + 1
                index = ids[-1]
                color = canvas.itemcget(index, "fill")
                if color.upper() == "BLACK":
                    drawnCount = drawnCount + 1

    return drawnCount


def updateVolume():
    pixel = getDrawnPixelCount()

    canvasArea = CANVAS_HEIGHT * CANVAS_WIDTH
    percentage = 100 / canvasArea * pixel

    volumeContent.set(str(round(percentage)) + "%")
    pyvolume.custom(percent=round(percentage))


def addLine(event):
    canvas.create_line((lastX, lastY, event.x, event.y), fill=brushColor, width=5)
    savePos(event)

    global saveCounter
    if saveCounter > UPDATE_INTERVAL:
        updateVolume()
        saveCounter = 0



def addCanvas():
    canvas.pack()

    canvas.grid(column=0, row=0, sticky=(N, W, E))
    canvas.bind("<Button-1>", savePos)
    canvas.bind("<B1-Motion>", addLine)


def addButtons():
    drawButton.grid(column=0, row=1, sticky=(N, E, S))
    eraseButton.grid(column=0, row=1, sticky=(N, S))


def addLabel():
    volumeLabel.grid(column=0, row=1, sticky=(N, W, S))


if __name__ == "__main__":
    addCanvas()
    addButtons()
    addLabel()
    window.mainloop()
