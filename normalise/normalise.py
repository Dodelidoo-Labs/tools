##
# Normalise numbers in a string
##
import re

def normalize_numbers_in_string(input_string):
    # Regular expression pattern to find numbers in the string
    number_pattern = r"[-+]?\d*\.?\d+(?:,\d+)?"

    # Find the valid numbers in the input string
    numbers = re.findall(number_pattern, input_string)
    numbers = [float(num.replace(',', '')) for num in numbers if num.strip()]

    # Check if any valid numbers were found
    if not numbers:
        return input_string

    min_value = min(numbers)
    max_value = max(numbers)

    # Check if the range is zero
    if max_value == min_value:
        return input_string

    def normalize(match):
        number = float(match.group().replace(',', ''))
        # Normalize the number between 0 and 1
        normalized_number = (number - min_value) / (max_value - min_value)
        return str(normalized_number)

    # Use re.sub() with a custom function to replace numbers with normalized values
    normalized_string = re.sub(number_pattern, normalize, input_string)

    return normalized_string


string = 'text here::100 and another text here::400 and more text here::0.5'
norm = normalize_numbers_in_string(string)
print(f"Normalised: {norm}")