import streamlit as st
import cv2
import time
import pandas as pd
import os

st.title("Facial Recognition Attendance System")
# cap = cv2.VideoCapture(0)

# while True:
#     ret,frame = cap.read()
#     frame_placeholder = st.empty()
#     frame_placeholder.image(frame, channels="BGR")
#     time.sleep(0.01)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()

# def recognize_attendence():
#recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
#recognizer = cv2.face_LBPHFaceRecognizer.create()
recognizer=cv2.face.LBPHFaceRecognizer.create()
recognizer.read("./TrainedModel/Trainner.yml")
harcascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(harcascadePath)
df = pd.read_csv("StudentDetails" + os.sep + "StudentDetails.csv")

font = cv2.FONT_HERSHEY_SIMPLEX # initialize the font style 
# col_names = ['Id', 'Name', 'Date', 'Time']

# # Creates an empty pandas DataFrame to store attendance records
# attendance = pd.DataFrame(columns=col_names)

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640)  # set video width
cam.set(4, 480)  # set video height
# Define min window size to be recognized as a face
minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)

while True:
    _,im = cam.read()
    frame_placeholder = st.empty()
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.3, 5,minSize = (int(minW), int(minH)),flags = cv2.CASCADE_SCALE_IMAGE)
    for(x, y, w, h) in faces:
        cv2.rectangle(im, (x, y), (x+w, y+h), (10, 159, 255), 2)
        Id, conf = recognizer.predict(gray[y:y+h, x:x+w])
        aa=[]

        if conf < 100:

            aa = df.loc[df['Id'] == Id]['Name'].values
            confstr = "  {0}%".format(round(100 - conf))
            tt = str(Id)+"-"+aa

        else:
            Id = '  Unknown  '
            tt = str(Id)
            confstr = "  {0}%".format(round(100 - conf))

        # if (100-conf) > 60:
        #     ts = time.time()
        #     date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        #     timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        #     aa = str(aa)[2:-2]
        #     attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]

        tt = str(tt)[2:-2]
        if(100-conf) > 60:
            tt = tt + "[Pass]"
            cv2.putText(im, str(tt), (x+5,y-5), font, 1, (0, 255, 0), 2) # lable(id-name,Pass ) in white color
        else:
            cv2.putText(im, str(tt), (x + 5, y - 5), font, 1, (255, 255, 255), 2)

        if (100-conf) > 60:
            cv2.putText(im, str(confstr), (x + 5, y + h - 5), font,1, (0, 255, 0),1 )
        elif (100-conf) > 50:
            cv2.putText(im, str(confstr), (x + 5, y + h - 5), font, 1, (0, 255, 255), 1)
        else:
            cv2.putText(im, str(confstr), (x + 5, y + h - 5), font, 1, (0, 0, 255), 1)



    # attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
    frame_placeholder.image(im, channels="BGR")
    time.sleep(0.01)
    # cv2.imshow('Attendance', im)
    if (cv2.waitKey(1) == ord('q')):
        break

# attendance_file_path = os.path.join("Attendance", "Attendance.csv")

# append_dataframe_to_csv(attendance,attendance_file_path)

# print("Attendance Successful")
cam.release()
cv2.destroyAllWindows()