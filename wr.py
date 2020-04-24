from automation import get_item, get_weather


def wr():
    loc = get_item()
    get_weather(loc if loc else "here")


if __name__ == "__main__":
    wr()
    exit(0)
