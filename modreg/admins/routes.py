import json
from flask import Blueprint, request, render_template, url_for,redirect
from modreg.admins.forms import *
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_user, current_user, logout_user, login_required
from modreg import db

admins = Blueprint('admins', __name__)

@admins.route("/admin/home")
def adminHome():
    return render_template('admin/home.html')

@admins.route("/admin/viewmodules")
def adminViewModule():
    query="""
    SELECT * 
    FROM Modules;
    """
    modules=db.engine.execute(query).fetchall()
    return render_template('admin/viewModules.html',modules=modules)    

@admins.route("/admin/viewlectures/<modcode>")
def adminEditModule(modcode):
    query="""   
    SELECT *
    FROM lectures 
    WHERE modcode=%s;    
    """

    lectures=db.engine.execute(query, modcode).fetchall()
    print(lectures)
    return render_template('admin/viewLectures.html', lectures=lectures, modcode=modcode)

@admins.route("/admin/viewslots/<modcode>/<lnum>")
def adminViewSlots(modcode, lnum):
    slot = (modcode, lnum)

    slotsquery = """
    SELECT * 
    FROM slots
    WHERE modcode=%s AND lnum=%s 
    """
    slots = db.engine.execute(slotsquery, slot).fetchall()

    return render_template('admin/viewSlots.html', slots=slots, modcode=modcode, lnum=lnum)

@admins.route("/admin/viewOneSlot/<modcode>/<lnum>/<day>")
def adminViewOneSlot(modcode, lnum, day):
    slot = (modcode, lnum)

    studentsquery="""
    SELECT S.id, S.name, CEILING(compute_year(S.id)) AS Year 
    FROM Students S NATURAL JOIN Gets G
    WHERE G.modcode = %s AND G.lnum = %s 
    ORDER BY S.name
    """

    students = db.engine.execute(studentsquery, slot).fetchall()
    print(students[0])

    return render_template('admin/viewOneSlot.html', students=students)

@admins.route("/admin/addlecture/<modcode>", methods=['GET','POST'])
def adminAddLecture(modcode):
    form=AddLectureForm()
    if form.validate_on_submit():
        datatuple=(form.lnum.data, modcode, form.quota.data, form.deadline.data)
        query = """
        INSERT INTO lectures
        VALUES (%s,%s,%s,%s);
        """
        db.engine.execute(query,datatuple)
        return redirect(url_for('admins.adminEditModule', modcode=modcode))
    
    return render_template('admin/addLecture.html', form=form, modcode=modcode)

@admins.route("/admin/addslot/<modcode>/<lnum>", methods=['GET','POST'])
def adminAddSlot(modcode,lnum):
    form=AddSlotForm()
    if form.validate_on_submit():
        datatuple=(lnum, modcode, form.t_start.data, form.t_end.data, form.day.data)
        query = """
        INSERT INTO slots
        VALUES (%s,%s,%s,%s,%s);
        """
        db.engine.execute(query,datatuple)
        return redirect(url_for('admins.adminViewSlots', modcode=modcode))
    
    return render_template('admin/addSlot.html', form=form, lnum=lnum, modcode=modcode)
    


    