class ErrorCounter:
    def __init__(self):
        self.accumulated_count = 0

    def invoke(self, f, *args) -> int:
        """
        Call f with args. Reset error count once a success is observed, otherwise increase error count by 1.
        The f function should catch Exception and thus doesn't throw exceptions.
        :param f: The function to be monitored. It must return True for success, False for failure.
        :param args: f's arguments.
        :return: The accumulated error count.
        """
        result = f(*args)
        if result:
            self.accumulated_count = 0
        else:
            self.accumulated_count += 1

        return self.accumulated_count
