import numpy
from scipy import ndimage
from PIL import Image

def otsu(image):
  size = image.shape[0]*image.shape[1]
  hist  = ndimage.histogram(image, 0, 255, 256)
  sum = numpy.dot(numpy.arange(0,256), hist)
  
  sumB = 0.0
  
  wB = 0
  wF = 0
  varmax = 0.0
  Tmax = 0
  
  for T in range(255):
    wB += hist[T]                   #Weight Background
    if (wB == 0): continue
    wF = size-wB                    #Weight Foreground
    if (wF == 0): break
    
    sumB += float(T * hist[T])
    
    mB = sumB / wB             # Mean Background
    mF = (sum - sumB) / wF     # Mean Foreground
    
    varBetween = float(wB) * float(wF) * (mB - mF) * (mB - mF)

    if varBetween > varmax: (varmax, Tmax) = (varBetween, T)
      
  print Tmax
  return ((image > Tmax)*255).astype(numpy.uint8)

###

# IMAGE THRESHOLDING BY MINIMIZING THE MEASURES OF FUZZINESS
# LIANG-KAIHUANG and MAO-JIUN J. WANG

def ux (x, t, u0, u1):
  if x <= t:
    K = u0
  else:
    K = u1
  return 1.0/(1.0+numpy.abs((x-K)/256.0))

def yager_entropy (hist, t, u0, u1, p=2.0):
  v = 0.0
  for I in range(256):
    v += (numpy.abs(2.0*ux(I, t, u0, u1)-1.0)**p)*hist[I]
  return (v**(1.0/p))

def fuzzy_thresh(image):
  size = image.shape[0]*image.shape[1]
  hist = ndimage.histogram(image, 0, 255, 256)
  sum  = numpy.dot(numpy.arange(0,256), hist)
  
  S = 0
  W = 0
  
  fuzzinessmax = 0.0
  Tmax = 0
  
  for T in range(254):
    S  += hist[T]
    nS  = size-S
    W  += T*hist[T]
    nW  = sum-W
    
    if nW > 0:
      u0 = int(float(W)/S)
      u1 = int(float(nW)/nS)
      
      fuzziness = yager_entropy(hist, T, u0, u1)
      if fuzziness > fuzzinessmax: (Tmax, fuzzinessmax) = (T, fuzziness)
  
  print Tmax
  return ((image > Tmax)*255).astype(numpy.uint8)
  
###

I = numpy.asarray(Image.open("img/block.png").convert("L")).astype(numpy.uint8)
T = otsu(I)
Image.fromarray(T).save("img/otsu.png")
T = fuzzy_thresh(I)
Image.fromarray(T).save("img/fuzzy.png")

