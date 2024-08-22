import cv2
import easyocr
import pyodbc
import matplotlib.pyplot as plt
from IPython.display import Image





#importing the model to detect the number plate
harcascade = "model/haarcascade_russian_plate_number.xml"

# open the cam to capture the image
cap = cv2.VideoCapture(0)

# setting the cam window 

cap.set(3,640) # window
cap.set(4,480) # height

min_area = 500
count = 0

while True:
    success, img = cap.read()

    plate_cascade = cv2.CascadeClassifier(harcascade)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)

    for (x,y,w,h) in plates:
        area = w * h

        if area > min_area:
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
            cv2.putText(img, "Number Plate", (x,y-5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)

            img_roi = img[y: y+h, x:x+w]
            cv2.imshow("ROI", img_roi)


    
    cv2.imshow("Result", img)

    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite("plates/scaned_img_" + str(count) + ".jpg", img_roi)
        cv2.rectangle(img, (0,200), (640,300), (0,255,0), cv2.FILLED)
        cv2.putText(img, "Plate Saved", (150, 265), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255), 2)
        cv2.imshow("Results",img)
        Image("plates/scaned_img_" + str(count) + ".jpg")

        reader = easyocr.Reader(['en'])

        output = reader.readtext("plates/scaned_img_" + str(count) + ".jpg")
        tuple_data = output[0]

        # Access individual components
        coordinates = tuple_data[0]  # List of coordinates
        license_plate = tuple_data[1]  # License plate string
        confidence = tuple_data[2]  # Confidence score
        print(f"the value is {license_plate}")
        insert_into_sql_server(license_plate)
        cv2.waitKey(500)
        count += 1

    
    #import OCR package


    # Function to insert extracted number plate into SQL Server
    def insert_into_sql_server(plate_text):
    # SQL Server connection details


        conn_str = (
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=your_server_name;'
        r'DATABASE=your_database_name;'
        r'UID=your_username;'
        r'PWD=your_password'
    )
  
        # Connect to SQL Server
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
    
        # Insert query
        insert_query = "INSERT INTO CarNumberPlates (NumberPlate) VALUES (?)"
        cursor.execute(insert_query, plate_text)
    
        # Commit and close connection
        conn.commit()
        cursor.close()
        conn.close()



'''

# Function to insert extracted number plate into SQL Server
def insert_into_sql_server(plate_text):
    # SQL Server connection details
    conn_str = (
        r'DRIVER={SWD-SQLDEV-01};'
        r'SERVER=SWD-SQLDEV-01;'
        r'DATABASE=HMGWEBDB;'
        r'UID=HmgWebUser;'
        r'PWD=HmgWebUser'
    )

   
    # Connect to SQL Server
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    # Insert query
    insert_query = "INSERT INTO CarNumberPlates (NumberPlate) VALUES (?)"
    cursor.execute(insert_query, plate_text)
    
    # Commit and close connection
    conn.commit()
    cursor.close()
    conn.close()

# Main function to capture video, process frames, and insert data
def main():
    # Initialize webcam capture
    cap = cv2.VideoCapture(0)  # 0 for default webcam
    
    # Initialize EasyOCR reader
    reader = easyocr.Reader(['en'])
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            break
        
        # Detect number plate
        plate_text = detect_number_plate(frame)
        
        if plate_text:
            print(f'Extracted Number Plate: {plate_text}')
            insert_into_sql_server(plate_text)
        
        # Display the captured frame
        cv2.imshow('Webcam', frame)
        
        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the webcam and close windows
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

'''




    # Main function
    # def main():
    #     image_path = 'car_image.jpg'  # Path to the image file
    #     plate_text = detect_number_plate(image_path)
        
    #     if plate_text:
    #         print(f'Extracted Number Plate: {plate_text}')
    #         insert_into_sql_server(plate_text)
    #     else:
    #         print('Number plate not detected.')

