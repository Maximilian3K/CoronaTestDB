import cv2


video = cv2.VideoCapture(0) 

a = 0

while True:
    a = a + 1
    check, frame = video.read()
    cv2.imshow("Capturing",frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

showPic = cv2.imwrite("filename.jpg",frame)
print(showPic)

video.release()
cv2.destroyAllWindows 