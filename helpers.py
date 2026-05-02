import random
import string


def generate_random_string(length):
    letters = string.ascii_lowercase
    random_chars = []
    current_length = 0
    while current_length < length:
        random_chars.append(random.choice(letters))
        current_length += 1
    return "".join(random_chars)
