from flask import url_for, render_template, flash, request, redirect, abort, current_app
from .forms import PostsForm
from .models import Posts
from .. import db
from flask_login import login_user, current_user, logout_user, login_required
from . import posts_blueprint
import os
import secrets
from PIL import Image
from datetime import datetime


@posts_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def view_posts():
    form = PostsForm()
    posts = Posts.query.all()
    return render_template('posts_crud.html', posts_list = posts, form = form, user_id = current_user.id)


@posts_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostsForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            image = picture_file
        else:
            image = "postdefault.jpg"
            
        new_post = Posts(title = form.title.data, 
                        text = form.text.data,
                        image_file = image,
                        type = form.type.data,
                        user_id = current_user.id)

        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('posts.view_posts'))
    posts = Posts.query.all()
    return render_template('create_post.html', posts = posts, form = form)


@posts_blueprint.route('/<id>', methods=['GET', 'POST'])
def show_post(id):
    print(id)
    post = Posts.query.get_or_404(id)
    return render_template('post_details.html', post = post)


@posts_blueprint.route('/<id>/delete', methods=['GET', 'POST'])
def delete_post(id):
    post = Posts.query.get_or_404(id)
    if current_user.id == post.user_id:
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('posts.view_posts'))
    flash('Це не ваш пост', category='warning')
    return redirect(url_for('contracts.detail_info_contract', id = post.user_id))


@posts_blueprint.route('/<id>/edit', methods=['GET', 'POST'])
def edit_post(id):
    post = Posts.query.get_or_404(id)
    if current_user.id != post.user_id:
        flash('Це договір не є вашим!', category='warning')
        return redirect(url_for('contracts.detail_info_contract', posts = post, id = id))
    form = PostsForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.text = form.text.data
        post.type = form.type.data
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            post.image_file = picture_file
        else:
            post.image_file = "postdefault.jpg"
        post.enabled = form.enabled.data

        db.session.add(post)
        db.session.commit()

        flash('Пост був оновлений', category='access')
        return redirect(url_for('posts.view_posts', id = id))
    form.title.data = post.title 
    form.text.data = post.text
    form.type.data = post.type
    form.enabled.data = post.enabled

    image_file = url_for("static", filename = "posts_pics/" + post.image_file)
    return render_template('create_post.html', form = form, posts_list = post, image_file = image_file)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/posts_pics', picture_fn)
    output_size = (250, 250)

    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn