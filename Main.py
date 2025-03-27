import os  
from Recognize import recognize_attendence
from Model_Train import ModelTrain
from Camera_Check import CheckCamera
from Capture_Image import takeImages

def title_bar():
    os.system('cls')  # for windows
    # title of the program

    print("\t**********************************************")
    print("\t***** Face Recognition Attendance System *****")
    print("\t**********************************************")

def mainMenu():
    title_bar()
    print()
    print(10 * "*", "WELCOME MENU", 10 * "*")
    print("[1] Check Camera")
    print("[2] Capture New Faces")
    print("[3] Model Training")
    print("[4] Recognize & Attendance")
    print("[5] Quit")

    while True:
        try:
            choice = int(input("Enter Choice: "))
            if choice == 1:
                print("checking camera...")
                CheckCamera()
                break
            elif choice == 2:
                print("Capturing image from video...")
                CaptureFaces()
                break
            elif choice == 3:
                print("Model Training With images...")
                ModelTrain()
                break
            elif choice == 4:
                print("Recognize face & Mark Attendence...")
                Recognize_Faces_and_Mark_Attendance()
                break
            elif choice == 5:
                print("Thank You, bye...")
                break
            else:
                print("Invalid Choice. Enter 1-5")
                mainMenu()
        except Exception as e:
            print("Error:", e)
            print("Invalid Choice. Enter 1-5\n Try Again")

#------------Menus-------
# ---------------------------------------------------------
# calling the camera test function from check camera.py file
def CheckCamera():
    CheckCamera()
    print("For check camera...")
    key = input("Enter any key to return main menu")
    mainMenu()

# --------------------------------------------------------------
# calling the take image function form capture image.py file

def CaptureFaces():
    while True:
        takeImages()
        user_input = input("run take images again? (Y/N)").upper()
        if user_input == "N":
            break
    key = input("Enter any key to return main menu")
    mainMenu()

# -----------------------------------------------------------------
# calling the train images from train_images.py file

def Trainimages():
    ModelTrain()
    key = input("Enter any key to return main menu")
    mainMenu()

# --------------------------------------------------------------------
# calling the recognize_attendance from recognize.py file
def Recognize_Faces_and_Mark_Attendance():
    recognize_attendence()
    key = input("Enter any key to return main menu")
    mainMenu()

mainMenu()