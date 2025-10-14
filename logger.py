from datetime import datetime


class logs:
    def __init__(
        self, app_name: str = "Coffee Shop", file_name: str = "app.log"
    ) -> None:
        self.file_name = file_name
        self.app_name = app_name

        self.log_file = open(self.file_name, "w+")

    def build_message(self, message: str) -> str:
        now = datetime.now()
        formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")

        log = f'[{formatted_time}]["{self.app_name}"] - {message}\n'

        return log

    def add(self, message: str):
        final_log = self.build_message(message=message)

        self.log_file.write(final_log)
        self.log_file.flush()

        print(final_log)
        return final_log
