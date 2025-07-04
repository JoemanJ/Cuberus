import cv2

def show_hsv(img_path):
    img = cv2.imread(img_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    def click_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            pixel = hsv[y, x]
            print(f"HSV em ({x},{y}): {pixel}")

    print("[INFO] Clique nos 9 quadrados amarelos e observe os valores HSV")
    cv2.imshow("Clique nos quadradinhos", img)
    cv2.setMouseCallback("Clique nos quadradinhos", click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

show_hsv("./test_inputs/calibrar2.png")
