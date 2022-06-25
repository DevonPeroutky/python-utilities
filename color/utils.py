import random

def random_rgb_color():
    """
    Return a random RGB color
    """
    print("Generating a random color!!!")
    return color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
