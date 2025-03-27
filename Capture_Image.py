import csv
import cv2
import os
import os.path
# import kagglehub

# # Download latest version
# harcascadePath = kagglehub.dataset_download("timlukasblom/haarcascade-frontalface-defaultxml")

# print("Path to dataset files:", harcascadePath)

#-------------------------------
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

#---------------------------------------
# Take image function
def takeImages():
    Id = input("Enter Your Id: ")
    name = input("Enter Your Name: ")
    if (is_number(Id) and name.isalpha()):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)

        sampleNum = 0
        while (True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (10, 159, 255), 2)
                # incrementing sample number
                sampleNum = sampleNum + 1
                # saving the captured face in the dataset folder TrainingImage
                path = "TrainingImage" + os.sep + name + "." + Id + '.' + str(sampleNum) + ".jpg"
                print("Image Name......:", path)
                cv2.imwrite("TrainingImage" + os.sep + name + "." + Id + '.' + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
                # display the frame
                cv2.imshow('frame', img)
            # wait for 100 miliseconds
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is more than 100
            elif sampleNum > 100:
                break
        cam.release()
        cv2.destroyAllWindows()
        res = f"Images saved for ID: {Id}, Name: {name}"
        print(res)

        student_details_path = os.path.join("StudentDetails", "StudentDetails.csv")
        student_data = {"Id": Id, "Name": name}

        try:
            file_exists = os.path.isfile(student_details_path)
            with open(student_details_path, 'a', newline='') as csvfile:
                fieldnames = ["Id", "Name"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader()
                writer.writerow(student_data)

        except IOError as e:
            print(f"Error writing to CSV: {e}")

    else:
        if not is_number(Id):
            print("Enter Numeric ID")
        if not name.isalpha():
            print("Enter Alphabetical Name")


# takeImages()