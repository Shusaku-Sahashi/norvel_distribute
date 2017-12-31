from logging import getLogger, DEBUG, Formatter, StreamHandler

class logger:

    def get_logger(self, name):
        # loggerの初期化
        self.logger = getLogger(name)
        self.logger.setLevel(DEBUG)

        # handler
        handler = StreamHandler()
        handler.setLevel(DEBUG)

        formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        self.logger.addHandler(handler)

        return self.logger

    def get_child(self, name):
        return self.logger.getChild(name)