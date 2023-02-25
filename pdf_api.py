import sys
import os

import requests
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class MyForm(QWidget):
    def __init__(self):
        super().__init__()
        self.gauth = GoogleAuth()
        self.initUI()
        self.setWindowTitle("Xalil Pdf API")

        self.flag = False

        
    def initUI(self):
        self.status_label = QLabel("")
        
        self.auth_button = QPushButton("Authenticate")
        self.auth_button.clicked.connect(self.authenticate)
        
        self.file_name_label = QLabel("File Name:")
        self.file_name_input = QLineEdit()
        
        self.pdf_link_label = QLabel("PDF Link:")
        self.pdf_link_input = QLineEdit()
        
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.upload_file)
        
        layout = QVBoxLayout()
        layout.addWidget(self.auth_button)
        layout.addWidget(self.file_name_label)
        layout.addWidget(self.file_name_input)
        layout.addWidget(self.pdf_link_label)
        layout.addWidget(self.pdf_link_input)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.status_label)

        self.setLayout(layout)
        

    def dowloand_link(self):
        # The URL of the PDF file to download
        url = self.pdf_link_input.text()

        # Make a GET request to download the file
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Write the content of the response (the PDF file) to a local file
            dir_path = os.path.dirname(os.path.abspath(__file__))
            self.my_pathy = dir_path + "/" + self.file_name_input.text()
            self.my_pathy = self.my_pathy.replace(" ","")
            if not self.my_pathy.endswith(".pdf"):
                self.my_pathy += ".pdf"

    
            with open(self.my_pathy, "wb") as f:
                f.write(response.content)
            self.status_label.setText(f"PDF downloaded to {self.my_pathy}")

            print(f"PDF file saved to {self.my_pathy}")
        else:
            self.status_label.setText("Failed to download the PDF file.")
            print("Failed to download the PDF file.")


    def authenticate(self):
        self.gauth = GoogleAuth()
        self.gauth.LocalWebserverAuth()
        self.drive = GoogleDrive(self.gauth)
        self.flag = True
        self.status_label.setText("Google authentication successful")

        
    def upload_file(self):
        file_name = self.file_name_input.text()
        file_name = file_name.replace(" ","")
        file_name += ".pdf"

        url = self.pdf_link_input.text()
        #if 
        if url[:7] == "file://":
            url = url[7:]
            self.my_pathy = url
        else:

            self.dowloand_link()

        self.status_label.setText("File uploading to  to Google Drive ...")

        if self.flag != True:
            self.authenticate()
            self.flag = True

        f = self.drive.CreateFile({'title': file_name,
                                   'mimeType': 'application/pdf',
                                   'parents': [{'kind': 'drive#fileLink', 'id': "1xodbJIFX24uWPYiF3gD7Wsb5n29uLZKq"}]})
                                   #'parents': [{'kind': 'drive#fileLink', 'id': "1QIBNUM0AM6Nj395spZ6JNF7qE1bMPKRd"}]})
        f.SetContentFile(self.my_pathy)
        f.Upload()

        self.status_label.setText("File deleted from local system")

        os.remove(self.my_pathy)
        print("file deleted")


    #TODO
    #add multiple link support 
    #add multiple link dowloand from txt file 
    #add acces api from whatsapp 
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    form = MyForm()
    form.show()
    exit(app.exec())
