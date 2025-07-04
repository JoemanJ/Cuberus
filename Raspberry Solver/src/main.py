import cv2
import os
from color_detect import detectar_face_por_cor  # nova função baseada em cores HSV

def analisar_pasta(pasta="./test_inputs"):
    imagens_identificadas = 0
    imagens_nao_identificadas = 0

    for arquivo in sorted(os.listdir(pasta)):
        if not arquivo.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        caminho = os.path.join(pasta, arquivo)
        img = cv2.imread(caminho)

        if img is None:
            print(f"[ERRO] Não foi possível abrir {arquivo}")
            imagens_nao_identificadas += 1
            continue

        pontos, img_marcada = detectar_face_por_cor(img, debug=True)
        if pontos is not None:
            print(f"[OK] Imagem {arquivo}: face detectada ✅")
            imagens_identificadas += 1
            # salvar imagem marcada
            cv2.imwrite(f"output_marcadas/{arquivo}", img_marcada)
        else:
            print(f"[X] Imagem {arquivo}: face **não** identificada ❌")
            imagens_nao_identificadas += 1


        if pontos is not None:
            print(f"[OK] Imagem {arquivo}: face detectada ✅")
            imagens_identificadas += 1
        else:
            print(f"[X] Imagem {arquivo}: face **não** identificada ❌")
            imagens_nao_identificadas += 1

    print("\n===== RESUMO =====")
    print(f"✔️ Imagens com face detectada:     {imagens_identificadas}")
    print(f"❌ Imagens sem face identificada:  {imagens_nao_identificadas}")
    print("==================")

if __name__ == "__main__":
    analisar_pasta("./test_inputs")
