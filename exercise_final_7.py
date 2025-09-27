import random
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path

def simulate_dice_rolls(num_rolls, seed=42):
    """
    Імітує кидки двох кубиків і повертає словник ймовірностей сум 2..12.
    (Заповнення TODO з наданого шаблону)
    """
    rng = random.Random(seed)
    counts = {s: 0 for s in range(2, 13)}  # лічильники для кожної можливої суми

    # Симуляція кидків
    for _ in range(num_rolls):
        d1 = rng.randint(1, 6)
        d2 = rng.randint(1, 6)
        s = d1 + d2
        # Підрахунок кількості кидків для можливих значень сум
        counts[s] += 1

    # Обрахування ймовірності випаду кожної суми
    probabilities = {s: counts[s] / num_rolls for s in range(2, 13)}
    return probabilities

def plot_probabilities(probabilities, num_rolls=None):
    sums = list(probabilities.keys())
    probs = list(probabilities.values())

    # Створення графіка
    plt.figure()
    plt.bar(sums, probs, tick_label=sums)
    plt.xlabel('Сума чисел на кубиках')
    plt.ylabel('Ймовірність')
    title = 'Ймовірність суми чисел на двох кубиках'
    if num_rolls is not None:
        title += f' (N={num_rolls})'
    plt.title(title)

    # Додавання відсотків випадання на графік
    for i, prob in enumerate(probs):
        plt.text(sums[i], prob, f"{prob*100:.2f}%", ha='center', va='bottom', fontsize=8)

    # Невеликий відступ згори, щоб не обрізати підписи
    plt.ylim(0, max(probs) * 1.15)
    plt.tight_layout()
    plt.show()

# ---- Додаткові невеликі допоміжні функції (мінімальне розширення шаблону) ----
def theoretical_probs():
    """Аналітичні (теоретичні) ймовірності для сум 2..12."""
    combos = {2:1, 3:2, 4:3, 5:4, 6:5, 7:6, 8:5, 9:4, 10:3, 11:2, 12:1}
    total = 36
    return {s: combos[s] / total for s in range(2, 13)}

def write_readme(probabilities, theory, N, path=None):
    """Генерує короткий README з порівнянням Monte Carlo та теорії для найбільшого N.
    README зберігається там, де лежить скрипт.
    """
    if path is None:
        try:
            script_dir = Path(__file__).resolve().parent
        except NameError:
            # запасний варіант для середовищ без __file__
            script_dir = Path.cwd()
        path = script_dir / 'README_MonteCarlo_Dice.md'

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    lines = [
        '# Завдання 7. Метод Монте-Карло — сума на двох кубиках',
        f'**Дата запуску:** {now}',
        '',
        f'## Результати (N={N})',
        '| Сума | Monte Carlo, % | Теоретична, % | Абс. похибка, п.п. |',
        '|-----:|---------------:|--------------:|-------------------:|'
    ]
    for s in range(2, 13):
        mc = probabilities[s] * 100
        th = theory[s] * 100
        lines.append(f'| {s:>2} | {mc:6.2f} | {th:6.2f} | {mc - th:+6.2f} |')
    lines += [
        '',
        '  ## Висновки',
        'Порівняння результатів, отриманих за допомогою симуляції методом Монте-Карло, з аналітичними розрахунками показує високу точність моделювання.',
        '    1.  **Точність зростає з кількістю випробувань**: При невеликій кількості кидків (напр., 100) результати можуть помітно відхилятися від теоретичних значень. Однак при збільшенні кількості симуляцій до 10,000, 100,000 і більше, отримані ймовірності дуже близько наближаються до аналітичних. Це наочно демонструє **закон великих чисел**.',
        '   2.  **Підтвердження теоретичного розподілу**: Симуляція підтверджує, що сума **7** є найімовірнішою, а ймовірності сум, рівновіддалених від 7 (наприклад, 6 і 8, 5 і 9), є приблизно однаковими.',
        '   3.  **Ефективність методу**: Метод Монте-Карло є потужним інструментом для вирішення задач, де аналітичний розрахунок є складним або неможливим. Цей приклад показує, що навіть для простої системи він дає дуже точні результати.',

        '   Отже, розрахунки, виконані за допомогою методу Монте-Карло, є правильними та підтверджуються аналітичною теорією ймовірностей.'
    ]
    Path(path).write_text('\n'.join(lines), encoding='utf-8')
    return str(path)

if __name__ == "__main__":
    theory = theoretical_probs()
    best_N = None
    best_probs = None

    for accuracy in [100, 1000, 10000, 100000]:
        # Симуляція кидків і обчислення ймовірностей
        probabilities = simulate_dice_rolls(accuracy, seed=42)

        # Коротке порівняння з аналітичними значеннями у консолі
        print(f"\\n=== N={accuracy} ===")
        for s in range(2, 13):
            mc = probabilities[s] * 100
            th = theory[s] * 100
            print(f"Сума {s:>2}: MC={mc:6.2f}% | Теорія={th:6.2f}% | Δ={mc - th:+6.2f} п.п.")

        # Відображення ймовірностей на графіку (із зазначенням N у назві)
        plot_probabilities(probabilities, num_rolls=accuracy)

        best_N = accuracy
        best_probs = probabilities

    # Генеруємо короткий README за підсумками найбільшої симуляції і зберігаємо поряд зі скриптом
    out = write_readme(best_probs, theory, best_N)
    print(f"README збережено: {out}")
