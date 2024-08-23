import os

from flask import Flask, render_template, request, session, redirect, url_for, flash
from utils.db import *
from datetime import datetime, date

app = Flask(__name__)
app.secret_key = 'secret_key'

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if check_credentials(username, password):
            session['username'] = username
            return redirect(url_for('carts'))
        else:
            flash('Invalid username or password', 'danger')
    if 'username' in session:
        return redirect(url_for('carts'))
    return render_template('index.html')


@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']
        budget = request.form['budget']
        birthday = request.form['birthday']

        if not check_username(username):
            flash('Username already taken', 'danger')
            return render_template('register.html')

        if password != confirm:
            flash('Passwords must match', 'danger')
            return render_template('register.html')

        if not budget:
            flash('Please set a starting budget', 'danger')
            return render_template('register.html')

        if datetime.strptime(birthday, '%Y-%m-%d').date() > date.today():
            flash('Please enter a valid birthday', 'danger')
            return render_template('register.html')

        register_user(username, budget, date.today(), birthday, password)
        flash('Successfully registered new user %s!' % username, 'success')
        return redirect(url_for('index'))

    return render_template('register.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/carts", methods=["GET", "POST"])
def carts():
    if 'username' not in session:
        return redirect(url_for('index'))

    if request.method == "POST":
        cart_name = request.form['cartName']
        create_new_cart(session['username'], cart_name)

    user_carts = execute_query_file('get_carts', session['username'])
    user_budget = get_budget(session['username'])
    return render_template('carts.html', carts=user_carts, budget=user_budget)

@app.route("/carts/<cart_id>", methods=["GET","POST"])
def cart_page(cart_id):
    if 'username' not in session:
        return redirect(url_for('index'))

    if request.method == "POST":
        notes = request.form['notes']
        update_cart_notes(cart_id, notes)

    cart_details = get_cart_details(cart_id)
    user_permission = get_user_permission(cart_id, session['username'])
    return render_template('cart_page.html', cart=cart_details, permission=user_permission)

@app.route("/CPU")
def CPU():
    editable_carts = execute_query_file('get_editable_carts', session['username'])
    return render_template('cpu.html', cpus=get_cpus(), carts=editable_carts)

@app.route("/GPU")
def GPU():
    editable_carts = execute_query_file('get_editable_carts', session['username'])
    return render_template('gpu.html', gpus=get_gpus(), carts=editable_carts)

@app.route("/Trending_CPU")
def Trending_CPU():
    editable_carts = execute_query_file('get_editable_carts', session['username'])
    return render_template('trending_cpu.html', tren_cpus=get_trending_cpus(), carts=editable_carts)

@app.route("/Trending_GPU")
def Trending_GPU():
    editable_carts = execute_query_file('get_editable_carts', session['username'])
    return render_template('trending_gpu.html', tren_gpus=get_trending_gpus(), carts=editable_carts)

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        query = request.form['search']
        results = execute_query_file('search', (query, query, query, query))
        return render_template('search.html', search_results=results)

    return redirect(url_for('index'))

@app.route("/carts/<cart_id>/update_cpu/<cpu_name>")
def update_CPU(cart_id, cpu_name):
    set_cpu(cart_id, cpu_name)
    return redirect(url_for('cart_page', cart_id=cart_id))

@app.route("/carts/<cart_id>/update_gpu/<gpu_name>")
def update_GPU(cart_id, gpu_name):
    set_gpu(cart_id, gpu_name)
    return redirect(url_for('cart_page', cart_id=cart_id))

@app.route("/carts/<cart_id>/delete_cpu")
def delete_CPU(cart_id):
    remove_cpu(cart_id)
    return redirect(url_for('cart_page', cart_id=cart_id))

@app.route("/carts/<cart_id>/delete_gpu")
def delete_GPU(cart_id):
    remove_gpu(cart_id)
    return redirect(url_for('cart_page', cart_id=cart_id))

@app.route("/carts/<cart_id>/delete_cart")
def delete_cart(cart_id):
    remove_cart(cart_id)
    return redirect(url_for('carts'))

@app.route("/sign_out")
def sign_out():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('index'))

@app.route("/test")
def test():
    query = test_query()
    return str(query)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
