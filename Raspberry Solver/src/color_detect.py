import cv2
import numpy as np

COLOR_RANGES = {
    'U': ((0, 0, 200), (180, 50, 255)),       # Branco
    'R': ((0, 150, 100), (10, 255, 255)),     # Vermelho
    'R2': ((160, 150, 100), (180, 255, 255)), # Vermelho
    'F': ((35, 50, 50), (85, 255, 255)),      # Verde
    'D': ((20, 100, 100), (30, 255, 255)),    # Amarelo
    'L': ((10, 100, 20), (25, 255, 255)),     # Laranja
    'B': ((90, 50, 50), (130, 255, 255))      # Azul
}

def detect_color(bgr_pixel):
    """Classifica uma cor BGR como uma letra do cubo mágico."""
    pixel = np.uint8([[bgr_pixel]])
    hsv = cv2.cvtColor(pixel, cv2.COLOR_BGR2HSV)[0][0]
    h, s, v = hsv

    # Checa vermelho (2 faixas no HSV)
    if (COLOR_RANGES['R'][0][0] <= h <= COLOR_RANGES['R'][1][0] and
        COLOR_RANGES['R'][0][1] <= s <= COLOR_RANGES['R'][1][1] and
        COLOR_RANGES['R'][0][2] <= v <= COLOR_RANGES['R'][1][2]):
        return 'R'
    elif (COLOR_RANGES['R2'][0][0] <= h <= COLOR_RANGES['R2'][1][0] and
          COLOR_RANGES['R2'][0][1] <= s <= COLOR_RANGES['R2'][1][1] and
          COLOR_RANGES['R2'][0][2] <= v <= COLOR_RANGES['R2'][1][2]):
        return 'R'

    for code, (lower, upper) in COLOR_RANGES.items():
        if code in ['R', 'R2']:
            continue
        lower = np.array(lower, dtype=np.uint8)
        upper = np.array(upper, dtype=np.uint8)
        if cv2.inRange(np.array([hsv]), lower, upper)[0]:
            return code

    # Branco (baixa saturação, alta luminosidade)
    if v > 200 and s < 50:
        return 'U'

    return '?'  # não reconhecida

def average_color(img, x, y, size=20):
    """Calcula a média BGR de um quadrado centrado em (x, y)."""
    h, w, _ = img.shape
    x1 = max(x - size // 2, 0)
    y1 = max(y - size // 2, 0)
    x2 = min(x + size // 2, w)
    y2 = min(y + size // 2, h)
    region = img[y1:y2, x1:x2]
    return tuple(map(int, cv2.mean(region)[:3]))

def detect_9_colors(img):
    """Detecta as 9 cores centrais da imagem do cubo e retorna as letras."""
    h, w, _ = img.shape
    step_x = w // 3
    step_y = h // 3

    colors = []
    for row in range(3):
        for col in range(3):
            cx = col * step_x + step_x // 2
            cy = row * step_y + step_y // 2
            avg = average_color(img, cx, cy)
            code = detect_color(avg)
            colors.append(code)

            cv2.circle(img, (cx, cy), 10, (0, 0, 0), 2)
            cv2.putText(img, code, (cx - 10, cy + 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    return colors, img
