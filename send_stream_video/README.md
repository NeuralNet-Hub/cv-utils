# Live Streaming using Flask for any frame
This is a Flask Web-App to stream live from local webcam or CCTV (rtsp link).

## How to use it?

1. Deploy the API running `apihttpflask.py`. This will create and endpoint in port 5000 that will receive the images
2. Run `client.py`. This will take images from webcam and it will send to the endpoint at the port 8080.
3. Go to your browser and type `http://localhost:5000/`. This will show the images that are being sent to the endpoint.


### How to change the source for RTSP and HTTP cameras?

Change `cv2.VideoCapture(0)` for any of the following sources:

1. `camera = cv2.VideoCapture('rtsp://username:password@camera_ip_address:554/your url')`
2. `camera = cv2.VideoCapture('http://192.168.0.11:4747/video?1280x720')`
3. `camera = cv2.VideoCapture(2)`

