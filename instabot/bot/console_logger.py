class ConsoleLogger:
    @staticmethod
    def print(verbosity, text):
        if verbosity:
            print(text)
