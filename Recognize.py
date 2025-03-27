import datetime
import os
import time
import csv
import cv2
import cv2.face
import pandas as pd
# cv2.face.LBPHFaceRecognizer.create()
#-------------------------
import csv
import os

def append_dataframe_to_csv(dataframe, filename):
    """Appends a list to an existing CSV file."""

    file_exists = os.path.isfile(filename)

    file_exists = os.path.isfile(filename)

    try:
        if file_exists:
            # Append without header if file exists
            dataframe.to_csv(filename, mode='a', header=False, index=False)
        else:
            # Create file and write header if it doesn't exist
            dataframe.to_csv(filename, mode='w', header=True, index=False)

        print(f"Data added to the {filename} successfully.")

    except IOError as e:
        print(f"Error appending to CSV: {e}")


def recognize_attendence():
    #recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    #recognizer = cv2.face_LBPHFaceRecognizer.create()
    recognizer=cv2.face.LBPHFaceRecognizer.create()
    recognizer.read("./TrainedModel/Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    df = pd.read_csv("StudentDetails" + os.sep + "StudentDetails.csv")

    font = cv2.FONT_HERSHEY_SIMPLEX # initialize the font style 
    col_names = ['Id', 'Name', 'Date', 'Time']

    # Creates an empty pandas DataFrame to store attendance records
    attendance = pd.DataFrame(columns=col_names)

    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)  # set video width
    cam.set(4, 480)  # set video height
    # Define min window size to be recognized as a face
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    while True:
        _,im = cam.read()
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

            if (100-conf) > 60:
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = str(aa)[2:-2]
                attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]

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



        attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
        cv2.imshow('Attendance', im)
        if (cv2.waitKey(1) == ord('q')):
            break

    attendance_file_path = os.path.join("Attendance", "Attendance.csv")

    append_dataframe_to_csv(attendance,attendance_file_path)

    print("Attendance Successful")
    cam.release()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    recognize_attendence()