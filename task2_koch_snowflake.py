"""Завдання 2: фрактал «сніжинка Коха» з рекурсією.

Використання:
    python3 task2_koch_snowflake.py [рівень_рекурсії]

Якщо рівень не передано аргументом, програма запитає його у користувача.
"""

import sys
import turtle

MAX_LEVEL = 7


def koch_curve(t: turtle.Turtle, order: int, size: float) -> None:
    """Рекурсивно малює криву Коха заданого порядку."""
    if order == 0:
        t.forward(size)
        return
    for angle in (60, -120, 60, 0):
        koch_curve(t, order - 1, size / 3)
        t.left(angle)


def draw_koch_snowflake(order: int, size: float = 300) -> None:
    """Малює сніжинку Коха з трьох кривих Коха."""
    window = turtle.Screen()
    window.bgcolor("white")
    window.title(f"Сніжинка Коха, рівень {order}")

    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    turtle.tracer(0, 0)

    t.penup()
    t.goto(-size / 2, size / (2 * 3 ** 0.5))
    t.pendown()

    for _ in range(3):
        koch_curve(t, order, size)
        t.right(120)

    turtle.update()
    window.mainloop()


def read_level() -> int:
    """Зчитує рівень рекурсії з аргументу командного рядка або з вводу."""
    raw = sys.argv[1] if len(sys.argv) > 1 else input(
        f"Введіть рівень рекурсії (0-{MAX_LEVEL}): "
    )
    try:
        level = int(raw)
    except ValueError:
        print("Рівень рекурсії має бути цілим числом.")
        sys.exit(1)
    if not 0 <= level <= MAX_LEVEL:
        print(f"Рівень рекурсії має бути в межах від 0 до {MAX_LEVEL}.")
        sys.exit(1)
    return level


if __name__ == "__main__":
    draw_koch_snowflake(read_level())
