def log(msg, color=None):
    colors = {
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "cyan": "\033[36m",
    }
    prefix = colors.get(color, "")
    reset = "\033[0m"
    print(prefix + msg + reset)

