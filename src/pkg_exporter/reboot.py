from pathlib import Path


class RebootManager:
    def __init__(self):
        self.value = 0

    def query(self):
        rebootPath = Path("/run/reboot-required")
        if rebootPath.is_file():
            self.value = 1

    def getMetricValue(self):
        return self.value
