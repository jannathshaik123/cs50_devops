from prime import is_prime

def test_prime(n,expected):
    if is_prime(n) != expected:
        print(f"Test failed for {n}: expected {expected}, got {is_prime(n)}")