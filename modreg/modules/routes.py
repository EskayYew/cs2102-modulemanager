import json
from flask import Blueprint, request, render_template, url_for,redirect
from modreg.modules.forms import *
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_user, current_user, logout_user, login_required
from modreg.models import WebUsers
from modreg import db

modules = Blueprint('modules', __name__)

@modules.route("/viewmodule/<modcode>")
def viewModule(modcode):
    #query for module using mod code
    modcode=modcode 
    query = "SELECT * FROM modules WHERE modcode=%s LIMIT 1"

    preclusion_query = """
    SELECT * 
    FROM preclusions 
    WHERE modcode=%s
    """
    prereq_query = """
    SELECT *
    FROM prerequisites
    WHERE want=%s;
    """

    preclude_mods = db.engine.execute(preclusion_query, modcode).fetchall()
    prereq_mods = db.engine.execute(prereq_query, modcode).fetchall()
    thisModule = db.engine.execute(query, modcode).fetchall()
    return render_template('modules/module.html', thisModule=thisModule, prereq_mods=prereq_mods, preclude_mod=preclude_mods)