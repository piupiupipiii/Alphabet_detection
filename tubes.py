import cv2
import numpy as np
import pandas as pd
import os
import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.uic import loadUi


class ShowImage(QMainWindow):
    def __init__(self):
        super(ShowImage, self).__init__()
        loadUi('gui.ui', self)
        self.csv_path = 'C:\\Users\\user\\Documents\\folder pipi\\archive (2)\\A_Z Handwritten Data.csv'
        self.Image = None
        self.buttonBrowseImage.clicked.connect(self.browseImage)

    def browseImage(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Images (*.png *.xpm *.jpg *.bmp *.jpeg)")
        if file_dialog.exec_():
            file_path = file_dialog.selectedFiles()[0]
            self.Image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            self.displayImage(self.Image, self.label)
            print("Gambar berhasil dibaca:", self.Image)
            self.preprocessImage()

    def displayImage(self, image, label):
        if image is not None:
            qformat = QImage.Format_Indexed8

            if len(image.shape) == 3:
                if image.shape[2] == 4:
                    qformat = QImage.Format_RGBA8888
                else:
                    qformat = QImage.Format_RGB888

            img = QImage(image.data, image.shape[1], image.shape[0],
                         image.strides[0], qformat)

            img = img.rgbSwapped()

            label.setPixmap(QPixmap.fromImage(img))

    def preprocessImage(self):
        def detect_letter(image):
            print("Memulai proses deteksi huruf...")
            if image is None:
                print("Gambar tidak valid!")
                return None

            df = pd.read_csv(self.csv_path, header=None)
            print("Data huruf berhasil dimuat:", df)

            max_corr = -np.inf
            detected_letter = None
            for i, template in enumerate(df.iloc[:, 1:].values):
                result = cv2.matchTemplate(image, template.reshape((28, 28)), cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                if max_val > max_corr:
                    max_corr = max_val
                    detected_letter = chr(ord('A') + i)

            return detected_letter

        print("Memulai proses preprocessing gambar...")
        if self.csv_path and os.path.exists(self.csv_path):
            if self.Image is not None:
                detected_letter = detect_letter(self.Image)
                if detected_letter is not None:
                    print(f"Deteksi huruf selesai. Gambar berisi huruf '{detected_letter}'")
                else:
                    print("Tidak ada huruf yang terdeteksi dalam gambar")
        else:
            print("Path file CSV tidak valid atau tidak ditemukan.")


app = QtWidgets.QApplication(sys.argv)
window = ShowImage()
window.setWindowTitle('Project Tubes')
window.show()
sys.exit(app.exec_())
