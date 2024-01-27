from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, recipe # import entire file, rather than class, to avoid circular imports
# As you add model files add them the the import above
# This file is the second stop in Flask's thought process, here it looks for a route that matches the request



# Create Users Controller

@app.post('/recipes/create')
def create_new_recipe():
    if 'user_id' not in session: return redirect('/')
    print(request.form)
    if recipe.Recipe.create_new_recipe(request.form):
        return redirect('/recipes') # redirect to the show page
    return redirect('/recipe/create')


# Read Users Controller



@app.get('/recipes')
def display_recipes_page():
    print(session, "This is session") 
    if 'user_id' not in session: return redirect('/')
    user_data = session['first_name']
    recipe_data = recipe.Recipe.get_all_recipes_with_creator()
    return render_template('recipes.html', user = user_data, recipes = recipe_data )
    
@app.get('/recipe/create')
def display_create_recipe_page():
    if 'user_id' not in session: return redirect('/')
    return render_template('create_recipe.html')

@app.get('/recipe/edit/<int:recipe_id>')
def display_edit_recipe_page(recipe_id):
    if 'user_id' not in session: return redirect('/')
    recipe_data = recipe.Recipe.get_one_recipe_with_creator(recipe_id)
    return render_template('edit_recipe.html', recipe=recipe_data)

@app.get('/recipes/<int:recipe_id>')
def display_one_recipe(recipe_id):
    if 'user_id' not in session: return redirect('/')
    print(recipe_id)
    one_recipe = recipe.Recipe.get_one_recipe_with_creator(recipe_id)
    print(one_recipe, "this is one recipe!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1")
    return render_template('recipes_show.html', recipe = one_recipe)

# Update Users Controller

@app.post('/recipes/edit/<int:recipe_id>')
def edit_one_recipe(recipe_id):
    if 'user_id' not in session: return redirect('/')
    recipe.Recipe.update_one_recipe(request.form, recipe_id)
    return redirect('/recipes')
    # return redirect('/recipe/edit/<int:recipe_id>')

# Delete Users Controller
@app.get('/recipe/delete/<int:recipe_id>')
def delete_one_recipe(recipe_id):
    if 'user_id' not in session: return redirect('/')
    recipe.Recipe.delete_user_recipe(recipe_id)
    return redirect('/recipes')



# Notes:
# 1 - Use meaningful names
# 2 - Do not overwrite function names
# 3 - No matchy, no worky
# 4 - Use consistent naming conventions 
# 5 - Keep it clean
# 6 - Test every little line before progressing
# 7 - READ ERROR MESSAGES!!!!!!
# 8 - Error messages are found in the browser and terminal




# How to use path variables:
# @app.route('/<int:id>')                                   The variable must be in the path within angle brackets
# def index(id):                                            It must also be passed into the function as an argument/parameter
#     user_info = user.User.get_user_by_id(id)              The it will be able to be used within the function for that route
#     return render_template('index.html', user_info)

# Converter -	Description
# string -	Accepts any text without a slash (the default).
# int -	Accepts integers.
# float -	Like int but for floating point values.
# path 	-Like string but accepts slashes.

# Render template is a function that takes in a template name in the form of a string, then any number of named arguments containing data to pass to that template where it will be integrated via the use of jinja
# Redirect redirects from one route to another, this should always be done following a form submission. Don't render on a form submission.