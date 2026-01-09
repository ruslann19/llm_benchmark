def print_with_padding(s: str, padding: str = 5 * "-", end: str = "\n") -> None:
    print(f"{padding} {s} {padding}", end=end)
