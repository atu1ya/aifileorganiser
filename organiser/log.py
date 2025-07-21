import logging

logging.basicConfig(
    filename="organiser.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

class Stats:
    def __init__(self):
        self.files_sorted = 0
        self.duplicates_detected = 0

    def log_file_sorted(self):
        self.files_sorted += 1
        logging.info(f"File sorted. Total: {self.files_sorted}")

    def log_duplicate_detected(self):
        self.duplicates_detected += 1
        logging.info(f"Duplicate detected. Total: {self.duplicates_detected}")

    def get_stats(self):
        return self.files_sorted, self.duplicates_detected
