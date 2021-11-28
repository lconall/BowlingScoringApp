

class PytestBase():
    def setup_method(self, test_method):
        print(f"\n{'-' * 80}")
        print(f"{type(self).__name__}: {test_method.__name__}")
