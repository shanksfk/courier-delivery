import logging
from src.courier_io import CourierIO


def configure_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename='app.log',  # log to a file
        filemode='w'  # overwrite2 the log file each time
    )


if __name__ == "__main__":
    configure_logging()
    app = CourierIO()
    app.run()
