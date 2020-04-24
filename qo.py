#! python3
# todo: camsys

from automation import click_icon, exit_with_errmsg, get_coords, get_item, open_default_browser

url_dict = {"keep": "https://keep.google.com/u/0/", "keep1": "https://keep.google.com/u/1/",
            "class": "https://classroom.google.com/u/1/h", "mmls": "https://mmls.mmu.edu.my/",
            "e3lec": "https://meet.google.com/nsm-pfhm-acm?authuser=1",
            "e3tut": "https://meet.google.com/zxw-udei-noy?authuser=1",
            "dllec": "https://meet.google.com/lookup/EEE1036FOE?authuser=1",
            "dltut": "https://meet.google.com/aeu-hpaf-sfw?authuser=1"}

coords = get_coords()


def qo():
    try:
        site = get_item()
        open_default_browser(url=url_dict[site])
        if site == "mmls":
            click_icon(coords[site][0], region=coords[site][1])
    except KeyError:
        exit_with_errmsg("Invalid input.")


if __name__ == "__main__":
    qo()
    exit(0)
