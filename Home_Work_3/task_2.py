import re
import time
import hashlib
from math import log2
from typing import Iterable


LOG_FILE = "Home_Work_3/lms-stage-access.log"
IP_PATTERN = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")


def is_valid_ip(ip: str) -> bool:
    parts = ip.split(".")
    return len(parts) == 4 and all(part.isdigit() and 0 <= int(part) <= 255 for part in parts)


def load_ip_addresses(file_path: str) -> list[str]:
    ips = []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            match = IP_PATTERN.search(line)
            if not match:
                continue

            ip = match.group()
            if is_valid_ip(ip):
                ips.append(ip)

    return ips


def exact_count(ip_addresses: Iterable[str]) -> int:
    return len(set(ip_addresses))


class HyperLogLog:
    def __init__(self, p: int = 14):
        self.p = p
        self.m = 1 << p
        self.registers = [0] * self.m

    def _hash(self, value: str) -> int:
        return int(hashlib.sha1(value.encode("utf-8")).hexdigest(), 16)

    def add(self, value: str) -> None:
        x = self._hash(value)
        index = x & (self.m - 1)
        w = x >> self.p

        rank = self._rank(w)
        self.registers[index] = max(self.registers[index], rank)

    @staticmethod
    def _rank(value: int) -> int:
        if value == 0:
            return 160

        return 160 - value.bit_length() + 1

    def count(self) -> float:
        alpha = 0.7213 / (1 + 1.079 / self.m)
        raw_estimate = alpha * self.m * self.m / sum(2.0 ** -r for r in self.registers)

        empty_registers = self.registers.count(0)
        if raw_estimate <= 2.5 * self.m and empty_registers > 0:
            return self.m * log2(self.m / empty_registers)

        return raw_estimate


def hyperloglog_count(ip_addresses: Iterable[str]) -> int:
    hll = HyperLogLog(p=14)

    for ip in ip_addresses:
        hll.add(ip)

    return round(hll.count())


def measure_time(func, data):
    start = time.perf_counter()
    result = func(data)
    end = time.perf_counter()

    return result, end - start


def print_results(exact_result: int, exact_time: float, hll_result: int, hll_time: float) -> None:
    print("Comparison results:")
    print(f"{'':30}{'Accurate counting':>20}{'HyperLogLog':>15}")
    print(f"{'Unique elements':30}{exact_result:>20.1f}{hll_result:>15.1f}")
    print(f"{'Execution time (sec.)':30}{exact_time:>20.5f}{hll_time:>15.5f}")

    error = abs(exact_result - hll_result) / exact_result * 100 if exact_result else 0
    print(f"\nПохибка HyperLogLog: {error:.2f}%")


def main():
    ip_addresses = load_ip_addresses(LOG_FILE)

    exact_result, exact_time = measure_time(exact_count, ip_addresses)
    hll_result, hll_time = measure_time(hyperloglog_count, ip_addresses)

    print_results(exact_result, exact_time, hll_result, hll_time)


if __name__ == "__main__":
    main()