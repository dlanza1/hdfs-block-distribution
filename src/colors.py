class colors:
    G = '\033[92m' # Green
    Y = '\033[93m' # Yellow
    R = '\033[91m' # Red
    B = '\033[1m'  # Bold
    U = '\033[4m'  # Underline

def color(msg, color):
    return color + str(msg) +'\033[0m'
