import argparse
import shutil
from pathlib import Path

arguments = argparse.ArgumentParser(
    prog="reccopy",
    description="Рекурсивно копіює файли з одного каталогу в інший на основі їх розширення.",
)

arguments.add_argument("-s", "--source", type=Path, required=True, help="Вихідний каталог")
arguments.add_argument(
    "-d",
    "--destination",
    type=Path,
    required=False,
    default="dist",
    help="Каталог призначення (default: ./%(default)s)",
)


def recursive_copy(source: Path, destination: Path):
    """
    Рекурсивно копіює файл або каталог із початкового шляху до кінцевого шляху.

    Args:
        source (Path): Шлях до файлу або каталогу для копіювання.
        destination (Path): Шлях цільового каталогу, куди буде скопійовано файл або каталог.

    Returns:
        None
    """
    try:
        if source.is_file():
            file_extension = source.suffix.lower()

            destination_subdirectory = destination / file_extension[1:]
            destination_subdirectory.mkdir(parents=True, exist_ok=True)

            destination_file = destination_subdirectory / source.name
            print(f"Копіюю {source} в {destination_file}")
            shutil.copy2(source, destination_file, follow_symlinks=False)
        else:
            for file in source.iterdir():
                recursive_copy(file, destination)
    except OSError as e:
        print(f"Не зміг скопіювати {source} в {destination}: {e}")


if __name__ == "__main__":
    args = arguments.parse_args()
    recursive_copy(args.source, args.destination)