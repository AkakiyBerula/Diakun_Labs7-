from flask import current_app as app
from flask import Flask, render_template, request, flash
from flask_bootstrap import Bootstrap
from datetime import datetime
from platform import platform
from sys import version

def get_footer():
    footer_data = {
        "platform": platform(),
        "request": request.user_agent,
        "python_version": version,
        "datetime": datetime.now().strftime('%d/%m/%Y %H:%M')
    }
    return footer_data

@app.route('/')
def index():
    data = "Main Page"
    title = "Головна сторінка"
    subtitle = "Опис навігаційного меню"
    footer_form = get_footer()
    return render_template('index.html', 
        data = data, 
        title = title,
        subtitle = subtitle,
        footer_form = footer_form
    )

@app.errorhandler(404)
def not_found(error):
    flash("The resource requested could not be found on this server!", category="warning")
    return render_template("404.html", title = "Error 404")
    