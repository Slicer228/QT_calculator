import logging


logging.basicConfig(
    level=logging.ERROR,
    filemode='w',
    filename='logs.log',
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def add_log(exception):
    logging.error(str(exception))
