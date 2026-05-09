def find_min_max(arr):
    if not arr:
        raise ValueError("Array cannot be empty")

    def divide_and_conquer(left, right):
        if left == right:
            return arr[left], arr[left]

        if right == left + 1:
            if arr[left] < arr[right]:
                return arr[left], arr[right]
            return arr[right], arr[left]

        mid = (left + right) // 2

        min_left, max_left = divide_and_conquer(left, mid)
        min_right, max_right = divide_and_conquer(mid + 1, right)

        return min(min_left, min_right), max(max_left, max_right)

    return divide_and_conquer(0, len(arr) - 1)


if __name__ == "__main__":
    numbers = [4, 20, 7, 1, 10, 23, -40, -3, 12, 8, 5]
    minimum, maximum = find_min_max(numbers)

    print(f"Мінімум: {minimum}")
    print(f"Максимум: {maximum}")
    print((minimum, maximum))