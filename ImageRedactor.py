import numpy as np
from PIL import Image

class ImageRedactor:
  
  # GETTING AN ARRAY FROM AN IMAGE
  def getImageArray(image, mode):
    if mode == 'HSV':
      image = image.convert('HSV')
    elif mode == 'RGB':
      pass
    imageArray = np.array(image)
    return imageArray

  # CONVERTING TO AN IMAGE
  def getImagefromArray(imageArray, mode = 'HSV'):
    imageArray_local = imageArray
    imageArray_local = ImageRedactor.normalizeArray(imageArray_local)
    imageArray_local = imageArray_local.astype(np.uint8, copy = False) # CAST TO NP.UINT8(BYTE) DATA TYPE
    if mode == 'HSV':
      image = Image.fromarray(imageArray_local, 'HSV')
      image = image.convert('RGB')
    elif mode == 'RGB':
      image = Image.fromarray(imageArray_local)
    return image

  # FOR CONTRAST CHANGING
  def contrastChange_cnl(array, factor):
    factor = (factor+100)/100
    avg_cnl = round(np.mean(array))
    array = factor * (array - avg_cnl) + avg_cnl
    return array

  # CAST TO RANGE(0, 255)
  def normalizeArray(array):
    array = np.where(array<0, 0, array)
    array = np.where(array>255, 255, array)
    return array

  # FOR VALUE CHANNELS CHANGING
  def channelChange(array, factor, cycle = False):
    array += factor
    if cycle:
      array %=256
    return array