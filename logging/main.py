import logging

#basic logging configuration
logging.basicConfig(level=logging.INFO, filename="log.log", filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s")

a = 'dollars'
logging.warning(f'Give me a million {a}. This is your final warning.')
logging.critical('This is a critical message')

#stack trace
try:
    1/0
except ZeroDivisionError as e:
    # logging.error('ZeroDivisionError', exc_info=True)
    logging.exception('ZeroDivisionError koa')

# custom logger
logger = logging.getLogger(__name__)    # gets logger with same name or creates and returns a new one if not exists

handler = logging.FileHandler('test.log')
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info('Testing custom log')
