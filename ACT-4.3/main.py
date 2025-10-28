import math

#calcula la distancia de dos puntos
def distancia(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

# ecuentra el par de puntos más cercano usando fuerza bruta
def fuerza_bruta(puntos):
    # Inicializa la distancia mínima con un valor grande para asegurar que cualquier distancia calculada sea menor
    min_dist = float('inf')
    par = (None, None)
    n = len(puntos)
    for i in range(n):
        for j in range(i+1, n):
            d = distancia(puntos[i], puntos[j])
            if d < min_dist:
                min_dist = d
                par = (puntos[i], puntos[j])
    return min_dist, par


# Calcula la distancia mínima en la franja
def strip_closest(strip, d_min):
    min_dist = d_min
    par = (None, None)
    strip.sort(key=lambda p: p[1])
    for i in range(len(strip)):
        for j in range(i+1, len(strip)):
            if (strip[j][1] - strip[i][1]) >= min_dist:
                break
            d = distancia(strip[i], strip[j])
            if d < min_dist:
                min_dist = d
                par = (strip[i], strip[j])
    return min_dist, par

# divide los puntos y halla el par más cercano recursivamente
def closest_pair_rec(puntos):
    n = len(puntos)
    if n <= 3:
        return fuerza_bruta(puntos)

    mid = n // 2
    mid_x = puntos[mid][0]

    izq = puntos[:mid]
    der = puntos[mid:]

    d_izq, par_izq = closest_pair_rec(izq)
    d_der, par_der = closest_pair_rec(der)

    if d_izq < d_der:
        d_min = d_izq
        par = par_izq
    else:
        d_min = d_der
        par = par_der

    # Construir la franja de puntos cercanos al eje medio
    strip = [p for p in puntos if abs(p[0] - mid_x) < d_min]

    d_strip, par_strip = strip_closest(strip, d_min)

    if d_strip < d_min:
        return d_strip, par_strip
    else:
        return d_min, par
    
# Funcion que llama al algoritmo principal
def closest_pair(puntos):
    puntos_ordenados = sorted(puntos, key=lambda p: p[0])
    return closest_pair_rec(puntos_ordenados)

puntos = [
    (37, 35), (35, 46), (11, 6), (7, 37), (43, 50), (25, 24),
    (42, 18), (10, 2), (42, 22), (35, 29), (44, 2), (11, 49),
    (5, 33), (40, 39), (37, 47), (13, 33), (47, 40), (20, 33),
    (7, 21), (25, 2)]


dist_min, par = closest_pair(puntos)


print(f"Distancia mínima: {dist_min:.4f}")
print(f"Par más cercano: {par[0]} y {par[1]}")




# Gráfica ASCII


def ascii_plot(puntos, par, ancho=60, alto=20):
    xs = [p[0] for p in puntos]
    ys = [p[1] for p in puntos]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)

    def escalar_x(x): return int((x - minx)/(maxx - minx)*(ancho-1))
    def escalar_y(y): return int((y - miny)/(maxy - miny)*(alto-1))

    matriz = [[" " for _ in range(ancho)] for _ in range(alto)]

    for p in puntos:
        x, y = escalar_x(p[0]), escalar_y(p[1])
        matriz[alto-1-y][x] = "o"

    # Marcar los puntos más cercanos con X
    for p in par:
        x, y = escalar_x(p[0]), escalar_y(p[1])
        matriz[alto-1-y][x] = "X"

    print("Gráfica ASCII (X = puntos más cercanos):")
    for fila in matriz:
        print("".join(fila))

ascii_plot(puntos, par)
