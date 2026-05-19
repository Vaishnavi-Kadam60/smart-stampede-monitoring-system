from ultralytics import YOLO
import cv2

# Load YOLOv8 pre-trained model
model = YOLO('yolov8n.pt')  # Downloaded automatically

cap = cv2.VideoCapture(0)  # Laptop camera

while True:
    ret, frame = cap.read()
    results = model(frame)  # Run YOLO model on frame

    count = 0  # Initialize people count

    for r in results:
        for box in r.boxes:  
            if int(box.cls) == 0:  # Class ID 0 = Person
                x1, y1, x2, y2 = map(int, box.xyxy[0])  
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                count += 1

    cv2.putText(frame, f"People Count: {count}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    cv2.imshow("Crowd Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
import smtplib
from email.mime.text import MIMEText

def send_email(count):
    sender_email = "vaishnavikadam60@gmail.com"
    receiver_email = "kadamvaishnavi22131021@gcoeara.ac.in"
    password = "your_email_password"  # Replace with your email password

    subject = "Crowd Alert: People Count Exceeded Limit!"
    body = f"Warning! The detected people count has exceeded the limit. Current Count: {count}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()
    print("Email Alert Sent!")



import requests

def trigger_pi():
    try:
        requests.post("http://192.168.226.65:5000/trigger")
        print("Triggered Raspberry Pi!")
    except Exception as e:
        print("Error:", e)

if count > 0:  # Change threshold as needed
    send_email(count)
    trigger_pi()


