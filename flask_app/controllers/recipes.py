from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

    #GET
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recipes')
def home():
    if session.get('user_id'):
        user = User.get_one(session['user_id'])
        return render_template('recipes.html', user = user, all_recipes = Recipe.get_all())
    else:
        flash('Please login or create an account')
        return redirect('/')

@app.route('/recipes/<int:recipe_id>')
def view_recipe(recipe_id):
    if session.get('user_id'):
        user = User.get_one(session['user_id'])
        recipe = Recipe.get_one_recipe(recipe_id)
        return render_template('/view_recipe.html', recipe = recipe, user=user)
    else:
        flash('Please login or create an account')
        return redirect('/')

@app.route('/recipes/new')
def new_recipe():
    if session.get('user_id'):
        return render_template('new_recipe.html')
    else:
        flash('Please login or create an account')
        return redirect('/')

@app.route('/recipes/edit/<int:recipe_id>')
def edit_recipe(recipe_id):
    if session.get("user_id"):
        recipe = Recipe.get_one_recipe(recipe_id) 
        return render_template('edit_recipe.html', recipe = recipe)
    else: 
        flash('Please login or create an account')
        return redirect('/')
# POST
@app.route('/recipes/new/recipe', methods=['POST'])
def save_recipe():
    data = {
        "name": request.form['name'],
        'description': request.form['description'],
        "instructions": request.form['instructions'],
        "date_cooked": request.form['date_cooked'],
        'under_30': request.form['under_30'],
        'user_id': session['user_id']
    }
    if not Recipe.validate_recipe(data):
        return redirect('/recipes/new')
    Recipe.create_recipe(data)
    return redirect('/recipes')

@app.route("/recipes/update", methods=["POST"])
def update_recipe():
    print(request.form)
    data = {
        "id": request.form['recipe_id'],
        "name": request.form['name'],
        'description': request.form['description'],
        "instructions": request.form['instructions'],
        "date_cooked": request.form['date_cooked'],
        'under_30': request.form['under_30'],
        'user_id': session['user_id']
    }
    Recipe.update(data)
    return redirect('/recipes')

@app.route('/recipes/<int:recipe_id>/delete')
def delete_recipe(recipe_id):
    Recipe.delete(recipe_id)
    return redirect('/recipes')