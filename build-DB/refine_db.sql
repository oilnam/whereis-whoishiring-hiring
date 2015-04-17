/* This is a set of queries needed to make the db consistent */

/* Grouping cities together */

UPDATE job SET location = (SELECT id FROM city WHERE name = 'Zurich')
WHERE location = (SELECT id FROM city WHERE name = 'Zürich');

UPDATE job SET location = (SELECT id FROM city WHERE name = 'New York City')
WHERE location IN (SELECT id FROM city 
      	       	  WHERE name = 'New York'
		  OR name = 'NYC'
		  OR name = 'Manhattan'
		  OR name = 'Brooklyn, NY'
		  OR name = 'NEW YORK'
		  OR name = 'NY, NY'
);

UPDATE job SET location = (SELECT id FROM city WHERE name = 'San Francisco')
WHERE location IN (SELECT id FROM city 
      	          WHERE name = 'SF'
		  OR name = 'SAN FRANCISCO'
);

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

UPDATE job SET location = (SELECT id FROM city WHERE name = 'Boston')
WHERE location IN (SELECT id FROM city 
      	           WHERE name = 'Cambridge, MA'
		   OR name = 'Cambridge MA'
);

UPDATE job SET location = (SELECT id FROM city WHERE name = 'Toronto')
WHERE location = (SELECT id FROM city WHERE name = 'TORONTO');

UPDATE job SET location = (SELECT id FROM city WHERE name = 'Los Angeles')
WHERE location IN (SELECT id FROM city 
      	          WHERE name = 'Venice'
		  OR name = 'Santa Monica'
);

UPDATE job SET location = (SELECT id FROM city WHERE name = 'St. Petersburg')
WHERE location = (SELECT id FROM city WHERE name = 'Saint Petersburg');


UPDATE city SET country = 'Hong Kong' WHERE country = 'HK';

UPDATE city SET country = 'China' WHERE country LIKE '%Republic of China';


/* delete jobs from Dublin that belong to Dublin, Ohio */
/* I hate you MySQL */

CREATE TEMPORARY TABLE the_dubliners AS
SELECT id FROM job WHERE location = 
    (SELECT id FROM city WHERE name = 'Dublin')
AND hn_id IN
    (SELECT hn_id FROM job WHERE location =
        (SELECT id FROM city WHERE name = 'Dublin')
    AND hn_id IN (
        SELECT hn_id FROM job WHERE location =
            (SELECT id FROM city WHERE name = 'Dublin OH')
	)
    );
DELETE FROM job WHERE id IN (SELECT id FROM the_dubliners);



/* Dealing with REMOTE jobs */

/* first, make Remote jobs point to REMOTE */

UPDATE job SET location = (SELECT id FROM city WHERE name = 'REMOTE')
WHERE location = (SELECT id FROM city WHERE name = 'Remote');

/* now, delete jobs from REMOTE which also happen to be in 
   one of the 'no remote' combinations */

CREATE TEMPORARY TABLE no_remote AS
SELECT description FROM job
       WHERE location IN (SELECT id FROM city 
       	     	      	  WHERE name = 'NO REMOTE' OR name = 'REMOTE no'
			  OR name = 'Remote not' OR name = 'No Remote');

DELETE FROM job WHERE description IN (SELECT description FROM no_remote);


/* Dealing with INTERN. Same as with REMOTE */

UPDATE job SET location = (SELECT id FROM city WHERE name = 'INTERN')
WHERE location IN (SELECT id FROM city 
      	       	   WHERE name = 'intern'
		   OR name = 'internship'
		   OR name = 'internships'
);

CREATE TEMPORARY TABLE no_intern AS
SELECT description FROM job
       WHERE location IN (SELECT id FROM city
       	     	      	  WHERE name = 'no internships'
			  OR name = 'No internships'
			  OR name = 'no intern'
);

DELETE FROM job WHERE description IN (SELECT description FROM no_intern);


/* Get rid of duplicates -- this is what I wanted to write */

/*
DELETE FROM job 
WHERE id NOT IN (SELECT MIN(id) FROM job GROUP BY description, location);
*/

/* this is what MySQL wants me to write :/ */

DELETE FROM job
WHERE job.id NOT IN 
(SELECT * FROM (SELECT MIN(job.id) FROM job GROUP BY job.description, job.location) x);

