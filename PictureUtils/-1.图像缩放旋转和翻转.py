from PIL import Image
import matplotlib.pyplot as plt

img = Image.open('pokemon.jpg')         #打开图片

plt.figure('pokemon')                   #设置figure

dst1 = img.transpose(Image.ROTATE_90)  #设置逆时针旋转90
plt.subplot(3,3,1),plt.title('90')
plt.imshow(dst1),plt.axis('off')

dst2 = img.transpose(Image.ROTATE_180) #设置逆时针旋转180
plt.subplot(3,3,2),plt.title('180')
plt.imshow(dst2),plt.axis('off')

dst3 = img.transpose(Image.ROTATE_270) #设置逆时针旋转270
plt.subplot(3,3,3),plt.title('270')
plt.imshow(dst3),plt.axis('off')

dst4 = img.resize((120, 120))           #重设宽120，高120
plt.subplot(3,3,4),plt.title('resize')
plt.imshow(dst4),plt.axis('off')

dst5 = img.rotate(45)                   #逆时针旋转45
plt.subplot(3,3,5),plt.title('rotate')
plt.imshow(dst5),plt.axis('off')

dst6 = img.transpose(Image.FLIP_LEFT_RIGHT)     #左右互换
plt.subplot(3,3,6),plt.title('Image.FLIP_LEFT_RIGHT')
plt.imshow(dst6),plt.axis('off')

dst7 = img.transpose(Image.FLIP_TOP_BOTTOM)     #上下互换
plt.subplot(3,3,7),plt.title('Image.FLIP_TOP_BOTTOM')
plt.imshow(dst7),plt.axis('off')


plt.show()