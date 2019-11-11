import datetime as datetime
from flask import Blueprint, request, render_template, url_for, redirect
from modreg.studentUsers.forms import BiddingForm
from modreg import db
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import exc


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
    idTuple=(current_user.id,current_user.id,current_user.id)
    query = """
    SELECT modcode 
    FROM Modules as new 
    WHERE NOT EXISTS 
    
    (SELECT 1 
    FROM Completions C 
    WHERE C.id  = %s
    AND C.modcode = new.modcode 

    OR EXISTS (SELECT 1 
                FROM Completions C 
                WHERE C.id = %s
                AND EXISTS (SELECT 1 FROM Preclusions P WHERE P.modcode = new.modcode AND C.modcode = P.precluded ))
    )
    AND NOT EXISTS 
    (SELECT 1 FROM Prerequisites P WHERE P.want = new.modcode AND NOT EXISTS (SELECT 1 FROM Completions C WHERE C.modcode = P.need AND C.id = %s))
    AND EXISTS
    (SELECT 1 FROM lectures l WHERE new.modcode = l.modcode)
    ;
    """

    modules = db.engine.execute(query, idTuple).fetchall()
    form = BiddingForm()

    if form.validate_on_submit():
        requestedMod = form.module.data
        requestedSlot = form.lectureslot.data
        bidTime = datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        valueTuple = (current_user.id, current_user.id, requestedMod, requestedSlot, bidTime)

        bidQuery = """
        INSERT INTO bids 
        (id,id_req, modcode, lnum, bid_time) 
        VALUES (%s, %s, %s, %s, %s)"""

        db.engine.execute(bidQuery, valueTuple)

        # try:
        #     db.engine.execute(bidQuery, valueTuple)
        # except exc.SQLAlchemyError:
        #     flash('Bid submission not successful. please make sure you have entered the correct details', 'message')
        #     return redirect(url_for('studentUsers.submitBids'))
            
        flash('Bid submitted, please check your bidding result', 'message')
        return redirect(url_for('studentUsers.studentHome'))

    return render_template('studentUsers/submitBids.html', form=form, modules=modules)


@studentUsers.route("/viewbids", methods=['POST', 'GET'])
def viewBids():
    query="""
    SELECT * 
    FROM bids
    WHERE bids.id=%s;
    """
    bids=db.engine.execute(query, current_user.id).fetchall()
    return render_template('studentUsers/viewBids.html', bids=bids)


@studentUsers.route("/myclass")
def viewClasses():
    viewClassQuery = """
    SELECT slots.lnum, slots.modcode, slots.t_start, slots.t_end, slots.day
    FROM gets LEFT OUTER JOIN slots 
    ON slots.modcode=gets.modcode AND slots.lnum=gets.lnum
    WHERE gets.id=%s;
    """
    classes = db.engine.execute(viewClassQuery, current_user.id).fetchall()
    return render_template('studentUsers/viewClasses.html', classes=classes)

@studentUsers.route("/student/viewallmodules")
def viewAllModules():
    query="""
    SELECT * 
    FROM Modules;
    """
    modules=db.engine.execute(query).fetchall()
    return render_template('studentUsers/viewAllModules.html',modules=modules)   
