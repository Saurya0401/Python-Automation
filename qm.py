#! python3

from automation import get_item, open_default_browser


if __name__ == "__main__":
    open_default_browser(url=f"https://www.google.com/maps/place/{get_item()}")
    exit(0)
