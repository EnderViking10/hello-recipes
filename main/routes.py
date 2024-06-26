import os

from flask import render_template, redirect, url_for, current_app
from flask_login import login_required
from werkzeug.utils import secure_filename

from app import db
from main import bp
from main.forms import RecipeForm
from models import Recipe, Instruction, Ingredient


@bp.route('/')
def index() -> render_template:
    return render_template('index.html')


@bp.route("/recipes")
def all_recipes():
    recipes = Recipe.query.all()
    return render_template('recipes.html', recipes=recipes)


@bp.route('/recipe/<int:id>')
def recipe(id):
    specific_recipe = Recipe.query.get_or_404(id)
    return render_template('recipe.html', recipe=specific_recipe)


@bp.route('/new_recipe', methods=['GET', 'POST'])
@login_required
def new_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        image_file = form.image.data
        if image_file:
            image_filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(current_app.root_path, 'static/uploads', image_filename))
            new_recipe = Recipe(title=form.title.data, description=form.description.data, image_file=image_filename)
        else:
            new_recipe = Recipe(title=form.title.data, description=form.description.data)

        ingredients = form.ingredients.data.split('\n')  # Split the textarea content by new line
        for ingredient in ingredients:
            name, measurement = ingredient.split(':')  # Assuming name and measurement are divided by space
            new_ingredient = Ingredient(name=name, measurement=measurement, recipe=new_recipe)
            db.session.add(new_ingredient)

        instructions = form.instructions.data.split('\n')  # Split the textarea content by new line
        for instruction in instructions:
            new_instruction = Instruction(step=instruction, recipe=new_recipe)
            db.session.add(new_instruction)

        db.session.commit()

        return redirect(url_for('main.all_recipes'))
    return render_template('new_recipe.html', title='New Recipe', form=form)
