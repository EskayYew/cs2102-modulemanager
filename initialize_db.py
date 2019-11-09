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
	fname varchar(100) DEFAULT 'NUS' NOT NULL REFERENCES Faculties ON DELETE SET DEFAULT -- minor belongs to
    );  
    """)
    db.engine.execute("""
    CREATE TABLE Majors (
	maj_name varchar(100) PRIMARY KEY,
	fname varchar(100) DEFAULT 'NUS' NOT NULL REFERENCES Faculties ON DELETE SET DEFAULT -- major belongs to
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
	description text, 
	fname varchar(100) DEFAULT 'NUS' NOT NULL REFERENCES Faculties ON DELETE SET DEFAULT, -- faculty owns a module,	
	workload int NOT NULL
    );
    """)
    db.engine.execute("""
    CREATE TABLE Lectures (
	lnum int NOT NULL,
	modcode varchar(100) NOT NULL REFERENCES Modules ON DELETE CASCADE, -- module covers the slot
	deadline timestamp with time zone NOT NULL,
	quota int DEFAULT 100 NOT NULL,
	PRIMARY KEY(lnum,modcode)
    );
    """)
    db.engine.execute("""
    CREATE TABLE Slots (
	lnum integer,
	modcode varchar(100),
	d varchar(10),
	t_start time,
	t_end time,
	FOREIGN KEY (lnum, modcode) REFERENCES Lectures,
	PRIMARY KEY(lnum, modcode, d),
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
