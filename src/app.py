import os
from flask import Flask, render_template
from src.views.alerts import alert_blueprint
from src.views.stores import store_blueprint
from src.views.users import user_blueprint

__author__ = 'benbrown'

app = Flask(__name__)
app.secret_key = 'asiughsdf78tew87tgr3g7fewiugfesdsfiojsdioferu89wy45328yhwe8hfa8fe9hoijh321n'
app.config.update(
    ADMIN=os.environ.get('ADMIN')
)


@app.route('/')
def home():
    return render_template('home.html')


app.register_blueprint(alert_blueprint, url_prefix="/alerts")
app.register_blueprint(store_blueprint, url_prefix="/stores")
app.register_blueprint(user_blueprint, url_prefix="/users")


if __name__ == '__main__':
    app.run()