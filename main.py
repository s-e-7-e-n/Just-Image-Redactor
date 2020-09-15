"""
JUST IMAGE REDACTOR BY VLADISLAV DYUDIN
version 1.0
"""

# import sys, time
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import Image
import  AppDesign # IMPORTING A DESIGN
from ImageRedactor import ImageRedactor # CLASS FOR WORKING WITH IMAGE

class JIR_App(QtWidgets.QMainWindow, AppDesign.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        try:
            # CONNECTING EVENTS TO BUTTONS
            # BUTTONS THAT ADD AN IMAGE
            self.AddImageButton.clicked.connect(self.AddImage)
            self.newImage_Button.clicked.connect(self.AddImage)
            # BUTTON THAT SHOW THE DIFFERENCE
            self.Compare_Button.pressed.connect(self.showOriginal)
            self.Compare_Button.released.connect(self.showCurrent)
            # APPLY/SAVE/DISCARD BUTTONS
            self.Apply_Button.clicked.connect(self.eventApply)
            self.Save_Button.clicked.connect(self.saveFile)
            self.Discard_Button.clicked.connect(self.reset)

            # CONNECTING EVENTS TO SLIDERS
            # HSB CHANNELS SLIDERS
            self.Hue_Slider.valueChanged.connect(self.hueChange)
            self.Saturation_Slider.valueChanged.connect(self.saturationChange)
            self.Brightness_Slider.valueChanged.connect(self.brightnessChange)
            # HSB CONTRAST SLIDERS
            self.ContrastHue_Slider.valueChanged.connect(self.hueContrastChange)
            self.ContrastSaturation_Slider.valueChanged.connect(self.saturationContrastChange)
            self.ContrastBrightness_Slider.valueChanged.connect(self.brightnessContrastChange)
            # RGB SLIDERS
            self.Red_Slider.valueChanged.connect(self.redChange)
            self.Green_Slider.valueChanged.connect(self.greenChange)
            self.Blue_Slider.valueChanged.connect(self.blueChange)
            # RGB CONTRAST SLIDERS
            self.ContrastRed_Slider.valueChanged.connect(self.redContrastChange)
            self.ContrastGreen_Slider.valueChanged.connect(self.greenContrastChange)
            self.ContrastBlue_Slider.valueChanged.connect(self.blueContrastChange)

            # HIDING WINDOWS WITH SLIDERS
            self.HSB_frame.hide()
            self.HSBContrast_frame.hide()
            self.RGB_frame.hide()
            self.RGBContrast_frame.hide()
            # HIDING FUNCTION BUTTONS
            self.show_menu.hide() # BUTTONS THAT SHOW MENU AND HIDE WINDOWS OF SLIDERS
            self.hide_menu.hide() # BUTTONS THST HIDE MENU(SLIDERS WINDOW HIDE BACK BUTTON)
        except:
            sys.exit(0)

    # FUNCTIONS FOR COMPARISON
    # SHOW ORIGINAL IMAGE
    def showOriginal(self):
        self.ImagePlace.setPixmap(QtGui.QPixmap(self.ImagePath))
        self.Compare_Button.setStyleSheet("background-color: rgb(173, 173, 173); border-color: rgb(106, 106, 106)")
    # SHOW CURRENT IMAGE
    def showCurrent(self):
        self.ImagePlace.setPixmap(QtGui.QPixmap('temp.jpg'))
        self.Compare_Button.setStyleSheet("background-color: rgb(240, 240, 240); border-color: rgb(173, 173, 173)")   

    # FUNCTION THAT ADDS / REPLACES AN IMAGE
    def AddImage(self):
        try:
            path = QtWidgets.QFileDialog.getOpenFileName(self,
                             "Выбрать файл",
                             ".",
                             "JPG Files(*.jpg);;PNG Files(*.png);;GIF File(*.gif);;JPEG Files(*.jpeg)")[0]

            assert(path != '') # IF THE PATH IS EMPTY DONT CONTINUE
            self.ImagePath = path
            self.trueImage = Image.open(self.ImagePath) # TRUE IMAGE
            self.temporaryImage = Image.open(self.ImagePath) # THE IMAGE THAT WILL CHANGE

            self.ImageArray_hsv = ImageRedactor.getImageArray(self.temporaryImage, 'HSV') # HSV ARRAY OF IMAGE
            self.ImageArray_hsv = self.ImageArray_hsv.astype(np.int32, copy = False)
            self.ImageArray_rgb = ImageRedactor.getImageArray(self.temporaryImage, 'RGB') # RGB ARRAY OF IMAGE
            self.ImageArray_rgb = self.ImageArray_rgb.astype(np.int32, copy = False)
            
            self.ImageArray_hsv_temp = np.copy(self.ImageArray_hsv) # THE ARRAY THAT WILL CHANGE(HSV)
            self.ImageArray_rgb_temp = np.copy(self.ImageArray_rgb) # THE ARRAY THAT WILL CHANGE(RGB)
            
            # I HAVEN'T FOUND A WAY TO OUTPUT AN IMAGE WITHOUT SAVING IT UNDER A SPECIFIC NAME :(
            self.temporaryImage.save('temp.jpg', 'JPEG') # SAVE IMAGE
            self.ImagePlace.setPixmap(QtGui.QPixmap('temp.jpg')) # SHOWING IMAGE

            # ENABLING THE INTERFACE
            self.Compare_Button.setEnabled(True)
            self.Menu_frame.setEnabled(True)
            self.Foot_frame.setEnabled(True)
            
            # TO HELL WITH THAT HUGE BUTTON
            self.AddImageButton.hide()
        except:
            pass

    # CONFIRM THE CHANGE BY OVERWRITING OF ARRAYS
    def eventApply(self):
        self.ImageArray_rgb = ImageRedactor.getImageArray(self.temporaryImage, 'RGB')
        self.ImageArray_hsv = ImageRedactor.getImageArray(self.temporaryImage, 'HSV')

        self.ImageArray_hsv = self.ImageArray_hsv.astype(np.int32, copy = False)
        self.ImageArray_rgb = self.ImageArray_rgb.astype(np.int32, copy = False)
        
        self.ImageArray_hsv_temp = np.copy(self.ImageArray_hsv)
        self.ImageArray_rgb_temp = np.copy(self.ImageArray_rgb)
        self.resetValueSliders() # SETTING THE SLIDERS TO 0

    # HBS CHANNELS CHANGE
    def hueChange(self):
        # TO MOVE TOGETHER WITH
        if self.withHsbChange_check_2.checkState():
            self.Saturation_Slider.setValue(self.Hue_Slider.value())
        if self.withHsbChange_check_3.checkState():
            self.Brightness_Slider.setValue(self.Hue_Slider.value())
        # CHANGING
        self.ImageArray_hsv_temp[:,:,:1] = ImageRedactor.channelChange(np.copy(self.ImageArray_hsv[:,:,:1]), self.Hue_Slider.value())
        self.temporaryImage = ImageRedactor.getImagefromArray(self.ImageArray_hsv_temp)
        self.temporaryImage.save('temp.jpg', 'JPEG')
        self.ImagePlace.setPixmap(QtGui.QPixmap('temp.jpg'))

    def saturationChange(self):
        # TO MOVE TOGETHER WITH
        if self.withHsbChange_check_1.checkState():
            self.Hue_Slider.setValue(self.Saturation_Slider.value())
        if self.withHsbChange_check_3.checkState():
            self.Brightness_Slider.setValue(self.Saturation_Slider.value())
        # CHANGING
        self.ImageArray_hsv_temp[:,:,1:2] = ImageRedactor.channelChange(np.copy(self.ImageArray_hsv[:,:,1:2]), self.Saturation_Slider.value())
        self.temporaryImage = ImageRedactor.getImagefromArray(self.ImageArray_hsv_temp)
        self.temporaryImage.save('temp.jpg', 'JPEG')
        self.ImagePlace.setPixmap(QtGui.QPixmap('temp.jpg'))    
        
    def brightnessChange(self):
        # TO MOVE TOGETHER WITH
        if self.withHsbChange_check_1.checkState():
            self.Hue_Slider.setValue(self.Brightness_Slider.value())
        if self.withHsbChange_check_2.checkState():
            self.Saturation_Slider.setValue(self.Brightness_Slider.value())
        # CHANGING
        self.ImageArray_hsv_temp[:,:,2:3] = ImageRedactor.channelChange(np.copy(self.ImageArray_hsv[:,:,2:3]), self.Brightness_Slider.value())
        self.temporaryImage = ImageRedactor.getImagefromArray(self.ImageArray_hsv_temp)
        self.temporaryImage.save('temp.jpg', 'JPEG')
        self.ImagePlace.setPixmap(QtGui.QPixmap('temp.jpg'))

    # HSB CHANNELS CONTRAST CHANGE
    def hueContrastChange(self):
        # TO MOVE TOGETHER WITH
        if self.withHsbCntrChange_check_2.checkState():
            self.ContrastSaturation_Slider.setValue(self.ContrastHue_Slider.value())
        if self.withHsbCntrChange_check_3.checkState():
            self.ContrastBrightness_Slider.setValue(self.ContrastHue_Slider.value())
        # CHANGING
        self.ImageArray_hsv_temp[:,:,:1] = ImageRedactor.contrastChange_cnl(np.copy(self.ImageArray_hsv[:,:,:1]), self.ContrastHue_Slider.value())
        self.temporaryImage = ImageRedactor.getImagefromArray(self.ImageArray_hsv_temp)
        self.temporaryImage.save('temp.jpg', 'JPEG')
        self.ImagePlace.setPixmap(QtGui.QPixmap('temp.jpg'))

    def saturationContrastChange(self):
        # TO MOVE TOGETHER WITH
        if self.withHsbCntrChange_check_1.checkState():
            self.ContrastHue_Slider.setValue(self.ContrastSaturation_Slider.value())
        if self.withHsbCntrChange_check_3.checkState():
            self.ContrastBrightness_Slider.setValue(self.ContrastSaturation_Slider.value())
        # CHANGING
        self.ImageArray_hsv_temp[:,:,1:2] = ImageRedactor.contrastChange_cnl(np.copy(self.ImageArray_hsv[:,:,1:2]), self.ContrastSaturation_Slider.value())
        self.temporaryImage = ImageRedactor.getImagefromArray(self.ImageArray_hsv_temp)
        self.temporaryImage.save('temp.jpg', 'JPEG')
        self.ImagePlace.setPixmap(QtGui.QPixmap('temp.jpg'))

    def brightnessContrastChange(self):
        # TO MOVE TOGETHER WITH
        if self.withHsbCntrChange_check_1.checkState():
            self.ContrastHue_Slider.setValue(self.ContrastBrightness_Slider.value())
        if self.withHsbCntrChange_check_2.checkState():
            self.ContrastSaturation_Slider.setValue(self.ContrastBrightness_Slider.value())
        # CHANGING
        self.ImageArray_hsv_temp[:,:,2:3] = ImageRedactor.contrastChange_cnl(np.copy(self.ImageArray_hsv[:,:,2:3]), self.ContrastBrightness_Slider.value())
        self.temporaryImage = ImageRedactor.getImagefromArray(self.ImageArray_hsv_temp)
        self.temporaryImage.save('temp.jpg', 'JPEG')
        self.ImagePlace.setPixmap(QtGui.QPixmap('temp.jpg'))

    # RGB CHANNELS CHANGE
    def redChange(self):
        # TO MOVE TOGETHER WITH
        if self.withRgbChange_check_2.checkState():
            self.Green_Slider.setValue(self.Red_Slider.value())
        if self.withRgbChange_check_3.checkState():
            self.Blue_Slider.setValue(self.Red_Slider.value())
        # CHANGING
        self.ImageArray_rgb_temp[:,:,:1] = ImageRedactor.channelChange(np.copy(self.ImageArray_rgb[:,:,:1]), self.Red_Slider.value())
        self.temporaryImage = ImageRedactor.getImagefromArray(self.ImageArray_rgb_temp, 'RGB')
        self.temporaryImage.save('temp.jpg', 'JPEG')
        self.ImagePlace.setPixmap(QtGui.QPixmap('temp.jpg'))

    def greenChange(self):
        # TO MOVE TOGETHER WITH
        if self.withRgbChange_check_1.checkState():
            self.Red_Slider.setValue(self.Green_Slider.value())
        if self.withRgbChange_check_3.checkState():
            self.Blue_Slider.setValue(self.Green_Slider.value())
        # CHANGING
        self.ImageArray_rgb_temp[:,:,1:2] = ImageRedactor.channelChange(np.copy(self.ImageArray_rgb[:,:,1:2]), self.Green_Slider.value())
        self.temporaryImage = ImageRedactor.getImagefromArray(self.ImageArray_rgb_temp, 'RGB')
        self.temporaryImage.save('temp.jpg', 'JPEG')
        self.ImagePlace.setPixmap(QtGui.QPixmap('temp.jpg'))
        
    def blueChange(self):
        # TO MOVE TOGETHER WITH
        if self.withRgbChange_check_1.checkState():
            self.Red_Slider.setValue(self.Blue_Slider.value())
        if self.withRgbChange_check_2.checkState():
            self.Green_Slider.setValue(self.Blue_Slider.value())
        # CHANGING
        self.ImageArray_rgb_temp[:,:,2:3] = ImageRedactor.channelChange(np.copy(self.ImageArray_rgb[:,:,2:3]), self.Blue_Slider.value())
        self.temporaryImage = ImageRedactor.getImagefromArray(self.ImageArray_rgb_temp, 'RGB')
        self.temporaryImage.save('temp.jpg', 'JPEG')
        self.ImagePlace.setPixmap(QtGui.QPixmap('temp.jpg'))

    # RGB CHANNELS CONTRAST CHANGE
    def redContrastChange(self):
        # TO MOVE TOGETHER WITH
        if self.withRgbCntrChange_check_2.checkState():
            self.ContrastGreen_Slider.setValue(self.ContrastRed_Slider.value())
        if self.withRgbCntrChange_check_3.checkState():
            self.ContrastBlue_Slider.setValue(self.ContrastRed_Slider.value())
        # CHANGING
        self.ImageArray_rgb_temp[:,:,:1] = ImageRedactor.contrastChange_cnl(np.copy(self.ImageArray_rgb[:,:,:1]), self.ContrastRed_Slider.value())
        self.temporaryImage = ImageRedactor.getImagefromArray(self.ImageArray_rgb_temp, 'RGB')
        self.temporaryImage.save('temp.jpg', 'JPEG')
        self.ImagePlace.setPixmap(QtGui.QPixmap('temp.jpg'))

    def greenContrastChange(self):
        # TO MOVE TOGETHER WITH
        if self.withRgbCntrChange_check_1.checkState():
            self.ContrastRed_Slider.setValue(self.ContrastGreen_Slider.value())
        if self.withRgbCntrChange_check_3.checkState():
            self.ContrastBlue_Slider.setValue(self.ContrastGreen_Slider.value())
        # CHANGING
        self.ImageArray_rgb_temp[:,:,1:2] = ImageRedactor.contrastChange_cnl(np.copy(self.ImageArray_rgb[:,:,1:2]), self.ContrastGreen_Slider.value())
        self.temporaryImage = ImageRedactor.getImagefromArray(self.ImageArray_rgb_temp, 'RGB')
        self.temporaryImage.save('temp.jpg', 'JPEG')
        self.ImagePlace.setPixmap(QtGui.QPixmap('temp.jpg'))

    def blueContrastChange(self):
        # TO MOVE TOGETHER WITH
        if self.withRgbCntrChange_check_1.checkState():
            self.ContrastRed_Slider.setValue(self.ContrastBlue_Slider.value())
        if self.withRgbCntrChange_check_2.checkState():
            self.ContrastGreen_Slider.setValue(self.ContrastBlue_Slider.value())
        # CHANGING
        self.ImageArray_rgb_temp[:,:,2:3] = ImageRedactor.contrastChange_cnl(np.copy(self.ImageArray_rgb[:,:,2:3]), self.ContrastBlue_Slider.value())
        self.temporaryImage = ImageRedactor.getImagefromArray(self.ImageArray_rgb_temp, 'RGB')
        self.temporaryImage.save('temp.jpg', 'JPEG')
        self.ImagePlace.setPixmap(QtGui.QPixmap('temp.jpg'))

    def reset(self):
        self.resetValueSliders()

    def resetValueSliders(self):
        self.Hue_Slider.setValue(0)
        self.Saturation_Slider.setValue(0)
        self.Brightness_Slider.setValue(0)
        self.ContrastHue_Slider.setValue(0)
        self.ContrastSaturation_Slider.setValue(0)
        self.ContrastBrightness_Slider.setValue(0)

        self.Red_Slider.setValue(0)
        self.Green_Slider.setValue(0)
        self.Blue_Slider.setValue(0)
        self.ContrastRed_Slider.setValue(0)
        self.ContrastGreen_Slider.setValue(0)
        self.ContrastBlue_Slider.setValue(0)

    def saveFile(self):
        filename, ok = QtWidgets.QFileDialog.getSaveFileName(self,
                             "Сохранить файл",
                             ".",
                             "JPG Files(*.jpg)")
        try:
            self.temporaryImage.save(filename, 'JPEG')
        except:
            pass

def main():
    app = QtWidgets.QApplication([])
    window = JIR_App()
    window.move(50, 50)
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()