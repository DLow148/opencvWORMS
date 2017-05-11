#Edited by Derek Low
import numpy as np
import cv2
import os, sys
from Tkinter import *
from tkFileDialog import askopenfilename
from PIL import Image, ImageTk

# Read points from text file
def readPoints(path) :
    # Create an array of points.
    points = [];
    # Read points
    with open(path) as file :
        for line in file :
            x, y = line.split()
            points.append((int(x), int(y)))

    return points
#find the midpoints between the chosen pointed for delaunay Triangulation
#we will perform delaunay triangulation to find corresponding points for morph
#based on this
def averagePoints(p1, p2):
    for i in xrange(0, len(points1)):
        x = ( 1 - alpha ) * points1[i][0] + alpha * points2[i][0]
        y = ( 1 - alpha ) * points1[i][1] + alpha * points2[i][1]
        points.append((x,y))

# Apply affine transform calculated using srcTri and dstTri to src and
# output an image of size.
def applyAffineTransform(src, srcTri, dstTri, size) :

    # Given a pair of triangles, find the affine transform.
    warpMat = cv2.getAffineTransform( np.float32(srcTri), np.float32(dstTri) )

    # Apply the Affine Transform just found to the src image
    dst = cv2.warpAffine( src, warpMat, (size[0], size[1]), None, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101 )

    return dst


# Warps and alpha blends triangular regions from img1 and img2 to img
def morphTriangle(img1, img2, img, t1, t2, t, alpha) :

    # Find bounding rectangle for each triangle
    r1 = cv2.boundingRect(np.float32([t1]))
    r2 = cv2.boundingRect(np.float32([t2]))
    r = cv2.boundingRect(np.float32([t]))


    # Offset points by left top corner of the respective rectangles
    t1Rect = []
    t2Rect = []
    tRect = []


    for i in xrange(0, 3):
        tRect.append(((t[i][0] - r[0]),(t[i][1] - r[1])))
        t1Rect.append(((t1[i][0] - r1[0]),(t1[i][1] - r1[1])))
        t2Rect.append(((t2[i][0] - r2[0]),(t2[i][1] - r2[1])))


    # Get mask by filling triangle
    mask = np.zeros((r[3], r[2], 3), dtype = np.float32)
    cv2.fillConvexPoly(mask, np.int32(tRect), (1.0, 1.0, 1.0), 16, 0);

    # Apply warpImage to small rectangular patches
    img1Rect = img1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]
    img2Rect = img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]]

    size = (r[2], r[3])
    warpImage1 = applyAffineTransform(img1Rect, t1Rect, tRect, size)
    warpImage2 = applyAffineTransform(img2Rect, t2Rect, tRect, size)

    # Alpha blend rectangular patches
    imgRect = alpha * warpImage2
    #imgRect = (1.0 - alpha) * warpImage1 + alpha * warpImage2

    # Copy triangular region of the rectangular patch to the output image
    img[r[1]:r[1]+r[3], r[0]:r[0]+r[2]] = img[r[1]:r[1]+r[3], r[0]:r[0]+r[2]] * ( 1 - mask ) + imgRect * mask

#DELAUNAY BUTTONS
#on Button Press, open a file and record that pixel, and add a green dot to the button press
def coordsToText(event):
    python_hotPink = "#FF69B4"
    x1, y1 = (event.x-3), (event.y -3)
    x2, y2 = (event.x+3), (event.y +3)
    canvas.create_oval(x1,y1,x2,y2, fill = python_hotPink)
    f = open(File + ".txt","a")
    f.write(str(event.x) + " " +str(event.y)+"\n")
    f.close()

#helper function so we can bind to a button on the interface
def coordsToTextHelper():
    canvas.bind("<Button 1>", coordsToText)
    resetButton = Button(root, text = "Reset", command = textResetter)
    resetButton.pack()

#reset both the associated text file and the canvas to set new points
def textResetter():
    os.remove(File+".txt")
    canvas.delete("all")
    canvas.create_image(0,0,image=img,anchor="nw")

#delete the lists for Bezier Curve and points associated with it
def deleteXYS():
    del xys[:]
    del points[:]
    canvas.delete("all")
    canvas.create_image(0,0,image=img,anchor="nw")

'''def zoomIn():
    image1 = Image.open(File)
    image1 = image1.resize((imgx * 5, imgy * 5), Image.ANTIALIAS) #The (250, 250) is (height, width)
    imgResize = ImageTk.PhotoImage(image1)
    canvas.create_image(0,0,image = imgResize, anchor = "nw")'''

#BEZIER CURVE
#Here's where we do all the Bezier curve stuff. Start off by generating the global array that will be used
xys = [] #this is where the xys values will be stored for the bezier curve production
points = []

#This portion is the user-end portion that allows the user to select points and view the points they've selected
def pointSelectBezier(event):
    python_yellow = "#FFD700"
    x1, y1 = (event.x -3), (event.y -3)
    x2, y2 = (event.x +3), (event.y +3)
    canvas.create_oval(x1,y1,x2,y2, fill = python_yellow)
    xys.append([event.x,event.y])

#This portion will take the points created by the Bezier functions and draw the actual curve
def bezierDrawing():
    ts = [t/100.0 for t in range(101)]
    bezier = make_bezier(xys)
    points.extend(bezier(ts))
    print (points)
    for i in points:
        python_white = "#FFFFFF"
        x , y = int(i[0]), int(i[1])
        print x
        x1, y1 = (x -1),(y-1)
        x2, y2 = (x +1),(y+1)
        canvas.create_oval(x1,y1,x2,y2, fill = python_white)
    #TO DO: Draw Points here onto the campus!

def bezierHelper():
    canvas.bind("<Button 1>", pointSelectBezier)
    makeBezierButton = Button (root, text = "Make Bezier Curve!", command = bezierDrawing)
    makeBezierButton.pack()
    makeBezierDeleter = Button (root, text = "Reset Bezier Points", command = deleteXYS)
    makeBezierDeleter.pack()


#Functions for calculating the points of Bezier curves that I found on the internet at
#http://stackoverflow.com/questions/246525/how-can-i-draw-a-bezier-curve-using-pythons-pil
def make_bezier(xys):
    # xys should be a sequence of 2-tuples (Bezier control points)
    n = len(xys)
    combinations = pascal_row(n-1)
    def bezier(ts):
        # This uses the generalized formula for bezier curves
        # http://en.wikipedia.org/wiki/B%C3%A9zier_curve#Generalization
        result = []
        for t in ts:
            tpowers = (t**i for i in range(n))
            upowers = reversed([(1-t)**i for i in range(n)])
            coefs = [c*a*b for c, a, b in zip(combinations, tpowers, upowers)]
            result.append(
                tuple(sum([coef*p for coef, p in zip(coefs, ps)]) for ps in zip(*xys)))
        return result
    return bezier

def pascal_row(n):
    # This returns the nth row of Pascal's Triangle
    result = [1]
    x, numerator = 1, n
    for denominator in range(1, n//2+1):
        # print(numerator,denominator,x)
        x *= numerator
        x /= denominator
        result.append(x)
        numerator -= 1
    if n&1 == 0:
        # n is even
        result.extend(reversed(result[:-1]))
    else:
        result.extend(reversed(result))
    return result
def saveImage():
    canvas.postscript(file="NewWorms.eps")

#quit window to move on to the Triangulation
def exitWindow():
    root.destroy()

if __name__ == '__main__' :
    root = Tk()

    #adding the image, then create frame and canvas based on image size
    File = askopenfilename(parent = root, initialdir="C:/users/Derek/Desktop/WORMS PROJECT",title = 'Choose an image')
    img=ImageTk.PhotoImage(Image.open(File))
    root.img = img
    imgx = img.width()
    imgy = img.height()

    #Set up Tkinter canvas and frame based on size of image
    frame = Frame(root, bd=2, relief=SUNKEN)
    canvas = Canvas(frame, bd=0,width = imgx, height=imgy)
    frame.pack()
    canvas.pack()
    canvas.create_image(0,0,image=img,anchor="nw")

#INITIAL GUI BUTTONS
    #This buton will allow you to select points and add them to a text file, and will also give you a reset button to
    #reset the points if need be
    pointButton = Button(root,text = "Set Points for Triangulation!", command = coordsToTextHelper)
    pointButton.pack(side=LEFT)

    #This button will allow you to place points for Bezier Curve selection
    bezierButton = Button(root,text = "Set Points for Bezier!",command = bezierHelper)
    bezierButton.pack(side=LEFT)

    #This button will save the image currently on the GUI
    printButton = Button(root, text = "Save Image", command = saveImage)
    printButton.pack(side=LEFT)

    #This button will close the window, proceeding with the triangulation based on the files and points selected
    exitButton = Button(root,text = "Run Triangulation!", command = exitWindow)
    exitButton.pack(side=LEFT)

    #Run the main point-selection loop
    root.mainloop()

#RUN THE IMAGE MORPHING
    filename1 = 'flatwormEX1.jpg'
    filename2 = File
    #By setting coordAlpha to 0 and pixelAlpha to 1, you use actual pixel colors of file 2
    #and fit it to the shape of file 1
    pixelAlpha = 1.0
    coordAlpha = 0.0
    # Read images
    img1 = cv2.imread(filename1);
    img2 = cv2.imread(filename2);

    # Convert Mat to float data type
    img1 = np.float32(img1)
    img2 = np.float32(img2)

    # Read array of corresponding points
    points1 = readPoints(filename1 + '.txt')
    points2 = readPoints(filename2 + '.txt')
    points = [];

    # Compute weighted average point coordinates
    for i in xrange(0, len(points1)):
        x = ( 1 - coordAlpha ) * points1[i][0] + coordAlpha * points2[i][0]
        y = ( 1 - coordAlpha ) * points1[i][1] + coordAlpha * points2[i][1]
        #x = ( 1 - alpha ) * points1[i][0] + alpha * points2[i][0]
        #y = ( 1 - alpha ) * points1[i][1] + alpha * points2[i][1]
        points.append((x,y))

    print (points)

    # Allocate space for final output
    imgMorph = np.zeros(img1.shape, dtype = img1.dtype)

    # Read triangles from tri.txt
    with open("wormtri.txt") as file :
        for line in file :
            x,y,z = line.split()

            x = int(x)
            y = int(y)
            z = int(z)
            print(x,y,z)
            t1 = [points1[x], points1[y], points1[z]]
            t2 = [points2[x], points2[y], points2[z]]
            t = [ points[x], points[y], points[z] ]

            # Morph one triangle at a time.
            morphTriangle(img1, img2, imgMorph, t1, t2, t, pixelAlpha)


    # Display Result
    cv2.imshow("Morphed Worm", np.uint8(imgMorph))
    cv2.waitKey(0)
