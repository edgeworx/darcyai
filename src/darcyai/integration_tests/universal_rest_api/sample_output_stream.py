from darcyai.config import Config
from darcyai.output.output_stream import OutputStream

class SampleOutputStream(OutputStream):
    def __init__(self):
        super().__init__()

        self.config_schema = [
            Config("test", "bool", False, "Test"),
        ]


    def write(self, data):
        pass


    def close(self):
        pass
