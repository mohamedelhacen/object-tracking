import cv2

tracker = cv2.legacy.TrackerMOSSE_create()
path = input("Enter the path to the video: ")
cap = cv2.VideoCapture(path)
success, frame = cap.read()
bbox = cv2.selectROI("Tracking", frame, False)
tracker.init(frame, bbox)


def drawBox(image, bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(image, (x, y), ((x+w), (y+h)), (255, 0, 255), 3, 3)
    cv2.putText(image, "Tracking", (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)


frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_fps = int(cap.get(cv2.CAP_PROP_FPS))

size = (frame_width, frame_height)
result = cv2.VideoWriter('result.avi',
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         frame_fps, size)

while True:
    timer = cv2.getTickCount()
    success, image = cap.read()
    success, bbox = tracker.update(image)

    if success:
        drawBox(image, bbox)
    else:
        cv2.putText(image, "Lost", (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.rectangle(image, (15, 15), (200, 90), (255, 0, 255), 2)
    cv2.putText(image, "Fps:", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
    cv2.putText(image, "Status:", (20, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)

    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    if fps > 60:
        myColor = (20, 230, 20)
    elif fps > 20:
        myColor = (230, 20, 20)
    else:
        myColor = (20, 20, 230)

    cv2.putText(image, str(int(fps)), (75, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, myColor, 2)

    result.write(image)
    cv2.imshow("Tracking", image)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

result.release()
cv2.destroyAllWindows()