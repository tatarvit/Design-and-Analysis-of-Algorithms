import hashlib


class BloomFilter:
    def __init__(self, size: int, num_hashes: int):
        if not isinstance(size, int) or size <= 0:
            raise ValueError("size must be a positive integer")

        if not isinstance(num_hashes, int) or num_hashes <= 0:
            raise ValueError("num_hashes must be a positive integer")

        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size

    def _hashes(self, item: str):
        item = str(item)

        for i in range(self.num_hashes):
            hash_value = hashlib.sha256(f"{item}_{i}".encode()).hexdigest()
            yield int(hash_value, 16) % self.size

    def add(self, item: str) -> None:
        if not isinstance(item, str) or item.strip() == "":
            return

        for index in self._hashes(item):
            self.bit_array[index] = 1

    def contains(self, item: str) -> bool:
        if not isinstance(item, str) or item.strip() == "":
            return False

        return all(self.bit_array[index] == 1 for index in self._hashes(item))


def check_password_uniqueness(bloom_filter: BloomFilter, passwords: list) -> dict:
    results = {}

    if not isinstance(passwords, list):
        raise TypeError("passwords should be a list")

    for password in passwords:
        if not isinstance(password, str):
            results[password] = "incorrect password"
        elif password.strip() == "":
            results[password] = "password is empty"
        elif bloom_filter.contains(password):
            results[password] = "already used"
        else:
            results[password] = "unique"
            bloom_filter.add(password)

    return results


if __name__ == "__main__":
    bloom = BloomFilter(size=1000, num_hashes=3)

    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    new_passwords_to_check = [
        "password123",
        "newpassword",
        "admin123",
        "guest",
        "",
        "   ",
        None,
        12345
    ]

    results = check_password_uniqueness(bloom, new_passwords_to_check)

    for password, status in results.items():
        print(f"Password '{password}' — {status}.")