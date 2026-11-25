"""Завдання 3: порівняння сортування злиттям, вставками та Timsort.

Час виконання вимірюється модулем timeit на різних наборах даних.

Використання:
    python3 task3_sorting_comparison.py
"""

import random
import timeit

SIZES = [100, 1_000, 5_000, 10_000, 100_000]
REPEATS = 3
INSERTION_SORT_LIMIT = 10_000  # більші масиви вставками сортуються занадто довго


def insertion_sort(arr: list) -> list:
    result = arr[:]
    for i in range(1, len(result)):
        key = result[i]
        j = i - 1
        while j >= 0 and result[j] > key:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = key
    return result


def merge(left: list, right: list) -> list:
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def merge_sort(arr: list) -> list:
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    return merge(merge_sort(arr[:mid]), merge_sort(arr[mid:]))


def timsort(arr: list) -> list:
    return sorted(arr)


ALGORITHMS = {
    "Merge sort": merge_sort,
    "Insertion sort": insertion_sort,
    "Timsort (sorted)": timsort,
}


def generate_datasets(size: int) -> dict:
    random.seed(42)
    random_data = [random.randint(0, size * 10) for _ in range(size)]
    sorted_data = sorted(random_data)
    nearly_sorted = sorted_data[:]
    for _ in range(max(1, size // 100)):
        a, b = random.randrange(size), random.randrange(size)
        nearly_sorted[a], nearly_sorted[b] = nearly_sorted[b], nearly_sorted[a]
    return {
        "Випадковий": random_data,
        "Відсортований": sorted_data,
        "Зворотний": sorted_data[::-1],
        "Майже відсортований": nearly_sorted,
    }


def measure(func, data: list) -> float:
    """Повертає найкращий середній час одного запуску в секундах."""
    timer = timeit.Timer(lambda: func(data))
    number = 1 if len(data) >= 5_000 else 5
    return min(timer.repeat(repeat=REPEATS, number=number)) / number


def check_correctness() -> None:
    sample = [random.randint(-100, 100) for _ in range(500)]
    expected = sorted(sample)
    for name, func in ALGORITHMS.items():
        assert func(sample) == expected, f"{name} сортує некоректно"


def main() -> None:
    check_correctness()
    header = f"| {'Набір даних':<20} | {'n':>6} | " + " | ".join(
        f"{name:>16}" for name in ALGORITHMS
    ) + " |"
    print(header)
    print("|" + "|".join("-" * (len(col)) for col in header.split("|")[1:-1]) + "|")

    for size in SIZES:
        for dataset_name, data in generate_datasets(size).items():
            cells = []
            for name, func in ALGORITHMS.items():
                if func is insertion_sort and size > INSERTION_SORT_LIMIT:
                    cells.append(f"{'—':>16}")
                    continue
                cells.append(f"{measure(func, data):>14.6f} с")
            print(f"| {dataset_name:<20} | {size:>6} | " + " | ".join(cells) + " |")


if __name__ == "__main__":
    main()
