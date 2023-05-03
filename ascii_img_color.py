import numpy as np
import cv2
from PIL import Image, ImageFont, ImageDraw
import warnings
warnings.filterwarnings("ignore")

CHAR_LIST = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~i!lI;:,\"^`"
# input: image (430, 379, 3)
img = cv2.imread("cloudy.jpg",1) 

# split image to 250 columns and n rows 
col = 300
height, width, _ = img.shape #height = 430; width = 379
cell_width = width / col # width of 1 cell 
cell_height = cell_width*2 #height of 1 cell 
row = int(height / cell_height) # n = row and it must be an integer

img_font = ImageFont.truetype('./DejaVuSansMono-Bold.ttf', size=25)
char_width, char_height = img_font.getsize("A")

ascimg_width = char_width * col
ascimg_height = 2 * char_height * row
asc_img = Image.new("RGB", (ascimg_width, ascimg_height), (0, 0, 0)) #replace new img with black pixel 
draw = ImageDraw.Draw(asc_img)

for i in range(row):
	for j in range(col):
		img2 = img[int(i*cell_height): int((i+1)*cell_height), int(j*cell_width): int((j+1)*cell_width)] # (vertical: 8pix ,horizontal: 4pix, 3)
		avg_color = np.sum(np.sum(img2, axis=0), axis=0) / (cell_height * cell_width)
		avg_color = tuple(avg_color.astype(np.int32).tolist()) #find average color
		#calculate average color (0-255) then find index of ascii characters
		index = int(np.mean(img2) / 255 * len(CHAR_LIST))
		draw.text((j * char_width, i * char_height), CHAR_LIST[index], fill=avg_color, font=img_font)
asc_img = asc_img.save("ascii_img6.jpg")

