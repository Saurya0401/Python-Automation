from automation import get_item, home_path, screencap
from datetime import datetime
from os import path, mkdir


def scp():
    # gui option
    if not path.exists(f"{home_path}\\Desktop\\Screencaps"):
        mkdir(f"{home_path}\\Desktop\\Screencaps")
    default_name = datetime.strftime(datetime.now(), "%d%m%Y-%H%M%S")
    name = get_item()
    filename = f"{home_path}\\Desktop\\Screencaps\\{name if name else 'scp-' + default_name}.png"
    screencap(img_file=filename)


if __name__ == "__main__":
    scp()
    exit(0)
