import cv2
from color_detect import detect_9_colors

img = cv2.imread("../test_inputs/cubo1.jpeg")

if img is None:
    print("Erro ao carregar a imagem.")
    exit()

colors, img_marked = detect_9_colors(img)
print("Cores detectadas:", colors)

cv2.imshow("Cubo com cores detectadas", img_marked)
cv2.waitKey(0)
cv2.destroyAllWindows()
