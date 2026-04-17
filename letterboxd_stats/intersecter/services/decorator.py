import time


def measure_time(unit="s"):
    def dekorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            wynik = func(*args, **kwargs)
            end = time.time()
            duration = end - start  # domyślnie sek
            if unit == "ms":
                duration *= 1000
            print(f"Duration of executing {func.__name__}: {duration} {unit}")
            return wynik

        return wrapper

    return dekorator
