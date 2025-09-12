import os

import g


def close_action():
    g.exit_flag = True

    print("Exiting...")

    os._exit(0)
