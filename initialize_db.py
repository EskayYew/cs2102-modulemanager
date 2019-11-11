from modreg import db, create_app

app = create_app()

with app.app_context():
    db.engine.execute("""CREATE TABLE WebUsers (
	id varchar(100) PRIMARY KEY,
	password varchar(100) NOT NULL,
	is_super boolean DEFAULT False NOT NULL
    );
    """)
    db.engine.execute("""
    CREATE TABLE WebAdmins (
	id varchar(100) PRIMARY KEY,
	name varchar(100),
	contact varchar(100),
	FOREIGN KEY (id) REFERENCES webusers ON DELETE CASCADE
    );
    """)
    db.engine.execute("""
    CREATE TABLE Students (
	id varchar(100) PRIMARY KEY,
	name varchar(100) NOT NULL,
	enroll DATE NOT NULL,
	FOREIGN KEY (id) REFERENCES webusers ON DELETE CASCADE ON UPDATE CASCADE
    );
    """)
    db.engine.execute("""
    CREATE TABLE Exchanges (
	id varchar(100) PRIMARY KEY,
	home_country varchar(100) NOT NULL,
	FOREIGN KEY (id) REFERENCES Students ON DELETE CASCADE ON UPDATE CASCADE
    );
    """
                      )
    db.engine.execute("""
    CREATE TABLE Faculties (
	fname varchar(100) PRIMARY KEY
    );
    """)
    db.engine.execute("""
    CREATE TABLE Minors (
	min_name varchar(100) PRIMARY KEY,
	fname varchar(100) DEFAULT 'NUS' NOT NULL REFERENCES Faculties ON DELETE SET DEFAULT
    );  
    """)
    db.engine.execute("""
    CREATE TABLE Majors (
	maj_name varchar(100) PRIMARY KEY,
	fname varchar(100) DEFAULT 'NUS' NOT NULL REFERENCES Faculties ON DELETE SET DEFAULT 
    );
    """)
    db.engine.execute("""
    CREATE TABLE Minoring (
	id varchar(100) NOT NULL REFERENCES Students ON DELETE CASCADE ON UPDATE CASCADE,
	min_name varchar(100) NOT NULL REFERENCES Minors ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (id,min_name)
    );
    """)
    db.engine.execute("""
    CREATE TABLE Majoring (
	id varchar(100) NOT NULL REFERENCES Students ON DELETE CASCADE ON UPDATE CASCADE 
		DEFERRABLE INITIALLY DEFERRED,
	maj_name varchar(100) NOT NULL REFERENCES Majors ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (id,maj_name)
    );
    """)
    db.engine.execute("""
    CREATE TABLE Modules (
	modcode varchar(100) PRIMARY KEY,
	modname varchar(100) NOT NULL,
	descriptions text, 
	fname varchar(100) DEFAULT 'NUS' NOT NULL REFERENCES Faculties ON DELETE SET DEFAULT, 
	workload int NOT NULL
    );
    """)
    db.engine.execute("""
    CREATE TABLE Lectures (
	lnum int NOT NULL,
	modcode varchar(100) NOT NULL REFERENCES Modules ON DELETE CASCADE,
	deadline timestamp with time zone NOT NULL,
	quota int DEFAULT 100 NOT NULL,
	PRIMARY KEY(lnum,modcode)
    );
    """)
    db.engine.execute("""
    CREATE TABLE Slots (
	lnum integer,
	modcode varchar(100),
	day varchar(10),
	t_start time,
	t_end time,
	FOREIGN KEY (lnum, modcode) REFERENCES Lectures,
	PRIMARY KEY(lnum, modcode, day),
	CHECK (t_start < t_end)
    );
    """)
    db.engine.execute("""
    CREATE TABLE Prerequisites(
    want varchar(100) NOT NULL REFERENCES Modules ON DELETE CASCADE,
    need varchar(100) NOT NULL REFERENCES Modules ON DELETE CASCADE CHECK(want <> need),
    PRIMARY KEY(want,need)
    );    
    """)
    db.engine.execute("""
    CREATE TABLE Preclusions(
	modcode varchar(100) NOT NULL REFERENCES Modules ON DELETE CASCADE,
	precluded varchar(100) NOT NULL REFERENCES Modules ON DELETE CASCADE CHECK(precluded <> modcode),
	PRIMARY KEY(modcode,precluded)
    ); 
    """)
    db.engine.execute("""
    CREATE TABLE Bids(
	id varchar(100) NOT NULL REFERENCES Students,
	id_req varchar(100) NOT NULL REFERENCES webusers,
	modcode varchar(100) NOT NULL,
	lnum int NOT NULL,
	bid_time timestamp with time zone,
	status boolean DEFAULT True,
	remark varchar(100) DEFAULT 'Successful bid!',
	PRIMARY KEY(id, id_req, modcode,lnum,bid_time),
	FOREIGN KEY (lnum,modcode) REFERENCES Lectures ON DELETE CASCADE ON UPDATE CASCADE
    ); 
    """)
    db.engine.execute("""
    CREATE TABLE Gets(
	modcode varchar(100),
	lnum int,
	id varchar(100) REFERENCES Students ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY(id,modcode,lnum),
	FOREIGN KEY (lnum,modcode) REFERENCES Lectures ON DELETE CASCADE ON UPDATE CASCADE
    );
    """)
    db.engine.execute("""
    CREATE TABLE Completions(
	id varchar(100) NOT NULL,
	modcode varchar(100) NOT NULL REFERENCES Modules ON UPDATE CASCADE,
	PRIMARY KEY(id, modcode)
    );
    """)
    db.engine.execute("""
    CREATE EXTENSION IF NOT EXISTS pgcrypto;
    CREATE OR REPLACE FUNCTION hash_proc()
    RETURNS TRIGGER AS 
    $aab$
    BEGIN 
	IF (TG_OP = 'UPDATE') AND crypt(NEW.password, gen_salt('bf'))::varchar(100) = OLD.password::varchar(100)
	THEN RETURN NEW;
	ELSE
		RETURN (NEW.id, crypt(NEW.password, gen_salt('bf'))::varchar(100), NEW.is_super);
	END IF;
    END;
    $aab$ LANGUAGE plpgsql;
    CREATE TRIGGER add_user 
    BEFORE INSERT OR UPDATE ON webusers
    FOR EACH ROW 
    EXECUTE PROCEDURE hash_proc();
    """)
    db.engine.execute("""
    CREATE OR REPLACE PROCEDURE create_student_user(
	id varchar(100) DEFAULT NULL, 
	pw varchar(100) DEFAULT NULL, 
	name varchar(100) DEFAULT NULL, 
	enroll date DEFAULT NULL, 
	major varchar(100) DEFAULT NULL, 
	country varchar(100) DEFAULT 'LOCAL') 
    AS
    $csu$
    BEGIN
	INSERT INTO webusers VALUES (id, pw, False);
	INSERT INTO Students VALUES (id, name, enroll);
	INSERT INTO Majoring VALUES (id, major);
	IF country <> 'LOCAL'
	THEN INSERT INTO Exchanges VALUES (id, country);
	END IF;
    EXCEPTION
	WHEN SQLSTATE '23502' THEN 
		RAISE EXCEPTION 'Error: some of the required fields are missing';
		ROLLBACK;
	WHEN SQLSTATE '23503' THEN 
		RAISE EXCEPTION 'Error: an inaccurate major name has been entered';
		ROLLBACK;
	WHEN SQLSTATE '23505' THEN   
		RAISE EXCEPTION 'Error: account with this ID has existed';
		ROLLBACK;
    END;
    $csu$ LANGUAGE plpgsql;
    """)
    db.engine.execute("""
    CREATE OR REPLACE FUNCTION dual_preclusion()
    RETURNS TRIGGER AS
    $a_p$
    BEGIN
	IF TG_OP = 'DELETE' 
	THEN 
		IF EXISTS (SELECT 1
				FROM Preclusions P 
				WHERE P.modcode = old.precluded AND P.precluded = old.modcode
		       )
		THEN	   
			DELETE FROM Preclusions PP
			WHERE PP.modcode = old.precluded AND PP.precluded = old.modcode;
			RETURN NULL;
		ELSE
			RETURN NULL;
		END IF;
	ELSEIF NOT EXISTS (SELECT 1
			   FROM Preclusions P1
			   WHERE P1.modcode = new.precluded AND P1.precluded = new.modcode
			  ) 
	THEN	
		INSERT INTO Preclusions VALUES(new.precluded, new.modcode);
		RETURN NULL;
	ELSE 
		RETURN NULL;
	END IF;
    END;
    $a_p$ LANGUAGE plpgsql;
    CREATE TRIGGER add_preclusion
    AFTER INSERT OR DELETE ON Preclusions
    FOR EACH ROW
    EXECUTE PROCEDURE dual_preclusion();
    """)
    db.engine.execute("""
    CREATE OR REPLACE FUNCTION compute_workload(id varchar(50)) 
    RETURNS int AS
    $c_w$
    BEGIN
	IF NOT EXISTS (SELECT 1 FROM Students S WHERE S.id = id)
	THEN
		RAISE EXCEPTION 'Error: this student does not exist';
	END IF;
	RETURN COALESCE((SELECT SUM(workload)
		  	FROM modules M 
			WHERE EXISTS (SELECT 1
						  FROM Gets G
			              WHERE G.id = id AND M.modcode = G.modcode   
						 )
			), 0);
    END;
    $c_w$ LANGUAGE plpgsql;
    """
    )
    db.engine.execute("""
    CREATE OR REPLACE FUNCTION time_clash(id varchar(100), l integer, code varchar(100)) 
    RETURNS SETOF varchar(100) AS
    $t_c$
    BEGIN
	RETURN QUERY  
		(SELECT M.modcode 
		 FROM Modules M
		 WHERE  
		 		
		 		
		 EXISTS (SELECT 1 
		      	 FROM Slots L1 JOIN Slots L2 ON ((L1.modcode, L1.lnum) <> (L2.modcode, L2.lnum) AND (L1.modcode, L1.lnum) = (code, l) AND L2.modcode = M.modcode)
				                      
				 WHERE L1.d = L2.d AND ((L1.t_end > L2.t_start AND L2.t_start > L1.t_start) OR (L2.t_end > L1.t_start AND L1.t_start > L2.t_start))
				 AND 
			    
			     EXISTS (SELECT 1 
					     FROM Gets G
		 			     WHERE G.id = id AND G.modcode = L2.modcode AND G.lnum = L2.lnum 
		 		        )
		       )
		);		 
	RETURN;
    END
    $t_c$ LANGUAGE plpgsql;
    """)
    db.engine.execute("""
    CREATE OR REPLACE FUNCTION remove_cyclic_prereq()
    RETURNS TRIGGER AS
    $rcp$
    BEGIN
	IF EXISTS 
	  (WITH RECURSIVE Preq(want, need) AS (
		SELECT want, need FROM Prerequisites
		UNION
		SELECT P.want, Pr.need
		FROM Preq P, Prerequisites Pr
		WHERE P.need = Pr.want
	       )
	        SELECT 1 FROM Preq P  
	 		 WHERE P.need = P.want 
	   )
	THEN
		DELETE FROM Prerequisites P WHERE P.want = new.want AND P.need = new.need; 
        RAISE EXCEPTION 'Error: Cyclic dependency detected';
	END IF;
    RETURN NULL;
    END;
    $rcp$ LANGUAGE plpgsql;
    """
    )
    db.engine.execute("""
    CREATE TRIGGER detect_cycle
    AFTER INSERT ON Prerequisites
    FOR EACH ROW
    EXECUTE PROCEDURE remove_cyclic_prereq();
    """)
    db.engine.execute("""
    CREATE OR REPLACE FUNCTION DFS_fulfill(student_id varchar(100), wantt varchar(100), need varchar(100)[])
    RETURNS varchar(100)[] AS
    $DFS$
    DECLARE
	r record;
	mc varchar(100);
	
    BEGIN
	
	FOR r IN (SELECT * FROM Prerequisites PP where PP.want = wantt) LOOP
		mc := r.need;
		IF mc = ANY(DFS_fulfill(student_id, mc, need)) AND mc != ALL(need)
		THEN
			need := need || mc;
		END IF;
	END LOOP;
	IF NOT EXISTS (SELECT 1
				   FROM Completions C
				   WHERE C.modcode = wantt and C.id = student_id
				  )
	THEN
		need := need || wantt;
	END IF;
	RETURN need;
    END; 
    $DFS$ LANGUAGE plpgsql;
    """)
    db.engine.execute("""
    CREATE OR REPLACE FUNCTION findNeededModules(student_id varchar(100), modcode varchar(100))
    RETURNS text AS
    $n$
    DECLARE
	arr varchar(100)[];
    BEGIN
	arr := DFS_fulfill(student_id, modcode, '{}');
	arr := arr[0:array_length(arr, 1)-1];
	RETURN array_to_string(arr,', ');
    END;
    $n$ LANGUAGE plpgsql;    
    """)
    db.engine.execute("""
	CREATE OR REPLACE FUNCTION compute_year(student_id varchar(100))
	RETURNS numeric AS
	$cy$
	BEGIN
		RETURN ROUND(EXTRACT(epoch from(now() - (SELECT enroll
								FROM Students S
								WHERE S.id = student_id
						))/31557600)::numeric, 2);
	END;
	$cy$ LANGUAGE plpgsql;
    """)


    db.engine.execute("""
    CREATE OR REPLACE FUNCTION handle_bid()
    RETURNS TRIGGER AS 
    $hb$
    BEGIN
	
	IF EXISTS (SELECT 1 
			   FROM Completions C 
			   WHERE C.id  = new.id AND C.modcode = new.modcode 
			  )
		  OR
		  EXISTS (SELECT 1
				  FROM Completions C
				  WHERE C.id = new.id 
				  AND EXISTS (SELECT 1 
							  FROM Preclusions P
							  WHERE P.modcode = new.modcode AND C.modcode = P.precluded 
							 )
				 )
	THEN 
		RETURN (new.id, new.id_req, new.modcode, new.lnum, new.bid_time, False , 'Module/preclusion completed before'::varchar(100));
	
	ELSIF EXISTS (SELECT 1 
				  FROM Gets C 
				  WHERE C.id  = new.id AND C.modcode = new.modcode 
				 )
		  OR
		  EXISTS (SELECT 1
				  FROM Gets C
				  WHERE C.id = new.id 
				  AND EXISTS (SELECT 1 
							  FROM Preclusions P
							  WHERE P.modcode = new.modcode AND C.modcode = P.precluded 
							 )
				 )
	THEN
		RETURN (new.id, new.id_req, new.modcode, new.lnum, new.bid_time, False , 'Module/preclusion currently subscribed to'::varchar(100));
	ELSIF EXISTS (SELECT 1
			   FROM webadmins A
			   WHERE A.id = new.id_req 
			  )
	THEN
		RETURN (new.id, new.id_req, new.modcode, new.lnum, new.bid_time, True , 'Module added by an admin.'::varchar(100));	
	ELSIF (new.id_req <> new.id)
	THEN
		RAISE EXCEPTION 'Error: mismatching IDs';
		RETURN NULL;
	ELSIF EXISTS (SELECT 1 
			   FROM Exchanges E
			   WHERE E.id = new.id
			  )
	THEN 
		RETURN (new.id, new.id_req, new.modcode, new.lnum, new.bid_time, True , 'Module successfully added'::varchar(100));
	ELSIF EXISTS (SELECT 1 
				  FROM Prerequisites P
				  WHERE P.want = new.modcode 
				  AND NOT EXISTS (SELECT 1
				  				  FROM Completions C
								  WHERE C.modcode = P.need AND C.id = new.id 
				  				 )
	  			 )
	THEN 
		RETURN (new.id, new.id_req, new.modcode, new.lnum, new.bid_time, False , 'Uncompleted prerequisites'::varchar(100));
	ELSIF new.bid_time > (SELECT deadline 
						  FROM Lectures L
						  WHERE L.lnum = new.lnum AND L.modcode = new.modcode)
	THEN 
		RETURN (new.id, new.id_req, new.modcode, new.lnum, new.bid_time, False , 'Request made after deadline'::varchar(100));
	
	ELSIF (SELECT COUNT(DISTINCT G.id) 
		   FROM Gets G 
		   WHERE G.lnum = new.lnum AND G.modcode = new.modcode AND G.id <> new.id
		  ) >= (SELECT L.quota 
			   FROM Lectures L
			   WHERE L.lnum = new.lnum AND L.modcode = new.modcode
			  )
	THEN 
		IF EXISTS (SELECT 1
				   FROM Modules M
				   WHERE M.modcode = new.modcode 
				   AND EXISTS (SELECT 1
							   FROM (Majoring NATURAL JOIN Majors) AS MM
 							   WHERE MM.id = new.id AND MM.fname = M.fname
				   )
	
			) AND (compute_year(new.id) > 2) AND (compute_workload(new.id) < 23)
		
		THEN
			RETURN (new.id, new.id_req, new.modcode, new.lnum, new.bid_time, True , 'Module succesfully added'::varchar(100));	
		
		ELSE
			RETURN (new.id, new.id_req, new.modcode, new.lnum, new.bid_time, False , 'Quota exceeded'::varchar(100));
		END IF;
	ELSIF (SELECT SS.total
			FROM (SELECT S.id, COALESCE(SUM(GM.workload),0) AS total
	  		      FROM Students S 
      			  LEFT JOIN (Gets G NATURAL JOIN Modules M) AS GM 
	  			  ON GM.id = S.id 
                  GROUP BY S.id) AS SS
            WHERE SS.id = new.id) - compute_year(new.id) > 23
	THEN
		RETURN (new.id, new.id_req, new.modcode, new.lnum, new.bid_time, False , 'Maximum workload exceeded'::varchar(100));
	 
	ELSE
		RETURN (new.id, new.id_req, new.modcode, new.lnum, new.bid_time, True , 'Module successfully added'::varchar(100));
	
	END IF;
    END;
    $hb$ LANGUAGE plpgsql;
    CREATE TRIGGER add_bid
    BEFORE INSERT ON Bids
    FOR EACH ROW
    EXECUTE PROCEDURE handle_bid();
    """)
    db.engine.execute("""
    CREATE OR REPLACE FUNCTION proc_bid()
    RETURNS TRIGGER AS
    $pb$
    BEGIN
	IF (new.status) THEN
		INSERT INTO Gets VALUES (new.modcode, new.lnum, new.id);
	END IF;
	RETURN NULL;
	EXCEPTION
		WHEN SQLSTATE '23503' THEN
			RAISE EXCEPTION 'Error: The lecture slot does not exist ';
		WHEN SQLSTATE '23505' THEN
			RAISE EXCEPTION 'Error: This slot is already allocated to the student';
    END;
    $pb$ LANGUAGE plpgsql;
    CREATE TRIGGER bid_proc
    AFTER INSERT ON Bids
    FOR EACH ROW 
    EXECUTE PROCEDURE proc_bid();
    """)
    db.engine.execute("""
    CREATE OR REPLACE FUNCTION log_in(uid varchar(100), pw varchar(100))
    RETURNS boolean AS
    $log$
    BEGIN
    RETURN EXISTS 
    (SELECT 1 
    FROM webusers U
    WHERE
    U.password = crypt(pw, (select password from webusers u2 WHERE u2.id = uid ))::varchar(100)
    ); 
    END;
    $log$ LANGUAGE plpgsql;
    """)