/* This is a set of queries needed to make the db consistent */

/* Grouping cities together */

UPDATE job SET location = (SELECT id FROM city WHERE name = 'Zurich')
WHERE location = (SELECT id FROM city WHERE name = 'Z\xfcrich');

UPDATE job SET location = (SELECT id FROM city WHERE name = 'New York City')
WHERE location = (SELECT id FROM city WHERE name = 'New York');

UPDATE job SET location = (SELECT id FROM city WHERE name = 'New York City')
WHERE location = (SELECT id FROM city WHERE name = 'NYC');

UPDATE job SET location = (SELECT id FROM city WHERE name = 'New York City')
WHERE location = (SELECT id FROM city WHERE name = 'Manhattan');

UPDATE job SET location = (SELECT id FROM city WHERE name = 'New York City')
WHERE location = (SELECT id FROM city WHERE name = 'Brooklyn, NY');

UPDATE job SET location = (SELECT id FROM city WHERE name = 'New York City')
WHERE location = (SELECT id FROM city WHERE name = 'NEW YORK');

UPDATE job SET location = (SELECT id FROM city WHERE name = 'New York City')
WHERE location = (SELECT id FROM city WHERE name = 'NY, NY');

UPDATE job SET location = (SELECT id FROM city WHERE name = 'San Francisco')
WHERE location = (SELECT id FROM city WHERE name = 'SF');

UPDATE job SET location = (SELECT id FROM city WHERE name = 'San Francisco')
WHERE location = (SELECT id FROM city WHERE name = 'SAN FRANCISCO');

UPDATE job SET location = (SELECT id FROM city WHERE name = 'New Delhi')
WHERE location = (SELECT id FROM city WHERE name = 'Delhi');

UPDATE job SET location = (SELECT id FROM city WHERE name = 'Padua')
WHERE location = (SELECT id FROM city WHERE name = 'Padova');

UPDATE job SET location = (SELECT id FROM city WHERE name = 'Saint Paul')
WHERE location = (SELECT id FROM city WHERE name = 'St Paul');

UPDATE job SET location = (SELECT id FROM city WHERE name = 'Milan')
WHERE location = (SELECT id FROM city WHERE name = 'Milano');

UPDATE job SET location = (SELECT id FROM city WHERE name = 'London')
WHERE location = (SELECT id FROM city WHERE name = 'LONDON');

UPDATE job SET location = (SELECT id FROM city WHERE name = 'Seattle')
WHERE location = (SELECT id FROM city WHERE name = 'SEATTLE');

UPDATE job SET location = (SELECT id FROM city WHERE name = 'REMOTE')
WHERE location = (SELECT id FROM city WHERE name = 'Remote');

/* sad but true in tech lol */
UPDATE city SET country = 'United States' WHERE name = 'Venice';

UPDATE city SET country = 'Hong Kong' WHERE country = 'HK';

UPDATE city SET country = 'China' WHERE country LIKE '%Republic of China';


/* deleting <NO REMOTE>, <REMOTE no> jobs and
   <REMOTE> jobs which appears in one of the other two */

CREATE TEMPORARY TABLE no_remote AS
SELECT description FROM job
       WHERE location IN (SELECT id FROM city 
       	     	      	  WHERE name = 'NO REMOTE' OR name = 'REMOTE no'
			  OR name = 'Remote not' OR name = 'No Remote');

DELETE FROM job WHERE description IN (SELECT description FROM no_remote);


/* get rid of duplicates -- this is what I wanted to write */

/*
DELETE FROM job 
WHERE id NOT IN (SELECT MIN(id) FROM job GROUP BY description, location);
*/

/* this is what MySQL wants me to write :/ */
DELETE FROM job
WHERE job.id NOT IN 
(SELECT * FROM (SELECT MIN(job.id) FROM job GROUP BY job.description, job.location) x);

