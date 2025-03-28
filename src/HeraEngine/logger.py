import time

class Logger():
    def __init__(self):
        self.level = 0
        self.header = "[HeraEngine][{level} ({time})]"

    def DEBUG(self,message):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        header = self.header.format(level="DEBUG", time=current_time)
        log_entry = f"{header} {message}"
        print(log_entry)

    def INFO(self,message):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        header = self.header.format(level="INFO", time=current_time)
        log_entry = f"{header} {message}"
        print(log_entry)

    def WARNING(self,message):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        header = self.header.format(level="WARNING", time=current_time)
        log_entry = f"{header} {message}"
        print(log_entry)

    def ERROR(self,message):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        header = self.header.format(level="ERROR", time=current_time)
        log_entry = f"{header} {message}"
        print(log_entry)