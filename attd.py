from automation import get_item, screencap, qr_reader
# todo: do this with get_item()
# todo: click login icon


def attd():
    enable_gui = True if get_item() else False
    qr_img = screencap(delay_seconds=6, gui=enable_gui)
    qr_reader(qr_img)


if __name__ == "__main__":
    attd()
    exit(0)
