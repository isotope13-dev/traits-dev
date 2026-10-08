# A normal lookup table and dotted display are insufficient for the decoder.
numbers = {"north": 12, "south": 24, "east": 36, "west": 48}
words = ["north", "south", "east", "west"]
display = ".".join(str(numbers[word]) for word in words)
