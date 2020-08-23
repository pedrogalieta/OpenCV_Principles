import cv2 as cv
import imutils
import numpy as np

def imageClick(event, x, y, flags, param):

    #Check if left mouse button was clicked and stores RGB
    if event == cv.EVENT_LBUTTONDOWN:

        #saves BGR click values
        global bgr
        global click_flag
        bgr = [param[y, x, 0], param[y, x, 1], param[y, x, 2]]
        print("Red:", bgr[2], "Green:", bgr[1], "Blue:", bgr[0], " at X =", x, " and Y =", y)
        click_flag = True

def image_set_color(image):

    #splits image in three different channels
    cb, cg, cr = cv.split(image)

    #creates equal size matrix with every pixel like the selected one
    c2b = np.full((image.shape[0],image.shape[1]), bgr[0])
    c2g = np.full((image.shape[0],image.shape[1]), bgr[1])
    c2r = np.full((image.shape[0],image.shape[1]), bgr[2])

    mask = cv.pow(cv.absdiff(c2b, cb), 2) + cv.pow(cv.absdiff(c2g, cg), 2) + cv.pow(cv.absdiff(c2r, cr), 2)
    th, mask = cv.threshold(mask,169,255,cv.THRESH_BINARY_INV)

    result = cv.merge([cb, cg, cr])
    result[mask != 0] = [0,0,255]
    cv.imshow('Result', result)

    #if image was selected, wait for another click to update window
    if(option == '2'):
        click_flag = False

def setup():

    file = None
    camNumber = None
    print("\nThis code supports 4 different executions. What are you going for?")
    option = input('1 - Image RGB     2 - Image similarities     3 - Video similarities     4 - Webcam similarities: ')

    if (option == '1' or option == '2' or option == '3'):
        file = input('\nFile to be opened: ')
        print('\n')

    elif (option == '4'):
        camNumber = input('\nWebcam number is: ')
        camNumber = int(camNumber)
        print('\n')

    else:
        print("\nOption not avaiable! Try again")
        exit(0)

    return option, file, camNumber


if __name__== "__main__":

    option, file, camNumber = setup()

    #if image was selected
    if(option == '1' or option == '2'):

        image = cv.imread(file)
        click_flag = False

        cv.namedWindow('imageRGB')
        cv.setMouseCallback('imageRGB', imageClick, image)

        while(1):

            cv.imshow('imageRGB', image)
            if(click_flag == True and option == '2'): image_set_color(image)
            if cv.waitKey(20) & 0xFF == 27: break

    #if video was selected
    else:

        #start up streaming and get first frame
        if (option == '3'): vid = cv.VideoCapture(file)
        else: vid = cv.VideoCapture(camNumber)
        ret, frame = vid.read()
        #wait for click to start meshing video
        click_flag = False

        #creates and resizes both windows for better visualization
        cv.namedWindow('videoRGB', cv.WINDOW_NORMAL)
        cv.resizeWindow('videoRGB', 600,600)
        cv.namedWindow('Result', cv.WINDOW_NORMAL)
        cv.resizeWindow('Result', 600,600)
        cv.setMouseCallback('videoRGB', imageClick, frame)

        while(1):

            ret, frame = vid.read()
            #if video still up, keep showing on screen
            if(ret == True):
                cv.imshow("videoRGB", frame)
                if(click_flag == True): image_set_color(frame)
                if cv.waitKey(20) & 0xFF == 27: break

            else: break

        vid.release()

#if esc pressed, finish
cv.destroyAllWindows()
