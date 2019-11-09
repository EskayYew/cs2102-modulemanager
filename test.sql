SELECT modcode 
FROM Modules as new 
WHERE NOT EXISTS (
(SELECT 1 FROM Completions C WHERE C.id  = 'A001' AND C.modcode = new.modcode ) OR EXISTS 
(SELECT 1 FROM Completions C WHERE C.id = 'A001' AND EXISTS (SELECT 1 FROM Preclusions P WHERE P.modcode = new.modcode AND C.modcode = P.precluded ));


INSERT INTO Lectures (lnum, modcode, deadline, quota) VALUES
(1, 'CS2103', '2019-11-28 00:09:09', 100),
(1, 'CS2102A', '2019-11-28 00:09:09', 100),
(2, 'CS2104', '2019-11-28 00:09:09', 100),
(2, 'CS2100', '2019-11-28 00:09:09', 100),
(2, 'CS3243', '2019-11-28 00:09:09', 100),
(2, 'MA1101R', '2019-11-28 00:09:09', 100),
(1, 'CS2104', '2019-11-28 00:09:09', 2);

INSERT INTO slots (lnum, modcode, day, t_start, t_end) VALUES
(2, 'CS2104', 'Monday', '09:00:00', '11:00:00'),
(2, 'CS3243', 'Monday', '10:00:00', '12:00:00'),
(1, 'CS2102A', 'Monday', '09:00:00', '11:00:00'),
(1, 'CS2103', 'Monday', '12:00:00', '14:00:00'),
(2, 'MA1101R', 'Monday', '14:00:00', '15:00:00'),
(1, 'CS2103', 'Friday', '09:00:00', '11:00:00'),
(1, 'CS2102A', 'Friday', '09:00:00', '11:00:00'),
(1, 'CS2103', 'Tuesday', '11:00:00', '11:30:00'),
(2, 'CS3243', 'Tuesday', '10:00:00', '12:00:00');