CREATE TABLE webusers (
	id varchar(100) PRIMARY KEY,
	password varchar(100) NOT NULL,
	is_super boolean DEFAULT False NOT NULL
);

CREATE TABLE WebAdmins (
	id varchar(100) PRIMARY KEY,
	name varchar(100),
	contact varchar(100), -- Can display relevant people in-charge
	FOREIGN KEY (id) REFERENCES webusers ON DELETE CASCADE
);

CREATE TABLE Students (
	id varchar(100) PRIMARY KEY,
	name varchar(100) NOT NULL,
	--Remove cap, it's hard to calculate. cap numeric DEFAULT 0 ,
	enroll DATE NOT NULL,
	FOREIGN KEY (id) REFERENCES webusers ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Exchanges (
	id varchar(100) PRIMARY KEY,
	home_country varchar(100) NOT NULL,
	FOREIGN KEY (id) REFERENCES Students ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Faculties (
	fname varchar(100) PRIMARY KEY
);

CREATE TABLE Minors (
	min_name varchar(100) PRIMARY KEY,
	fname varchar(100) DEFAULT 'NUS' NOT NULL REFERENCES Faculties ON DELETE SET DEFAULT -- minor belongs to
);

CREATE TABLE Majors (
	maj_name varchar(100) PRIMARY KEY,
	fname varchar(100) DEFAULT 'NUS' NOT NULL REFERENCES Faculties ON DELETE SET DEFAULT -- major belongs to
);
--Has minor
CREATE TABLE Minoring (
	id varchar(100) NOT NULL REFERENCES Students ON DELETE CASCADE ON UPDATE CASCADE,
	min_name varchar(100) NOT NULL REFERENCES Minors ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (id,min_name)
);
--Has major   trigger needed to ensure that each student has a major
CREATE TABLE Majoring (
	id varchar(100) NOT NULL REFERENCES Students ON DELETE CASCADE ON UPDATE CASCADE 
		DEFERRABLE INITIALLY DEFERRED,
	maj_name varchar(100) NOT NULL REFERENCES Majors ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (id,maj_name)
);

CREATE TABLE Modules (
	modcode varchar(100) PRIMARY KEY,
	modname varchar(100) NOT NULL,
	description text, 
	fname varchar(100) DEFAULT 'NUS' NOT NULL REFERENCES Faculties ON DELETE SET DEFAULT, -- faculty owns a module,	
	workload int NOT NULL
);

CREATE TABLE Lectures (
	lnum int NOT NULL,
	modcode varchar(100) NOT NULL REFERENCES Modules ON DELETE CASCADE, -- module covers the slot
	deadline timestamp with time zone NOT NULL,
	quota int DEFAULT 100 NOT NULL,
	PRIMARY KEY(lnum,modcode)
);

-- Weak entity Slots created to represent the time slots for each lecture slot.
CREATE TYPE mood AS ENUM ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday');

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

-- make sure that mood is defined


CREATE TABLE Prerequisites(
	want varchar(100) NOT NULL REFERENCES Modules ON DELETE CASCADE,
	need varchar(100) NOT NULL REFERENCES Modules ON DELETE CASCADE CHECK(want <> need),
	PRIMARY KEY(want,need)
);

CREATE TABLE Preclusions(
	modcode varchar(100) NOT NULL REFERENCES Modules ON DELETE CASCADE,
	precluded varchar(100) NOT NULL REFERENCES Modules ON DELETE CASCADE CHECK(precluded <> modcode),
	PRIMARY KEY(modcode,precluded)
); -- trigger here to add preclusion in opposite direction

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

CREATE TABLE Gets(
	modcode varchar(100),
	lnum int,
	id varchar(100) REFERENCES Students ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY(id,modcode,lnum),
	FOREIGN KEY (lnum,modcode) REFERENCES Lectures ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Completions(
	id varchar(100) NOT NULL,
	modcode varchar(100) NOT NULL REFERENCES Modules ON UPDATE CASCADE,
	PRIMARY KEY(id, modcode)
);

INSERT INTO webusers VALUES ('sample','sample');
