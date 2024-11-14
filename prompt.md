```python
import dv_processing as dv
import cv2 as cv

# Open any camera
capture = dv.io.CameraCapture()

# Initiate a preview window
cv.namedWindow("Preview", cv.WINDOW_NORMAL)

# Run the loop while camera is still connected
while capture.isRunning():
    # Read a frame from the camera
    frame = capture.getNextFrame()

    # The method does not wait for frame arrive, it returns immediately with
    # latest available frame or if no data is available, returns a `None`
    if frame is not None:
        # Print received packet time range
        print(f"Received a frame at time [{frame.timestamp}]")

        # Show a preview of the image
        cv.imshow("Preview", frame.image)
    cv.waitKey(2)
```
上面是我读取相机帧的代码，请你根据上述代码来帮我写出双目摄像头标定的python程序。

```python
import dv_processing as dv
import cv2 as cv

# Open the specified camera
capture = dv.io.CameraCapture(cameraName="DAVIS346_00001055")

# Initiate a preview window
cv.namedWindow("Preview", cv.WINDOW_NORMAL)

# Run the loop while camera is still connected
while capture.isRunning():
    # Read a frame from the camera
    frame = capture.getNextFrame()

    # The method does not wait for frame arrive, it returns immediately with
    # latest available frame or if no data is available, returns a `None`
    if frame is not None:
        # Print received packet time range
        print(f"Received a frame at time [{frame.timestamp}]")

        # Show a preview of the image
        cv.imshow("Preview", frame.image)
    cv.waitKey(2)
```
上面是我读取一个相机的代码，现在我有两个相机，一个叫DAVIS346_00001055，另外一个叫DAVIS346_00001054，其中1055是左眼，1054是右眼，我希望你帮我修改上述程序，使其同时读取两个相机的图像并且同时展示在屏幕上，左眼的展示在屏幕的左边，右眼的展示在屏幕右边，两个相机的画面各占屏幕的一半。