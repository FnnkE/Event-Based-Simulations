import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
 
img = cv.imread('IMG_1182.JPG', cv.IMREAD_GRAYSCALE)
assert img is not None, "file could not be read, check with os.path.exists()"

img2 = cv.imread('IMG_1193.JPG', cv.IMREAD_GRAYSCALE)
assert img is not None, "file could not be read, check with os.path.exists()"

img = cv.medianBlur(img,5)
img2 = cv.medianBlur(img2,5)

ret,th1 = cv.threshold(img,127,255,cv.THRESH_BINARY)
ret2,th2 = cv.threshold(img2,127,255,cv.THRESH_BINARY)

 
titles = ['Original Image', 'Global Thresholding (v = 127)',
            'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
diff = th1-th2

height, width = diff.shape

output = np.zeros((height,width,3), np.uint8)

for y in range(height):
    for x in range(width):
        if (diff[y,y]!=255):
            continue
        if (th2[y,x]==255):
            output[y,x]=(255,0,0)
        if (th1[y,x]==255):
            output[y,x]=(0,0,255)

images = [ th1+th2, diff, output, output]


for i in range(4):
    plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])
plt.show()


