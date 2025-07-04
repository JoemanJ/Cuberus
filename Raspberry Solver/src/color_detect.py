import cv2
import numpy as np

# Faixas HSV para cada cor do cubo mágico
COLOR_HSV_RANGES = {
    'W': ((70, 0, 250), (100, 50, 255)),         # Branco ok
    'R': ((0, 250, 245), (10, 255, 255)),       # Vermelho ok
    'O': ((0, 140, 160), (20, 220, 255)),      # Laranja ok
    'Y': ((20, 80, 180), (35, 180, 255)),      # Amarelo ok
    'G': ((70, 250, 200), (85, 255, 220)),        # Verde ok
    'B': ((100, 250, 130), (130, 255, 200)),       # Azul ok
}

def detectar_face_por_cor(img, debug=False):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    pontos_centrais = []

    for cor, (lower, upper) in COLOR_HSV_RANGES.items():
        mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < 500 or area > 8000:
                continue

            M = cv2.moments(cnt)
            if M["m00"] == 0:
                continue

            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            pontos_centrais.append((cx, cy))

            if debug:
                cv2.circle(img, (cx, cy), 5, (255, 255, 255), -1)

    if len(pontos_centrais) < 9:
        if debug:
            print(f"[DEBUG] Apenas {len(pontos_centrais)} quadrados detectados.")
        return None, img

    pontos_ordenados = ordenar_em_grade(pontos_centrais)

    if debug:
        for i, (x, y) in enumerate(pontos_ordenados):
            cv2.putText(img, str(i + 1), (x - 10, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    return pontos_ordenados, img

def ordenar_em_grade(pontos):
    pontos = sorted(pontos, key=lambda p: p[1])
    linhas = [[], [], []]
    linha_atual = 0
    linha_base = pontos[0][1]
    tolerancia = 30 

    for p in pontos:
        if abs(p[1] - linha_base) > tolerancia and linha_atual < 2:
            linha_atual += 1
            linha_base = p[1]
        linhas[linha_atual].append(p)

    if any(len(linha) != 3 for linha in linhas):
        return pontos

    for linha in linhas:
        linha.sort(key=lambda p: p[0])
    return linhas[0] + linhas[1] + linhas[2]
