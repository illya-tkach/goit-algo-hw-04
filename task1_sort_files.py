"""Завдання 1: рекурсивне копіювання та сортування файлів за розширенням.

Використання:
    python3 task1_sort_files.py <вихідна_директорія> [директорія_призначення]

Якщо директорію призначення не вказано, використовується ``dist``.
"""

import argparse
import shutil
import sys
from pathlib import Path

NO_EXTENSION_DIR = "no_extension"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Рекурсивно копіює файли та сортує їх у піддиректорії за розширенням."
    )
    parser.add_argument("source", type=Path, help="Шлях до вихідної директорії")
    parser.add_argument(
        "destination",
        type=Path,
        nargs="?",
        default=Path("dist"),
        help="Шлях до директорії призначення (за замовчуванням: dist)",
    )
    return parser.parse_args()


def copy_file(file_path: Path, destination: Path) -> None:
    """Копіює файл у піддиректорію destination, названу за його розширенням."""
    extension = file_path.suffix[1:].lower() or NO_EXTENSION_DIR
    target_dir = destination / extension
    try:
        target_dir.mkdir(parents=True, exist_ok=True)
        target_path = target_dir / file_path.name
        counter = 1
        while target_path.exists():
            target_path = target_dir / f"{file_path.stem}_{counter}{file_path.suffix}"
            counter += 1
        shutil.copy2(file_path, target_path)
        print(f"Скопійовано: {file_path} -> {target_path}")
    except PermissionError:
        print(f"Немає доступу до файлу: {file_path}", file=sys.stderr)
    except OSError as error:
        print(f"Помилка копіювання {file_path}: {error}", file=sys.stderr)


def process_directory(path: Path, destination: Path) -> None:
    """Рекурсивно перебирає всі елементи директорії path."""
    try:
        items = list(path.iterdir())
    except PermissionError:
        print(f"Немає доступу до директорії: {path}", file=sys.stderr)
        return
    except OSError as error:
        print(f"Помилка читання директорії {path}: {error}", file=sys.stderr)
        return

    for item in items:
        # Не обробляємо директорію призначення, якщо вона всередині вихідної.
        if item.resolve() == destination.resolve():
            continue
        if item.is_dir():
            process_directory(item, destination)
        elif item.is_file():
            copy_file(item, destination)


def main() -> None:
    args = parse_args()
    source: Path = args.source
    destination: Path = args.destination

    if not source.exists():
        print(f"Вихідна директорія не існує: {source}", file=sys.stderr)
        sys.exit(1)
    if not source.is_dir():
        print(f"Шлях не є директорією: {source}", file=sys.stderr)
        sys.exit(1)

    try:
        destination.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        print(f"Не вдалося створити директорію {destination}: {error}", file=sys.stderr)
        sys.exit(1)

    process_directory(source, destination)
    print(f"Готово. Файли скопійовано та розсортовано у: {destination.resolve()}")


if __name__ == "__main__":
    main()
