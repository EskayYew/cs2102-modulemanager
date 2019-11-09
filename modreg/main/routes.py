import json
from flask import Blueprint, request, render_template, url_for, redirect
from modreg.main.forms import *
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_user, current_user, logout_user, login_required
from modreg.models import WebUsers
from modreg import db

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    return render_template('main/home.html')

@main.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	query=""" SELECT log_in(%s,%s)"""

	if form.validate_on_submit():
		LoginValue=(form.userName.data, form.password.data)
		attemptedWebUser=WebUsers.query.filter_by(id=form.userName.data).first()

		print(db.engine.execute(query,LoginValue).fetchone()[0])

		if attemptedWebUser and db.engine.execute(query,LoginValue).fetchone()[0]:
			login_user(attemptedWebUser)
			return redirect(url_for('main.home'))
		
		else:
			flash('Login unsuccessful, please check your credentials', 'danger')
	return render_template('/main/login.html',title='Login',form=form)

@main.route("/")
@main.route("/faqpage")
def faq():
    # db.engine.execute("""
    # CREATE OR REPLACE FUNCTION handle_bid()
    # RETURNS TRIGGER AS
    # $hb$
    # BEGIN
	# -- Check if the student had completed the module before or a preclusion
	# IF EXISTS (SELECT 1
	# 		   FROM Completions C
	# 		   WHERE C.id  = new.id AND C.modcode = new.modcode
	# 		  )
	# 	  OR
	# 	  EXISTS (SELECT 1
	# 			  FROM Completions C
	# 			  WHERE C.id = new.id
	# 			  AND EXISTS (SELECT 1
	# 						  FROM Preclusions P
	# 						  WHERE P.modcode = new.modcode AND C.modcode = P.precluded
	# 						 )
	# 			 )
	# THEN
	# 	RETURN (new.id, new.id_req, new.modcode, new.lnum, new.bid_time, False , 'Module/preclusion completed before'::varchar(100));
	# -- If currently subscribing to the mod or a preclusion then don't allow
	# ELSIF EXISTS (SELECT 1
	# 			  FROM Gets C
	# 			  WHERE C.id  = new.id AND C.modcode = new.modcode
	# 			 )
	# 	  OR
	# 	  EXISTS (SELECT 1
	# 			  FROM Gets C
	# 			  WHERE C.id = new.id
	# 			  AND EXISTS (SELECT 1
	# 						  FROM Preclusions P
	# 						  WHERE P.modcode = new.modcode AND C.modcode = P.precluded
	# 						 )
	# 			 )
	# THEN
	# 	RETURN (new.id, new.id_req, new.modcode, new.lnum, new.bid_time, False , 'Module/preclusion currently subscribed to'::varchar(100));
	# --If admin made the bid then all checks below are bypassed
	# ELSIF EXISTS (SELECT 1
	# 		   FROM  Webadmins A
	# 		   WHERE A.id = new.id_req
	# 		  )
	# THEN
	# 	RETURN (new.id, new.id_req, new.modcode, new.lnum, new.bid_time, True , 'Module added by an admin.'::varchar(100));
	# ELSIF (new.id_req <> new.id) -- A student can only bid for herself
	# THEN
	# 	RAISE EXCEPTION 'Error: mismatching IDs';
	# 	RETURN NULL;
	# --If the student is an exchange student then add him/ her
	# ELSIF EXISTS (SELECT 1
	# 		   FROM Exchanges E
	# 		   WHERE E.id = new.id
	# 		  )
	# THEN
	# 	RETURN (new.id, new.id_req, new.modcode, new.lnum, new.bid_time, True , 'Module successfully added'::varchar(100));

	# -- Check if the student has all prerequisites completed
	# ELSIF EXISTS (SELECT 1
	# 			  FROM Prerequisites P
	# 			  WHERE P.want = new.modcode
	# 			  AND NOT EXISTS (SELECT 1
	# 			  				  FROM Completions C
	# 							  WHERE C.modcode = P.need AND C.id = new.id
	# 			  				 )
	#   			 )
	# THEN
	# 	RETURN (new.id, new.id_req, new.modcode, new.lnum, new.bid_time, False , 'Uncompleted prerequisites'::varchar(100));
	# -- Check if the student made request before deadline
	# ELSIF new.bid_time > (SELECT deadline
	# 					  FROM Lectures L
	# 					  WHERE L.lnum = new.lnum AND L.modcode = new.modcode)
	# THEN
	# 	RETURN (new.id, new.id_req, new.modcode, new.lnum, new.bid_time, False , 'Request made after deadline'::varchar(100));

	# -- Check for quota
	# ELSIF (SELECT COUNT(DISTINCT G.id)
	# 	   FROM Gets G
	# 	   WHERE G.lnum = new.lnum AND G.modcode = new.modcode AND G.id <> new.id
	# 	  ) >= (SELECT L.quota
	# 		   FROM Lectures L
	# 		   WHERE L.lnum = new.lnum AND L.modcode = new.modcode
	# 		  )
	# THEN
	# 	/*If the mod belongs to one the student's major faculties
	# 	  	and the student is year 3 or above (i.e compute_year >= 2)
	# 		and the student takes less than 24MCs
	# 	 then she can take it
	# 	*/
	# 	IF EXISTS (SELECT 1
	# 			   FROM Modules M
	# 			   WHERE M.modcode = new.modcode
	# 			   AND EXISTS (SELECT 1
	# 						   FROM (Majoring NATURAL JOIN Majors) AS MM
 	# 						   WHERE MM.id = new.id AND MM.fname = M.fname
	# 			   )

	# 		) AND (compute_year(new.id) > 2) AND (compute_workload(new.id) < 23)

	# 	THEN
	# 		RETURN (new.id, new.id_req, new.modcode, new.lnum, new.bid_time, True , 'Module succesfully added'::varchar(100));

	# 	ELSE
	# 		RETURN (new.id, new.id_req, new.modcode, new.lnum, new.bid_time, False , 'Quota exceeded'::varchar(100));
	# 	END IF;
	# ELSIF (SELECT SS.total
	# 		FROM (SELECT S.id, COALESCE(SUM(GM.workload),0) AS total
	#   		      FROM Students S
    #   			  LEFT JOIN (Gets G NATURAL JOIN Modules M) AS GM
	#   			  ON GM.id = S.id
    #               GROUP BY S.id) AS SS
    #         WHERE SS.id = new.id) - compute_year(new.id) > 23
	# THEN
	# 	RETURN (new.id, new.id_req, new.modcode, new.lnum, new.bid_time, False , 'Maximum workload exceeded'::varchar(100));

	# ELSE
	# 	RETURN (new.id, new.id_req, new.modcode, new.lnum, new.bid_time, True , 'Module successfully added'::varchar(100));

	# END IF;

    # END;
    # $hb$ LANGUAGE plpgsql;
    # CREATE TRIGGER add_bid
    # BEFORE INSERT ON Bids
    # FOR EACH ROW
    # EXECUTE PROCEDURE handle_bid();
    # """)
    return render_template('/main/faq.html')

@main.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('main.home'))
