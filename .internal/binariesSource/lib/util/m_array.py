import math

def find_nearest(numbers, target):
    if not numbers:
        return None  # If the list is empty, there is no number to compare

    sorted_numbers = sorted(numbers)  # Sort the list for easier searching

    # Use binary search to find the index of the nearest number
    left, right = 0, len(sorted_numbers) - 1
    while left < right:
        middle = (left + right) // 2
        if sorted_numbers[middle] < target:
            left = middle + 1
        else:
            right = middle

    # Now, 'left' contains the index of the nearest number
    nearest_number = sorted_numbers[left]

    return nearest_number
