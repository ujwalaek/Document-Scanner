import cv2
import numpy as np
import utlis
 
webCamFeed = True
pathImage = "1.jpg"
cap = cv2.VideoCapture(0)
cap.set(10,160)
heightImg = 640
widthImg  = 480
 
utlis.initializeTrackbars()
count=0
 
while True:
    if webCamFeed:
        success = cap.read()
        img = cap.read()
    else:
        img = cv2.imread(pathImage)

#resizing the image
    img = cv2.resize(img, (widthImg, heightImg)) 
#creating a blank image for testing and debuging if required
    imgBlank = np.zeros((heightImg,widthImg, 3), np.uint8)
#converting image to gray scale  
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
#adding gaussian blur 
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1) 
#getting track bar values for thresholds
    thres=utlis.valTrackbars()  
#applying canny blur
    imgThreshold = cv2.Canny(imgBlur,thres[0],thres[1])  
    kernel = np.ones((5, 5))
#applying dilation
    imgDial = cv2.dilate(imgThreshold, kernel, iterations=2)  
#applying erossion
    imgThreshold = cv2.erode(imgDial, kernel, iterations=1)   
 
    #finding all contours
#copying image for display purposes
    imgContours = img.copy()  
#copying image for display purposes
    imgBigContour = img.copy()  
#finding all contours
    contours = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  
    hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
#drawing all detected contours
    cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10)  
 
 
    #finding the biggest contour
#finding the biggest contour
    biggest = utlis.biggestContour(contours)  
    maxArea = utlis.biggestContour(contours)
    if biggest.size != 0:
        biggest=utlis.reorder(biggest)
#drawing the biggest contour
        cv2.drawContours(imgBigContour, biggest, -1, (0, 255, 0), 20)  
        imgBigContour = utlis.drawRectangle(imgBigContour,biggest,2)
#preparing points for warp
        pts1 = np.float32(biggest) # PREPARE POINTS FOR WARP
#preparing points for warp
        pts2 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]])  
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
#removing 20 pixels from each side
        imgWarpColored=imgWarpColored[20:imgWarpColored.shape[0] - 20, 20:imgWarpColored.shape[1] - 20]
        imgWarpColored = cv2.resize(imgWarpColored,(widthImg,heightImg))
 
#applying the adaptive 
        imgWarpGray = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY)
        imgAdaptiveThre= cv2.adaptiveThreshold(imgWarpGray, 255, 1, 1, 7, 2)
        imgAdaptiveThre = cv2.bitwise_not(imgAdaptiveThre)
        imgAdaptiveThre=cv2.medianBlur(imgAdaptiveThre,3)
 
#image array for display
        imageArray = ([img,imgGray,imgThreshold,imgContours],
                      [imgBigContour,imgWarpColored, imgWarpGray,imgAdaptiveThre])
 
    else:
        imageArray = ([img,imgGray,imgThreshold,imgContours],
                      [imgBlank, imgBlank, imgBlank, imgBlank])
 
#labels for display
    lables = [["Original","Gray","Threshold","Contours"],
              ["Biggest Contour","Warp Prespective","Warp Gray","Adaptive Threshold"]]
 
    stackedImage = utlis.stackImages(imageArray,0.75,lables)
    cv2.imshow("Result",stackedImage)
 
#save image key when s is pressed
    if cv2.waitKey(1) &amp; 0xFF == ord('s'):
        cv2.imwrite("Scanned/myImage"+str(count)+".jpg",imgWarpColored)
        cv2.rectangle(stackedImage, ((int(stackedImage.shape[1] / 2) - 230), int(stackedImage.shape[0] / 2) + 50),
                      (1100, 350), (0, 255, 0), cv2.FILLED)
        cv2.putText(stackedImage, "Scan Saved", (int(stackedImage.shape[1] / 2) - 200, int(stackedImage.shape[0] / 2)),
                    cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 255), 5, cv2.LINE_AA)
        cv2.imshow('Result', stackedImage)
        cv2.waitKey(300)
        count += 1