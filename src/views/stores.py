import json
from flask import Blueprint, render_template, request, url_for, redirect
from src.models.store import Store
from src.models.user.decorators import requires_login, requires_admin

__author__ = 'benbrown'

store_blueprint = Blueprint('stores', __name__)


@store_blueprint.route('/')
@requires_login
def index():
    stores = Store.all()
    return render_template('stores/index.html', stores=stores)


@store_blueprint.route('/new', methods=['GET', 'POST'])
@requires_admin
def create_store():
    # Added three "query" fields to accommodate source pages breaking up price into separate pieces
    # If nothing is passed in by the user, query2 and query 3 will be null
    # query1 = currency (XXX of $XXX.CC)
    # query2 = currency percentile separator (. of $XXX.CC)
    # query3 = currency remainder (CC of $XXX.CC)
    if request.method == 'POST':
        name = request.form['name']
        url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        query1 = json.loads(request.form['query1'])
        # If query2 and/or query 3 are not populated, use null
        # Otherwise, use json.loads to properly format the html for storage in Mongo
        if request.form['query2']:
            query2 = json.loads(request.form['query2'])
        else:
            query2 = None
        if request.form['query3']:
            query3 = json.loads(request.form['query3'])
        else:
            query3 = None

        Store(name, url_prefix, tag_name, query1, query2, query3).save_to_mongo()

    return render_template('stores/new_store.html')


@store_blueprint.route('/edit/<string:store_id>', methods=['GET', 'POST'])
@requires_admin
def edit_store(store_id):
    store = Store.get_by_id(store_id)

    if request.method == 'POST':
        # Added three "query" fields to accommodate source pages breaking up price into separate pieces
        # If nothing is passed in by the user, query2 and query 3 will default to "." and "99", respectively
        # query1 = currency (XXX of $XXX.CC)
        # query2 = currency percentile separator (. of $XXX.CC)
        # query3 = currency remainder (CC of $XXX.CC)
        name = request.form['name']
        url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        query1 = json.loads(request.form['query1'])
        # If query2 and/or query 3 are not populated, store null
        # Otherwise, use json.loads to properly format the html for storage in Mongo
        if request.form['query2']:
            query2 = json.loads(request.form['query2'])
        else:
            query2 = None
        if request.form['query3']:
            query3 = json.loads(request.form['query3'])
        else:
            query3 = None

        store.name = name
        store.url_prefix = url_prefix
        store.tag_name = tag_name
        store.query1 = query1
        store.query2 = query2
        store.query3 = query3

        store.save_to_mongo()

        return redirect(url_for('.index'))

    return render_template('stores/edit_store.html', store=store)


@store_blueprint.route('/delete/<string:store_id>')
@requires_admin
def delete_store(store_id):
    Store.get_by_id(store_id).remove_from_mongo()
    return redirect(url_for('.index'))
