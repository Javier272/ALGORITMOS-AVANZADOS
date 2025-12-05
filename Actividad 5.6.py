#Javier Solorzano, A01645642
#Luis Fernando Rojo Valdés, A01640584

import random
import math
import numpy as np
import matplotlib.pyplot as plt

def f(x: float) -> float:
    return -x**4 + 4*x**3 - 10*x**2 + 8*x

DOM_MIN = -2.0
DOM_MAX = 4.0

def get_neighbors(x: float, step: float):
    neighbors = []
    left = x - step
    right = x + step
    if left >= DOM_MIN:
        neighbors.append(left)
    if right <= DOM_MAX:
        neighbors.append(right)
    return neighbors

def iterative_improvement(x0: float, step: float, max_iters: int):
    x = x0
    fx = f(x)
    history = []     
    traj_x = [x]      
    traj_y = [fx]     

    for it in range(1, max_iters + 1):
        neighbors = get_neighbors(x, step)
        xn = random.choice(neighbors)   
        fn = f(xn)

        if fn > fx:
            decision = "mover"
            x, fx = xn, fn
        else:
            decision = "quedarse"

        history.append({
            "iter": it,
            "x": x,
            "fx": fx,
            "neighbor": xn,
            "f_neighbor": fn,
            "decision": decision
        })

        traj_x.append(x)
        traj_y.append(fx)

    return history, traj_x, traj_y

def hill_climbing(x0: float, step: float, max_iters: int):
    x = x0
    fx = f(x)
    history = []
    traj_x = [x]
    traj_y = [fx]

    for it in range(1, max_iters + 1):
        neighbors = get_neighbors(x, step)

        best_x = x
        best_fx = fx

        for xn in neighbors:
            fn = f(xn)
            if fn > best_fx:
                best_fx = fn
                best_x = xn

        if best_fx > fx:
            decision = "mover"
            x, fx = best_x, best_fx
        else:
            decision = "quedarse"

        history.append({
            "iter": it,
            "x": x,
            "fx": fx,
            "neighbors": neighbors,
            "decision": decision
        })

        traj_x.append(x)
        traj_y.append(fx)

    return history, traj_x, traj_y

def simulated_annealing(x0: float, step: float, max_iters: int,
                        T0: float, alpha: float):
    x = x0
    fx = f(x)
    T = T0

    history = []
    traj_x = [x]
    traj_y = [fx]

    for it in range(1, max_iters + 1):
        neighbors = get_neighbors(x, step)
        xn = random.choice(neighbors)
        fn = f(xn)

        delta = fn - fx 

        if delta > 0:
            accept = True
            prob = 1.0
            decision = "mover"
        else:
            if T > 1e-8:
                prob = math.exp(delta / T)
            else:
                prob = 0.0
            r = random.random()
            if r < prob:
                accept = True
                decision = f"mover (peor, r={r:.3f} < p={prob:.3f})"
            else:
                accept = False
                decision = f"quedarse (r={r:.3f} ≥ p={prob:.3f})"

        if accept:
            x, fx = xn, fn

        history.append({
            "iter": it,
            "x": x,
            "fx": fx,
            "neighbor": xn,
            "f_neighbor": fn,
            "delta": delta,
            "T": T,
            "prob": prob,
            "decision": decision
        })

        traj_x.append(x)
        traj_y.append(fx)

        T *= alpha

    return history, traj_x, traj_y

def print_iterative_table(history):
    print("\nMejora iterativa")
    print(f"{'it':>3} {'x':>8} {'f(x)':>10} {'vecino':>10} {'f(vecino)':>12} {'decisión':>20}")
    for row in history:
        print(f"{row['iter']:3d} "
              f"{row['x']:8.3f} "
              f"{row['fx']:10.3f} "
              f"{row['neighbor']:10.3f} "
              f"{row['f_neighbor']:12.3f} "
              f"{row['decision']:>20}")

def print_hill_table(history):
    print("\nHill-Climbing")
    print(f"{'it':>3} {'x':>8} {'f(x)':>10} {'vecinos':>22} {'decisión':>20}")
    for row in history:
        neigh_str = "[" + ", ".join(f"{v:.2f}" for v in row['neighbors']) + "]"
        print(f"{row['iter']:3d} "
              f"{row['x']:8.3f} "
              f"{row['fx']:10.3f} "
              f"{neigh_str:>22} "
              f"{row['decision']:>20}")

def print_sa_table(history):
    print("\nSimulated Annealing")
    print(f"{'it':>3} {'T':>8} {'x':>8} {'f(x)':>10} {'vecino':>10} {'f(vecino)':>12} {'Δ':>8} {'p(aceptar)':>12} {'decisión':>25}")
    for row in history:
        print(f"{row['iter']:3d} "
              f"{row['T']:8.3f} "
              f"{row['x']:8.3f} "
              f"{row['fx']:10.3f} "
              f"{row['neighbor']:10.3f} "
              f"{row['f_neighbor']:12.3f} "
              f"{row['delta']:8.3f} "
              f"{row['prob']:12.3f} "
              f"{row['decision']:>25}")

def plot_results(traj1, traj2, traj3):
    xs = np.linspace(DOM_MIN, DOM_MAX, 600)
    ys = f(xs)

    idx = np.argmax(ys)
    x_opt = xs[idx]
    y_opt = ys[idx]

    plt.figure()
    plt.plot(xs, ys, label="f(x)")
    plt.axhline(0, linewidth=0.5)

    x1, y1 = traj1
    x2, y2 = traj2
    x3, y3 = traj3

    plt.plot(x1, y1, marker="o", linestyle="-", label="Mejora iterativa")
    plt.plot(x2, y2, marker="o", linestyle="-", label="Hill-Climbing")
    plt.plot(x3, y3, marker="o", linestyle="-", label="Simulated Annealing")

    plt.scatter([x_opt], [y_opt], s=80, marker="*", label="Óptimo global aprox")

    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend()
    plt.grid(True)
    plt.show()

random.seed(0)   

max_iters = 50
step = 0.1
T0 = 100.0
alpha = 0.95

x0 = random.uniform(DOM_MIN, DOM_MAX)
print(f"x0 inicial: {x0:.3f}, f(x0) = {f(x0):.3f}")

hist_it, it_x, it_y = iterative_improvement(x0, step, max_iters)
hist_hc, hc_x, hc_y = hill_climbing(x0, step, max_iters)
hist_sa, sa_x, sa_y = simulated_annealing(x0, step, max_iters, T0, alpha)

print_iterative_table(hist_it)
print_hill_table(hist_hc)
print_sa_table(hist_sa)

plot_results((it_x, it_y), (hc_x, hc_y), (sa_x, sa_y))

#¿Cuál llegó más cerca del óptimo global? Hill-Climbing

#¿Cuál exploró más el espacio? Simulated Annealing.

#¿Cuántas iteraciones se necesitan aprox? Mejora iterativa y Hill-Climbing ocupan unas 10–15 iteraciones, Simulated Annealing ocupa unas 20–30 iteraciones para ser mas estable/confiable.