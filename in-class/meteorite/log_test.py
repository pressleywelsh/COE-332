import argparse
import logging
import socket

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--loglevel', type=str, required=False, default='WARNING',
                    help='set log level to DEBUG, INFO, WARNING, ERROR, or CRITICAL')
args = parser.parse_args()

format_str=f'[%(asctime)s {socket.gethostname()}] %(filename)s:%(funcName)s:%(lineno)s - %(levelname)s: %(message)s'
logging.basicConfig(level=args.loglevel, format=format_str)

logging.debug('This is a DEBUG message')
logging.info('This is an INFO message')
logging.warning('This is a WARNING message')
logging.error('This is an ERROR message')
logging.critical('This is a CRITICAL message')
