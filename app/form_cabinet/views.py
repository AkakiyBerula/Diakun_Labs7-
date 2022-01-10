from flask import render_template, url_for, flash, redirect, request, session
from flask_bootstrap import Bootstrap
from .. import bootstrap
from json import load, dump, decoder
from .forms import LoginForm, RegistrationForm

from . import form_cabinet_blueprint

def add_info(validate):
    dictionary = {}
    data = {
        validate.login.data: { "password" : validate.password.data, "number_e" : validate.number.data,
            "pin_e" : validate.pin.data,
            "year_of_receive": validate.year.data,
            "diplom_serial": validate.diplom_serial.data,
            "diplom_number" : validate.diplom_number.data
        }
    }
    try:
        with open("registers.json", "r") as file:
            dictionary = load(file)
            dictionary.update(data)

        with open("registers.json", "w", encoding="utf-8") as write_file:
            dump(dictionary, write_file, ensure_ascii = False, indent = 4)

    except FileNotFoundError or decoder.JSONDecodeError:
        with open("registers.json", "w", encoding="utf-8") as write_file:
            dump(data, write_file, ensure_ascii = False, indent = 4)

@form_cabinet_blueprint.route('/basic_form', methods=['GET', 'POST'])
def basic_form():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Дані занесені успішно!')
        flash('The username is ' + form.username.data + ". The password is " + form.password.name + "!")
        return redirect(url_for('form_cabinet.basic_form'))
    return render_template('basic_form.html', form=form)

@form_cabinet_blueprint.route('/form_cabinet', methods=['GET', 'POST'])
def form_cabinet():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Дані занесені успішно!')
        add_info(form)
        session['login'] = form.login.data
        session['number'] = form.number.data
        session['pin'] = form.pin.data
        session['year'] = form.year.data
        session['diplom_serial'] = form.diplom_serial.data
        session['diplom_number'] = form.diplom_number.data
        return render_template('form_cabinet.html', 
                            form=form,
                            login=session.get("login"),
                            number=session.get("number"),
                            pin=session.get("pin"),
                            year=session.get("year"),
                            diplom_serial=session.get("diplom_serial"),
                            diplom_number=session.get("diplom_number"),)
    elif not form.validate_on_submit():
        flash('Дані не було внесено!')
    return render_template('form_cabinet.html', 
                            form=form,
                            login=session.get("login"),
                            number=session.get("number"),
                            pin=session.get("pin"),
                            year=session.get("year"),
                            diplom_serial=session.get("diplom_serial"),
                            diplom_number=session.get("diplom_number"),)