import cv2
import numpy as np
from color_detect import COLOR_HSV_RANGES

img = cv2.imread("./test_inputs/calibrar1.png")
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

for cor, (lower, upper) in COLOR_HSV_RANGES.items():
    print(f"=== Cor {cor} ===")
    mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5,5), np.uint8))
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(f"Contornos detectados: {len(contours)}")

    img_copy = img.copy()
    count = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 200 or area > 10000:
            continue
        count += 1
        approx = cv2.approxPolyDP(cnt, 0.04 * cv2.arcLength(cnt, True), True)
        cv2.drawContours(img_copy, [approx], -1, (0,255,0), 2)

    print(f"Quadrados válidos para cor {cor}: {count}")
    cv2.imshow(f"Máscara - {cor}", mask)
    cv2.imshow(f"Detectado - {cor}", img_copy)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
