/* updates with sqlalchemy are a f pain */

/* makes Z\xfcrich point to Zurich */
UPDATE job SET location = 976 WHERE location = 449;

/* makes New York point to New York City */
UPDATE job SET location = 173 WHERE location = 970;

/* makes NYC point to New York City */
UPDATE job SET location = 173 WHERE location = 968;

/* makes Manhattan point to New York City */
UPDATE job SET location = 173 WHERE location = 1007;

/* makes Brooklyn, NY point to New York City */
UPDATE job SET location = 173 WHERE location = 1024;

/* makes NEW YORK point to New York City */
UPDATE job SET location = 173 WHERE location = 1041;

/* makes SF point to San Francisco */
UPDATE job SET location = 24 WHERE location = 971;

/* makes SAN FRANCISCO point to San Francisco */
UPDATE job SET location = 24 WHERE location = 1040;

/* makes Delhi point to New Delhi */
UPDATE job SET location = 739 WHERE location = 960;

/* makes Padova point to Padua */
UPDATE job SET location = 1005 WHERE location = 1006;

/* makes St Paul point to Saint Paul */
UPDATE job SET location = 1029 WHERE location = 1028;	

/* makes Milano point to Milan */
UPDATE job SET location = 455 WHERE location = 1036;

/* makes LONDON point to London */
UPDATE job SET location = 397 WHERE location = 1039;

/* makes SEATTLE point to Seattle */
UPDATE job SET location = 25 WHERE location = 1042;

/* sad but true in tech lol */
UPDATE city SET country = 'United States' WHERE name = 'Venice';

UPDATE city SET country = 'Hong Kong' WHERE country = 'HK';

UPDATE city SET country = 'China' WHERE country LIKE '%Republic of China';


/* deleting <NO REMOTE>, <REMOTE no> jobs and
   <REMOTE> jobs which appears in one of the other two */
DELETE FROM job
WHERE description IN (SELECT description FROM job
      WHERE location = 1009 OR location = 1010);


/* get rid of duplicates */
DELETE FROM job 
WHERE id NOT IN (SELECT MIN(id) FROM job GROUP BY description, location);

