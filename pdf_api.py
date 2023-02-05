import sys
import requests
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class MyForm(QWidget):
    def __init__(self):
        super().__init__()
        self.gauth = GoogleAuth()
        self.initUI()
        self.flag = False
        
    def initUI(self):
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
        
        self.setLayout(layout)
        

    def dowloand_link(self):
        # The URL of the PDF file to download
        url = self.pdf_link_input.text()

        # Make a GET request to download the file
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Write the content of the response (the PDF file) to a local file
            self.file_path = "/Users/halil/Desktop/pdf_api/deneme.pdf"
    
            with open(self.file_path, "wb") as f:
                f.write(response.content)
            print(f"PDF file saved to {self.file_path}")
        else:
            print("Failed to download the PDF file.")


    def authenticate(self):
        self.gauth = GoogleAuth()
        self.gauth.LocalWebserverAuth()
        self.drive = GoogleDrive(self.gauth)
        self.flag = True
        
    def upload_file(self):
        file_name = self.file_name_input.text()
        self.dowloand_link()

        if self.flag != True:
            self.authenticate()
            self.flag = True

        f = self.drive.CreateFile({'title': file_name,
                                   'mimeType': 'application/pdf',
                                   'parents': [{'kind': 'drive#fileLink', 'id': "your drive link goes here"}]})
        f.SetContentFile(self.file_path)
        f.Upload()

    #TODO
    #add multiple link support 
    #add multiple link dowloand from txt file 
    #add acces api from whatsapp 
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyForm()
    form.show()
    sys.exit(app.exec())
