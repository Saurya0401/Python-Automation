#! python3

from automation import open_default_browser, click_icon, get_coords

coords = get_coords()


def rps():
    open_default_browser()
    click_icon(icon=coords["menu"][0], region=coords["menu"][1])
    click_icon(icon=coords["rps"][0], region=coords["rps"][1])


if __name__ == "__main__":
    rps()
    exit(0)
