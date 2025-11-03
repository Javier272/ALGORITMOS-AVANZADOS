#lectura de datos
import re
from collections import deque
from typing import List, Tuple


def read_inputs(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        raw = f.read().replace("\ufeff", "").replace("\xa0", " ")
    lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]

    n = int(lines[0])
    k = 1

    dist = []
    for i in range(n):
        dist.append([float(x) for x in re.split(r"[,\s]+", lines[k+i])])
    k += n

    cap = []
    for i in range(n):
        cap.append([float(x) for x in re.split(r"[,\s]+", lines[k+i])])
    k += n


    points = []
    numre = re.compile(r"-?\d+\.?\d*")
    for i in range(n):
        nums = numre.findall(lines[k+i])
        points.append((float(nums[0]), float(nums[1])))

    return n, dist, cap, points


#conexiones de grafo y flujo algoritmo de prim.


def prim_mst (dist: List[List[float]]) -> List[Tuple[int,int]]:
    n = len(dist)
    INF =float("inf")
    used = [False]*n
    best = [INF]*n
    parent = [-1]*n
    best[0] = 0.0  

    for _ in range (n):
        u = -1; bv = INF
        for v in range(n):
            if not used[v] and best[v]<bv:
                u, bv = v, best[v]
        if u==-1:
            raise ValueError("El grafo no está conectado (nodo no dsipponible)")
        used[u] = True

        for v in range(n):
            w = dist[u][v]
    
            if not used[v] and w < best[v]:
                best[v] = w
                parent[v] = u

    edges: List[Tuple[int,int]] = []

    for v in range (1, n):
        u = parent[v]
        if u == -1:
            raise ValueError("El grafo no está conectado (nodo sin padre)")
        a, b = (u, v) if u < v else (v, u)
        edges.append((a, b))
    edges.sort()
    
    return edges



def max_flow(capacity: List[List[float]], source: int, sink: int) -> float:
    n = len(capacity)
    res = [[float(capacity[i][j]) for j in range(n)] for i in range(n)]
    flow = 0.0
    EPS = 1e-12 

    while True:
        parent = [-1]*n
        parent[source] = -2
        q = deque([(source, float("inf"))])
        aug = 0.0
        while q:
            u, f = q.popleft()
            for v in range(n):
                if parent[v] == -1 and res[u][v] > EPS:
                    parent[v] = u
                    nf = min(f, res[u][v])
                    if v == sink:
                        aug = nf
                        q.clear()
                        break
                    q.append((v, nf))

        if aug == 0.0:
            break
        flow += aug
        v = sink
        while v != source:
            u = parent[v]
            res[u][v] -= aug
            res[v][u] += aug
            v = u

    return flow

#tsp para ruta aproximada


def tsp_route(dist: List[List[float]]) -> List[int]:
    n = len(dist)

    unv = set(range(1, n))
    route = [0]
    cur = 0
    while unv:
        nxt = min(unv, key=lambda j: dist[cur][j])
        route.append(nxt)
        unv.remove(nxt)
        cur = nxt
    route.append(0)

   
    def improve(rt: List[int]) -> bool:
        improved = False
        for i in range(1, n-1):
            for k in range(i+1, n):
                a,b = rt[i-1], rt[i]
                c,d = rt[k], rt[(k+1) % len(rt)]
                if dist[a][b] + dist[c][d] > dist[a][c] + dist[b][d]:
                    rt[i:k+1] = reversed(rt[i:k+1])
                    improved = True
        return improved

    while improve(route):
        pass
    return route

#poligonos de voronoi


def voronoi_polygons(points: List[Tuple[float,float]], margin: float = 50.0) -> List[List[Tuple[float,float]]]:
    xs = [p[0] for p in points]; ys = [p[1] for p in points]
    minx, maxx = min(xs)-margin, max(xs)+margin
    miny, maxy = min(ys)-margin, max(ys)+margin
    bbox = [(minx,miny),(maxx,miny),(maxx,maxy),(minx,maxy)]

    def dot(a,b): return a[0]*b[0] + a[1]*b[1]

    def clip(poly, D, C):
        if not poly: return []
        out = []; m=len(poly)
        for i in range(m):
            P=poly[i]; Q=poly[(i+1)%m]
            fP = dot(P,D) - C; fQ = dot(Q,D) - C
            Pin = fP <= 1e-9; Qin = fQ <= 1e-9

            if Pin and Qin:
                out.append(Q)
            elif Pin and not Qin:
                denom = dot((Q[0] - P[0], Q[1]-P[1]), D)
                if abs(denom) > 1e-12:
                    t = (C - dot(P, D)) / denom
                    I = (P[0] + t * (Q[0] - P[0]), P[1] + t * (Q[1] - P[1]))
                    out.append(I)
            elif not Pin and Qin:
                denom = dot((Q[0] - P[0], Q[1] - P[1]), D)
                if abs(denom) > 1e-12:
                    t = (C - dot(P, D)) / denom
                    I = (P[0] + t * (Q[0] - P[0]), P[1] + t * (Q[1] - P[1]))
                    out.append(I)
                out.append(Q)
        clean = []
        for pt in out:
            if not clean or abs(pt[0]-clean[-1][0])>1e-9 or abs(pt[1]-clean[-1][1])>1e-9:
                clean.append(pt)
        return clean

    polys = []
    for i, A in enumerate(points):
        Ax, Ay = A; a2 = Ax * Ax + Ay * Ay
        poly = bbox[:]
        for j, B in enumerate(points):
            if i == j: continue
            Bx, By = B; b2 = Bx * Bx + By * By
            D = (Bx - Ax, By - Ay); C = (b2 - a2) / 2.0
            poly = clip(poly, D, C)
            if not poly: break
        polys.append(poly)
    return polys

#main del programa
import sys

def _labels_from_idxs(idxs):
    return [chr(ord('A') + i) for i in idxs]

def _fmt_num(x: float) -> str:
    return str(int(round(x))) if abs(x - round(x)) < 1e-9 else f"{x:.6f}"

def _print_outputs(mst_edges, route, flow, polygons):
    labeled = []
    for (u, v) in mst_edges:
        A = chr(ord('A') + u); B = chr(ord('A') + v)
        if A > B: A, B = B, A
        labeled.append((A, B))
    labeled.sort()
    for A, B in labeled:
        print(f"({A},{B})")

    print("-".join(_labels_from_idxs(route)))
    print(_fmt_num(flow))

    def fmt(x):
        return str(int(round(x))) if abs(x - round(x)) < 1e-6 else f"{x:.3f}"
    for poly in polygons:
        print("[" + ",".join(f"({fmt(x)},{fmt(y)})" for (x,y) in poly) + "]")

def main():
    path = sys.argv[1] if len(sys.argv) >= 2 else None
    N, dist, cap, centers = read_inputs(path)

    # 1) MST (Prim) -> aristas
    mst_edges = prim_mst(dist)

    # 2) TSP -> ruta 
    route = tsp_route(dist)

    # 3) Max Flow 
    flow = max_flow(cap, 0, N-1)

    # 4) Lista de poligonos
    polygons = voronoi_polygons(centers, margin=50.0)

    _print_outputs(mst_edges, route, flow, polygons)

if __name__ == "__main__":
    main()

    


