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

INSERT INTO slots VALUES (1, 'CS1010E', '10:00:00', '12:00:00', 'Monday');
INSERT INTO slots VALUES (1, 'CS1010E', '16:00:00', '18:00:00', 'Friday');