import argparse
import math
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np


def draw_branch(ax, z: complex, length: float, angle: float,
                depth: int, theta: float, depth0: int):
    """
    Рекурсивно малює 'дерево Піфагора' лініями (стовбурами).

    z       — комплексна координата початку поточної гілки
    length  — довжина поточної гілки
    angle   — кут (радіани) напряму поточної гілки
    depth   — скільки рівнів ще малювати
    theta   — кут розвилки (радіани) для геометрії Піфагора
    depth0  — початкова глибина (для розрахунку товщини ліній/прозорості)
    """
    if depth <= 0 or length <= 0:
        return

    e = np.exp(1j * angle)
    p = z + length * e  # кінець поточної гілки

    # стилізація: товщина та альфа за глибиною
    t = depth / depth0
    lw = 1.5 + 2.5 * t
    alpha = 0.35 + 0.55 * t

    ax.plot([z.real, p.real], [z.imag, p.imag], linewidth=lw, alpha=alpha)

    # Геометрія Піфагора: довжини та кути для дочірніх гілок
    # Відхилення від батьківського напряму: ±(π/2 − θ)
    delta = math.pi / 2 - theta
    left_len = length * math.cos(theta)
    right_len = length * math.sin(theta)
    left_ang = angle + delta
    right_ang = angle - delta

    draw_branch(ax, p, left_len, left_ang, depth - 1, theta, depth0)
    draw_branch(ax, p, right_len, right_ang, depth - 1, theta, depth0)


def parse_args() -> Tuple[int, float]:
    parser = argparse.ArgumentParser(
        description="Фрактал «дерево Піфагора» у вигляді ліній (стовбурів)."
    )
    parser.add_argument("-d", "--depth", type=int, default=None,
                        help="Глибина рекурсії (напр., 10).")
    parser.add_argument("-t", "--theta", type=float, default=None,
                        help="Кут розвилки у градусах (типове 45). Діапазон (0, 90).")
    args = parser.parse_args()

    if args.depth is None:
        while True:
            try:
                d = int(input("Вкажіть глибину рекурсії (напр., 10): ").strip())
                if d >= 0:
                    args.depth = d
                    break
                print("Глибина має бути невід’ємною.")
            except ValueError:
                print("Будь ласка, введіть ціле число.")
    if args.theta is None:
        while True:
            raw = input("Вкажіть кут розвилки у градусах [Enter для 45]: ").strip()
            if raw == "":
                args.theta = 45.0
                break
            try:
                ang = float(raw)
                if 0 < ang < 90:
                    args.theta = ang
                    break
                print("Кут має бути в межах (0, 90) градусів.")
            except ValueError:
                print("Будь ласка, введіть число.")

    return args.depth, math.radians(args.theta)


def main():
    depth, theta = parse_args()

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect("equal", adjustable="datalim")
    ax.axis("off")

    # Початковий “стовбур”: вертикальна лінія вгору
    base_len = 1.0
    z0 = complex(0.0, 0.0)
    ang0 = math.pi / 2  # вгору по осі Y

    draw_branch(ax, z0, base_len, ang0, depth, theta, depth0=depth if depth > 0 else 1)

    # Автомасштаб + невеликий відступ, щоб не обрізати вершини
    ax.relim(); ax.autoscale_view()
    x0, x1 = ax.get_xlim(); y0, y1 = ax.get_ylim()
    pad_x = (x1 - x0) * 0.06 if x1 > x0 else 0.5
    pad_y = (y1 - y0) * 0.10 if y1 > y0 else 0.8
    ax.set_xlim(x0 - pad_x, x1 + pad_x)
    ax.set_ylim(y0 - pad_y, y1 + pad_y)

    plt.title(f"Pythagoras Tree (lines) | depth={depth}, theta={math.degrees(theta):.1f}°", pad=12)
    plt.show()


if __name__ == "__main__":
    main()
