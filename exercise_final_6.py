# Дані: словник {назва: {cost: ..., calories: ...}}
items = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350}
}

def greedy_algorithm(items: dict, budget: int):
    """
    Жадібний алгоритм (0/1): кожну страву можна взяти не більше одного разу.
    Критерій вибору — співвідношення калорії/вартість.
    """
    scored = []
    for name, info in items.items():
        cost = info["cost"]
        calories = info["calories"]
        ratio = calories / cost if cost > 0 else 0
        scored.append((name, cost, calories, ratio))

    # Сортування: ratio ↓, потім calories ↓, потім cost ↑
    scored.sort(key=lambda x: (x[3], x[2], -x[1]), reverse=True)

    total_calories = 0
    remaining_budget = budget
    chosen_items = []

    for name, cost, calories, _ in scored:
        if cost <= remaining_budget:
            chosen_items.append(name)
            remaining_budget -= cost
            total_calories += calories

    spent = budget - remaining_budget
    return total_calories, spent, chosen_items

def dynamic_programming(items: dict, budget: int):
    """
    ДП (класичний 0/1-рюкзак): оптимізуємо суму калорій при обмеженому бюджеті.
    """
    item_names = list(items.keys())
    n = len(item_names)

    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    # Заповнення DP-таблиці
    for i in range(1, n + 1):
        name = item_names[i - 1]
        cost = items[name]["cost"]
        calories = items[name]["calories"]
        for b in range(budget + 1):
            dp[i][b] = dp[i - 1][b]  # не беремо i-й елемент
            if cost <= b:
                dp[i][b] = max(dp[i][b], dp[i - 1][b - cost] + calories)  # беремо i-й

    # Відновлення вибраних страв
    chosen_items = []
    b = budget
    for i in range(n, 0, -1):
        if dp[i][b] != dp[i - 1][b]:
            name = item_names[i - 1]
            chosen_items.append(name)
            b -= items[name]["cost"]
    chosen_items.reverse()

    total_calories = dp[n][budget]
    spent = sum(items[name]["cost"] for name in chosen_items)
    return total_calories, spent, chosen_items

def ask_budget_interactive(prompt="Введіть бюджет (ціле число, грн): ") -> int:
    """
    Інтерактивне введення бюджету з валідацією:
    - приймає лише цілі числа;
    - не дозволяє від’ємні значення.
    """
    while True:
        s = input(prompt).strip()
        try:
            val = int(s)
            if val < 0:
                print("Бюджет не може бути від’ємним. Спробуйте ще раз.")
                continue
            return val
        except ValueError:
            print("Будь ласка, введіть ЦІЛЕ число. Наприклад: 0, 50, 120.")

def pretty_print_result(title: str, result):
    """
    Друк результату у зручному форматі.
    result = (total_calories, spent, chosen_items)
    """
    total_cal, spent, chosen = result
    print(f"\n[{title}]")
    print(f"  Калорійність: {total_cal}")
    print(f"  Витрачено:    {spent}")
    print(f"  Обрані страви: {', '.join(chosen) if chosen else '—'}")

if __name__ == '__main__':
    # Інтерактивне введення бюджету
    budget = ask_budget_interactive()

    # Запуск обох підходів
    greedy_result = greedy_algorithm(items, budget)
    dp_result = dynamic_programming(items, budget)

    # Вивід
    pretty_print_result("Жадібний алгоритм", greedy_result)
    pretty_print_result("Динамічне програмування", dp_result)

    # Підказка про різницю результатів
    if greedy_result[0] != dp_result[0]:
        print("\n Увага: жадібний підхід не гарантує оптимум — результати відрізняються від ДП.")
    else:
        print("\n Обидва підходи дали однакову суму калорій для цього бюджету.")
