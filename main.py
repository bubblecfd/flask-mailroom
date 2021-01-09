import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session
from peewee import fn

from model import Donor, Donation

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)

@app.route('/create/', methods=['GET', 'POST'])
def create_donation():
    if request.method == 'GET':
        return render_template('create_donation.jinja2')
    
    if request.method == 'POST':
        try:
            #name = Donor.select().where(fn.Lower(Donor.name)== request.form['name'].lower()).get()
            name = Donor.get(fn.Lower(Donor.name) == request.form['name'].lower())
            Donation(donor=name, value=int(request.form['amount'])).save()
            return redirect(url_for('home'))
        except:
            return render_template('create_donation.jinja2', error="Donor does not exist.")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

