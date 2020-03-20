from datetime import datetime
from requests import post
from hashlib import sha256
from flask import abort, render_template, request, redirect

from pay import app
from pay.models import db, Payments


def get_sign(*args):
    args_string = ":".join(args) + app.config['SECRET_KEY']
    return sha256(args_string.encode('utf-8')).hexdigest()


@app.route('/')
def index():
    return render_template("mainForm.html")


@app.route('/action', methods=['POST'])
def action():
    currency = request.form.get('payCurrency')
    amount = request.form.get('payAmount')
    description = request.form.get('description')
    shop_id = app.config['SHOP_ID']
    shop_order_id = app.config['SHOP_ORDER_ID']
    payway = app.config['PAYWAY']
    payment_id = 0
    payment = Payments(amount, currency, payment_id, description, datetime.now())

    if currency == '978':
        pay = {"url": app.config['PAY_URL'],
               "amount": amount,
               "currency": currency,
               "shop_id": shop_id,
               "shop_order_id": shop_order_id,
               "description": description,
               "sign": get_sign(amount, currency, shop_id, shop_order_id),
               }
        app.logger.info('{};{};{};{}'.format(payment_id, currency, amount, description))
        db.session.add(payment)
        db.session.commit()

        return render_template("payForm.html", pay=pay)

    elif currency == '840':
        params = {"payer_currency": currency,
                "shop_amount": amount,
                "shop_currency": currency,
                "shop_id": shop_id,
                "shop_order_id": shop_order_id,
                "description": description,
                "sign": get_sign(currency, amount, currency, shop_id, shop_order_id),
                }
        response = post(app.config['PIASTRIX_URL'], json=params).json()

        payment_id = response.get('data').get('id')
        app.logger.info('{};{};{};{}'.format(payment_id, currency, amount, description))
        payment.payment_id = payment_id
        db.session.add(payment)
        db.session.commit()

        return redirect(response.get('data').get('url'), code=302)

    elif currency == '643':
        params= {"amount": amount,
                "currency": currency,
                "payway": payway,
                "shop_id": shop_id,
                "shop_order_id": shop_order_id,
                "description": description,
                "sign": get_sign(amount, currency, payway, shop_id, shop_order_id),
                }
        response = post(app.config['INVOICE_URL'], json=params)
        data = response.json().get('data')
        invoice = data.get('data')
        invoice['url'] = data.get('url')
        invoice['method'] = data.get('method')

        payment_id = data.get('id')
        app.logger.info('{};{};{};{}'.format(payment_id, currency, amount, description))
        payment.payment_id = payment_id
        db.session.add(payment)
        db.session.commit()

        return render_template("invoiceForm.html", invoice=invoice)

    app.logger.warning('{};{};{};{} WARNING UNKNOWN CURRENCY'.format(payment_id,
                                                                       currency,
                                                                       amount,
                                                                       description))
    abort(404)
