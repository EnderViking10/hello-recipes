import os

from flask import render_template, redirect, url_for, current_app
from werkzeug.utils import secure_filename

from app import db
from main import bp
from main.forms import RecipeForm
from models import Recipe


@bp.route('/')
def index() -> render_template:
    return render_template('index.html')


# at the top of your routes.py or your main Python file
from flask import render_template


@bp.route("/recipes")
def all_recipes():
    recipes = Recipe.query.all()
    return render_template('recipes.html', recipes=recipes)


@bp.route('/recipe/<int:id>')
def recipe(id):
    specific_recipe = Recipe.query.get_or_404(id)
    return render_template('recipe.html', recipe=specific_recipe)


@bp.route('/new_recipe', methods=['GET', 'POST'])
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
        db.session.add(new_recipe)
        db.session.commit()

        return redirect(url_for('main.all_recipes'))
    return render_template('new_recipe.html', title='New Recipe', form=form)
