from flask import render_template, request, url_for, redirect, session, flash, request
from flask_app import app
from flask_app.models import pal

@app.route('/new/pal', methods=['POST'])
def new_pal():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    selected_user_id = session.get('selected_user_id')
    data = {
        'first_name': request.form.get('first_name'),
        'last_name': request.form.get('last_name'),
        'ranking': request.form.get('ranking'),
        'user_id': user_id
    }
    if pal.Pal.save(data):
        flash("Friend added successfully", "success")
    else:
        flash("Friend already exists", "mark")
    return redirect(url_for('view_user', id=selected_user_id))

@app.route('/pals')
def pals():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    friends = pal.Pal.get_friends_by_user(user_id)
    return render_template('pals.html', friends=friends)

# @app.route('/delete/pal/<int:friend_id>')
# def delete_pal(friend_id):
#     user_id = session.get('user_id')
#     if not user_id:
#         return redirect(url_for('login'))
#     if pal.Pal.delete_friend(user_id, friend_id):
#         return redirect(url_for('pals'))
#     else:
#         return redirect(url_for('pals'))


@app.route('/delete/pal/<int:friend_id>', methods=['GET', 'POST'])
def delete_pal(friend_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    
    if pal.Pal.delete_friend(user_id, friend_id):
        return redirect(url_for('pals'))
    else:
        return redirect(url_for('pals'))
