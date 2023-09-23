import paho.mqtt.client as mqtt
import cv2
from ultralytics import YOLO

# MQTT Configuration
mqtt_server = "broker.hivemq.com"
mqtt_port = 1883
mqtt_user = "pjriosc"
mqtt_password = "arduino-conexiones-101"  # Insert your password
mqtt_topic = "Arduino/MQTT"
detected_objects = {}  # To store detected objects in this frame

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print("Connection failed with code", rc)

def on_publish(client, userdata, mid):
    print("Message published")

client = mqtt.Client()
client.username_pw_set(username=mqtt_user, password=mqtt_password)

client.on_connect = on_connect
client.on_publish = on_publish

# Connect to the MQTT broker
client.connect(mqtt_server, mqtt_port)

# Load the YOLOv8 model
model = YOLO('yolov8x-pose.pt')

# Open the video file
cap = cv2.VideoCapture(0)
names = {0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 6: 'train', 7: 'truck', 8: 'boat', 9: 'traffic light', 10: 'fire hydrant', 11: 'stop sign', 12: 'parking meter', 13: 'bench', 14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant', 21: 'bear', 22: 'zebra', 23: 'giraffe', 24: 'backpack', 25: 'umbrella', 26: 'handbag', 27: 'tie', 28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard', 32: 'sports ball', 33: 'kite', 34: 'baseball bat', 35: 'baseball glove', 36: 'skateboard', 37: 'surfboard', 38: 'tennis racket', 39: 'bottle', 40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza', 54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted plant', 59: 'bed', 60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote', 66: 'keyboard', 67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'sink', 72: 'refrigerator', 73: 'book', 74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear', 78: 'hair drier', 79: 'toothbrush'}
cycle = 0
# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 inference on the frame
        results = model(frame, verbose=False, device='cuda')
        
        cycle +=1
        for r in results:
            for c in r.boxes.cls:
                if(detected_objects.get(names[int(c)])==None):
                    #print(detected_objects)
                    detected_objects.update({names[int(c)]:1})
                else:
                    #print(detected_objects)
                    detected_objects.update({names[int(c)]:(int(detected_objects[names[int(c)]])+1)})
                #detected_objects.append(names[int(c)])
        
        if cycle>=60:
            # Publish the detected objects to MQTT topic
            print(detected_objects)
            message = ', '.join(detected_objects)
            client.publish(mqtt_topic, message)
            detected_objects = {}  # To store detected objects in this frame
            cycle = 0

        # Visualize the results on the frame
        annotated_frame = results[0].plot()
        
        # Display the annotated frame
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
# Disconnect from the MQTT broker
client.disconnect()
