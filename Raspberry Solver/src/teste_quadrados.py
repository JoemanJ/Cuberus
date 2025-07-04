import cv2
import os
from color_detect import detectar_face_por_cor

ARQUIVO_IMAGEM = "./test_inputs/calibrar2.png"

def testar_detectar_face(arquivo=ARQUIVO_IMAGEM):
    if not os.path.exists(arquivo):
        print(f"[ERRO] Arquivo '{arquivo}' não encontrado.")
        return

    img = cv2.imread(arquivo)

    pontos, img_marcada = detectar_face_por_cor(img, debug=True)

    if pontos is not None:
        print("[OK] 9 quadrados detectados ✅")
        for i, (x, y) in enumerate(pontos):
            print(f"  Quadrado {i+1}: ({x}, {y})")
    else:
        print("[X] Não foram detectados 9 quadrados ❌")
        exit()

    cv2.imshow("Resultado com marcações", img_marcada)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    testar_detectar_face()
