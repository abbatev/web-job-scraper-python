from flask_app import app
from flask_app.models import user, listing
from flask import render_template, request, redirect, session


#dashboard
@app.route('/dashboard/')
def dashboard():
    if 'logged_in_id' not in session:
        return redirect('/')
    data={
        'user_id': session['logged_in_id']
    }
    return render_template('dashboard.html', all_listings=listing.Listing.get_all_listings(), one_user=user.User.get_user_by_id(data))

#create page
@app.route('/new/listing/')
def new_listing():
    return render_template('new_listing.html')

#create form data
@app.route('/create/listing/', methods=['POST'])   
def save_listing():
    if not listing.Listing.validate_listing(request.form):
        return redirect('/new/listing/')
    listing.Listing.create_listing(request.form)
    return redirect('/dashboard')

#Edit form populate existing data
@app.route('/edit/<int:id>')
def edit_listing(id):
    data={
        'id':id
    }
    return render_template('edit_listing.html', one_listing=listing.Listing.get_one_listing(data))

#update form validation and data
@app.route('/update/listing/', methods=['POST'])
def update_listing():
    if not listing.Listing.validate_listing(request.form):
        return redirect(f'/edit/{request.form["id"]}')
    listing.Listing.update_listing(request.form)
    return redirect(f'/show/{request.form["id"]}')

#view page
@app.route('/show/<int:id>')
def view_listing(id): 
    if 'logged_in_id' not in session:
        return redirect('/')
    data={
        'id':id, 
        'user_id': session['logged_in_id']
    }
    
    return render_template('view_listing.html', one_listing=listing.Listing.get_one_listing(data), one_user=user.User.get_user_by_id(data))

#delete
@app.route('/delete/', methods=['POST'])
def delete_listing():
    listing.Listing.delete_listing(request.form)
    return redirect('/dashboard')
