CREATE TABLE Users (
	uid varchar(100) PRIMARY KEY,
	password varchar(100) NOT NULL,
	is_super boolean DEFAULT False NOT NULL
);
CREATE TABLE Admins (
	uid varchar(100) PRIMARY KEY,
	name varchar(100),
	contact varchar(100), -- Can display relevant people in-charge
	FOREIGN KEY (uid) REFERENCES Users ON DELETE CASCADE
);

CREATE TABLE Students (
	uid varchar(100) PRIMARY KEY,
	name varchar(100) NOT NULL,
	cap numeric DEFAULT 0 ,
	enroll date NOT NULL,
	FOREIGN KEY (uid) REFERENCES Users ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Exchanges (
	uid varchar(100) PRIMARY KEY,
	home_country varchar(100) ,
	FOREIGN KEY (uid) REFERENCES Students ON DELETE CASCADE ON UPDATE CASCADE
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
	uid varchar(100) NOT NULL REFERENCES Students ON DELETE CASCADE ON UPDATE CASCADE,
	min_name varchar(100) NOT NULL REFERENCES Minors ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (uid,min_name)
);
--Has major   trigger needed to ensure that each student has a major
CREATE TABLE Majoring (
	uid varchar(100) NOT NULL REFERENCES Students ON DELETE CASCADE ON UPDATE CASCADE 
		DEFERRABLE INITIALLY DEFERRED,
	maj_name varchar(100) NOT NULL REFERENCES Majors ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY (uid,maj_name)
);

CREATE TABLE Modules (
	modcode varchar(100) PRIMARY KEY,
	modname varchar(100) NOT NULL,
	fname varchar(100) DEFAULT 'NUS' NOT NULL REFERENCES Faculties ON DELETE SET DEFAULT -- faculty owns a module
);

CREATE TABLE Lectures (
	lnum int NOT NULL,
	modcode varchar(100) NOT NULL REFERENCES Modules ON DELETE CASCADE, -- module covers the slot
	deadline timestamp with time zone NOT NULL,
	quota int DEFAULT 100 NOT NULL,
	t_start time,
	t_end time CHECK (t_end > t_start),
	PRIMARY KEY(lnum,modcode)
);

CREATE TABLE Prerequisites(
	modcode varchar(100) NOT NULL REFERENCES Modules ON DELETE CASCADE,
	prereq varchar(100) NOT NULL REFERENCES Modules ON DELETE CASCADE CHECK(prereq <> modcode),
	PRIMARY KEY(modcode,prereq)
);

CREATE TABLE Preclusions(
	modcode varchar(100) NOT NULL REFERENCES Modules ON DELETE CASCADE,
	precluded varchar(100) NOT NULL REFERENCES Modules ON DELETE CASCADE CHECK(precluded <> modcode),
	PRIMARY KEY(modcode,precluded)
); -- trigger here to add preclusion in opposite direction

CREATE TABLE Bids(
	uid varchar(100) NOT NULL REFERENCES Students ON DELETE CASCADE ON UPDATE CASCADE,
	modcode varchar(100) NOT NULL,
	lnum int NOT NULL,
	bid_time timestamp with time zone,
	status boolean DEFAULT True,
	remark varchar(100) DEFAULT 'Successful bid!',
	FOREIGN KEY (lnum,modcode) REFERENCES Lectures ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY(uid,modcode,lnum,bid_time)
); -- Bids

CREATE TABLE Gets(
	uid varchar(100) NOT NULL NOT NULL REFERENCES Students ON DELETE CASCADE ON UPDATE CASCADE,
	modcode varchar(100) NOT NULL,
	lnum int NOT NULL,
	is_audit boolean DEFAULT false,
	FOREIGN KEY (lnum,modcode) REFERENCES Lectures ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY(uid,modcode,lnum)
);

CREATE TABLE Completions(
	uid varchar(100) NOT NULL,
	modcode varchar(100) NOT NULL REFERENCES Modules ON UPDATE CASCADE,
	PRIMARY KEY(uid, modcode)
);