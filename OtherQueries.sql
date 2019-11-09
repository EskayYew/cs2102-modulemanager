userid = 'A001'
user = db.engine.execute("SELECT * FROM webusers where uid='" + userid + "' LIMIT 1;" )

SELECT * 
FROM webusers
WHERE uid='login'
LIMIT 1;

INSERT INTO bids (id, modcode, lnum, bid_time) VALUES ('A001', 'CS1010E', 1, '2019-12-11 12:00:00');
INSERT INTO gets VALUES ('A001', 'A001', 'CS1010E', 1, False);
DATETIME - format: YYYY-MM-DD HH:MI:SS

WITH CTE AS (
SELECT  modcode as modcode, lnum as lnum FROM gets WHERE id='A001' 
)

SELECT * FROM lectures, CTE
WHERE lectures.modcode=CTE.modcode AND lectures.lnum=CTE.lnum;

SELECT slots.lnum, slots.modcode, slots.t_start, slots.t_end, slots.day
FROM gets LEFT OUTER JOIN slots ON slots.modcode=gets.modcode AND slots.lnum=gets.lnum
WHERE gets.id='A001';

SELECT slots.lnum, slots.modcode, slots.t_start, slots.t_end, slots.day
FROM gets LEFT OUTER JOIN slots ON slots.modcode=gets.modcode AND slots.lnum=gets.lnum
WHERE gets.id='A001';

SELECT *
FROM lectures NATURAL JOIN slots
WHERE modcode='CS1010E'
ORDER BY lectures.lnum;



INSERT INTO slots VALUES (1, 'CS1010E', '10:00:00', '12:00:00', 'Monday');
INSERT INTO slots VALUES (1, 'CS1010E', '16:00:00', '18:00:00', 'Friday');

INSERT INTO webusers VALUES ('B001','password',True);
INSERT INTO webadmins VALUES ('B001', 'Mr Admin', 'Contact me at School of Computing Office');

INSERT INTO webusers VALUES
('A002', 'pandaA002', false),
('A003', 'pandaA003', false),
('A004', 'pandaA004', false),
('A005', 'pandaA005', false),
('A006', 'pandaA006', false),
('A007', 'pandaA007', false),
('A008', 'pandaA008', false),
('A009', 'pandaA009', false),
('A010', 'pandaA010', false),
('A011', 'pandaA011', false),
('A012', 'pandaA012', false),
('A013', 'pandaA013', false),
('A014', 'pandaA014', false),
('A015', 'pandaA015', false),
('A016', 'pandaA016', false),
('A017', 'pandaA017', false),
('A018', 'pandaA018', false),
('A019', 'pandaA019', false),
('A020', 'pandaA020', false),
('E001', 'pandaE001', false),
('E002', 'pandaE002', false),
('E003', 'pandaE003', false),
('E004', 'pandaE004', false),
('E005', 'pandaE005', false),
('E006', 'pandaE006', false),
('E007', 'pandaE007', false),
('E008', 'pandaE008', false),
('E009', 'pandaE009', false),
('Z001', 'pandaZ001', true),
('Z002', 'pandaZ002', true),
('Z003', 'pandaZ003', true);

INSERT INTO Majors VALUES 
('Mathematics', 'Department of Mathematics'), 
('Computer Engineering', 'School of Computing');

INSERT INTO Faculties VALUES ('Department of Mathematics'), ('School of Computing');

INSERT INTO Modules VALUES
('CS2102A', 'Intro to Database', 'The aim of this module is to introduce the fundamental concepts and techniques necessary for the understanding and practice of design and implementation of database applications and of the management of data with relational database management systems. The module covers practical and theoretical aspects of design with entity-relationship model, theory of functional dependencies and normalisation by decomposition in second, third and Boyce-Codd normal forms. The module covers practical and theoretical aspects of programming with SQL data definition and manipulation sublanguages, relational tuple calculus, relational domain calculus and relational algebra.', 'School of Computing', 4),
('CS2103', 'Software Engineering', '','School of Computing', 4),
('CS2104', 'Programming Language', '','School of Computing', 4),
('CS2100', 'Computer Organization','', 'School of Computing', 4),
('CS3243', 'Intro to AI','', 'School of Computing', 4),
('MA1101R', 'Linear Algebra','', 'Department of Mathematics', 5),
('CS2102', 'Intro to Database', 'The aim of this module is to introduce the fundamental concepts and techniques necessary for the understanding and practice of design and implementation of database applications and of the management of data with relational database management systems. The module covers practical and theoretical aspects of design with entity-relationship model, theory of functional dependencies and normalisation by decomposition in second, third and Boyce-Codd normal forms. The module covers practical and theoretical aspects of programming with SQL data definition and manipulation sublanguages, relational tuple calculus, relational domain calculus and relational algebra.', 'School of Computing', 4),
('CS2040', 'Data Structures and Algorithms', '', 'School of Computing', 4),
('MA1101', 'Lenient Algebra', '', 'Department of Mathematics', 5);

INSERT INTO  Prerequisites VALUES ('MA1101R' ,'CS3243' );

INSERT INTO completions VALUES 
('A001', 'CS2040'),
('A012', 'MA1101');


SELECT findNeededModules('A001', 'CS2040');


SELECT modcode 
FROM Modules as new 
WHERE NOT EXISTS (
(SELECT 1 FROM Completions C WHERE C.id  = 'A001' AND C.modcode = new.modcode ) OR EXISTS 
(SELECT 1 FROM Completions C WHERE C.id = 'A001' AND EXISTS (SELECT 1 FROM Preclusions P WHERE P.modcode = new.modcode AND C.modcode = P.precluded ));


WHERE NOT EXISTS (SELECT 1 
				  FROM Prerequisites P
				  WHERE P.want = new.modcode 
				  AND NOT EXISTS (SELECT 1
				  				  FROM Completions C
								  WHERE C.modcode = P.need AND C.id = 'A001'
				  				 )
	  			 );
