from datetime import datetime, timedelta
import yfinance as yf
import numpy as np

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from stockpicker.auth import login_required
from stockpicker.db import get_db

bp = Blueprint('dashboard', __name__)

# Connect the Index View to the Dashboard
@bp.route('/')
def index():
    db = get_db()
    titles = db.execute(
        'SELECT t.id, symbol, amount, bought, owner_id, username'
        ' FROM title t JOIN user u ON t.owner_id = u.id'
        ' ORDER BY bought DESC'
    ).fetchall()
    return render_template('dashboard/index.html', titles=titles)

@bp.route('/buy', methods=('GET', 'POST'))
@login_required
def buy():
    if request.method == 'POST':
        symbol = request.form['symbol']
        amount = request.form['amount']
        bought = request.form['bought']
        error = None

        if not symbol:
            error = 'Ticker Symbol is required.'

        if not amount:
            error = 'Amount is required.'

        try: 
            bought = datetime.strptime(bought, '%Y-%m-%d') #+ timedelta(seconds=0)
        except Exception:
            error = 'Buying date has to be in format yyyy-mm-dd.'

        # try: 
        #     dt.strptime(bought_time, '%Y-%m-%d')
        # except Exception:
        #     error = 'Buying date has to be in format yyyy-mm-dd.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO title (symbol, amount, bought, owner_id)'
                ' VALUES (?, ?, ?, ?)',
                (symbol, amount, bought, g.user['id'])
            )
            db.commit()
            return redirect(url_for('dashboard.index'))

    return render_template('dashboard/buy.html')

def get_title(id, check_owner=True):
    """Returns title for title_id"""
    title = get_db().execute(
        'SELECT t.id, symbol, amount, bought, owner_id, username'
        ' FROM title t JOIN user u ON t.owner_id = u.id'
        ' WHERE t.id = ?',
        (id,)
    ).fetchone()

    if title is None:
        abort(404, "Title id {0} doesn't exist.".format(id))

    if check_owner and title['owner_id'] != g.user['id']:
        abort(403)

    return title

@bp.route('/<int:id>/sell', methods=('GET', 'POST'))
@login_required
def sell(id):
    title = get_title(id)

    if request.method == 'POST':
        symbol = request.form['symbol']
        amount = request.form['amount']
        error = None

        if not symbol:
            error = 'Ticker Symbol is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE title SET symbol = ?, amount = ?'
                ' WHERE id = ?',
                (symbol, amount, id)
            )
            db.commit()
            return redirect(url_for('dashboard.index'))

    return render_template('dashboard/sell.html', title=title)

# TODO: write function for add savin plan
#       add function for buy title
#       addfunction for selling titles 


@bp.route('/add_savin_plan', methods=('GET', 'POST'))
@login_required
def add_saving_plan():
    if request.method == 'POST':
        symbol = request.form['symbol']
        first_buy = request.form['first_buy']
        last_buy = request.form['last_buy']
        interval = int(request.form['interval'])
        value = request.form['value']
        error = None

        # TODO: check if the input for ticker symbol is correct

        if not symbol:
            error = 'Ticker Symbol is required.'
        if not interval:
            error = 'Interval is required.'
        if not value:
            error = 'Value is required.'

        try: 
            first_buy = datetime.strptime(first_buy, '%Y-%m-%d')
            last_buy = datetime.strptime(last_buy, '%Y-%m-%d')
        except Exception:
            error = 'Buying date has to be in format yyyy-mm-dd.'

        try:
            value = float(value)
        except Exception:
            error = 'Value must be an number'

        if error is not None:
            flash(error)
        else:
            # prepare data for input in database (use yfinance)
            ticker_df = yf.Ticker(symbol).history(
                start=first_buy-timedelta(days=1), 
                end=last_buy+timedelta(days=2)
                )
            ref_date = first_buy

            db = get_db()

            while (ref_date < last_buy):
                # Add titles to database with looping through saving plan intervals
                # calculate day-specific value by calculating the mean price
                
                # use new date instead of ref_date
                new_date = ref_date

                # skip some days, when buy-day is on the weekend, here result is nan
                while (ticker_df[ticker_df.index == new_date.strftime("%Y-%m-%d")][["Open", "High", "Low", "Close"]].mean().mean() == np.nan):
                    new_date = new_date + timedelta(days=1)

                amount = value / ticker_df[ticker_df.index == new_date.strftime("%Y-%m-%d")][["Open", "High", "Low", "Close"]].mean().mean()
                
                print(new_date)
                db.execute(
                    'INSERT INTO title (symbol, amount, bought, owner_id)'
                    ' VALUES (?, ?, ?, ?)',
                    (symbol, 20.00, new_date.strftime("%Y-%m-%d"), g.user['id'])
                )
                db.commit()
                ref_date = ref_date + timedelta(days=interval)
            return redirect(url_for('dashboard.index'))

    return render_template('dashboard/add_saving_plan.html')