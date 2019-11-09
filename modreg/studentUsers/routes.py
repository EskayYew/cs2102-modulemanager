import datetime as datetime
from flask import Blueprint, request, render_template, url_for, redirect
from modreg.studentUsers.forms import BiddingForm
from modreg import db
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_user, current_user, logout_user, login_required

studentUsers = Blueprint('studentUsers', __name__)


@studentUsers.route("/myhome")
# @login_required
def studentHome():
    return render_template('studentUsers/home.html')


@studentUsers.route("/mymodules")
# @login_required
def viewModules():
    # print(current_user.id)
    viewModulesQuery = """ 
    SELECT * FROM Completions
    WHERE id = '""" + current_user.id + "';"

    completedModules = db.engine.execute(viewModulesQuery).fetchall()

    return render_template('studentUsers/viewModules.html', completedModules=completedModules)


@studentUsers.route("/mybids", methods=['POST', 'GET'])
def submitBids():
    form = BiddingForm()
    if form.validate_on_submit():
        requestedMod = form.module.data
        requestedSlot = form.lectureslot.data
        bidTime = datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        valueTuple = (current_user.id, requestedMod, requestedSlot, bidTime)

        bidQuery = """
        INSERT INTO bids 
        (id, modcode, lnum, bid_time) 
        VALUES (%s, %s, %s, %s)"""
        
        db.engine.execute(bidQuery, valueTuple)
        flash('Succesful submission', 'message')
        return redirect(url_for('studentUsers.studentHome'))

    return render_template('studentUsers/submitBids.html', form=form)

@studentUsers.route("/viewbids", methods=['POST', 'GET'])
def viewBids():
    return render_template('studentUsers/viewBids.html')


@studentUsers.route("/myclass")
def viewClasses():
    viewClassQuery = """
    SELECT slots.lnum, slots.modcode, slots.t_start, slots.t_end, slots.day
    FROM gets LEFT OUTER JOIN slots 
    ON slots.modcode=gets.modcode AND slots.lnum=gets.lnum
    WHERE gets.id=%s;
    """
    classes=db.engine.execute(viewClassQuery,current_user.id).fetchall()
    return render_template('studentUsers/viewClasses.html', classes=classes)
