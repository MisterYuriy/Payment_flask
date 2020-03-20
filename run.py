import logging
from logging.handlers import RotatingFileHandler

from pay import app

handler_debug = RotatingFileHandler('debug.log', maxBytes=1024 * 1024)
logging.getLogger('werkzeug').setLevel(logging.DEBUG)
logging.getLogger('werkzeug').addHandler(handler_debug)

handler_payments = RotatingFileHandler('payments.log', maxBytes=1024 * 1024)
handler_payments.setFormatter(logging.Formatter('%(asctime)s -  %(levelname)s - %(message)s'))
app.logger.setLevel(logging.INFO)
app.logger.addHandler(handler_payments)

app.run(host='localhost', port='8888')