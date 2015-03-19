/* updates with sqlalchemy are a f pain */

/* makes Z\xfcrich point to Zurich */
UPDATE job
SET location = 976
WHERE location = 449;

/* makes New York point to New York City */
UPDATE job
SET location = 173
WHERE location = 970;

/* makes NYC point to New York City */
UPDATE job
SET location = 173
WHERE location = 968;

/* makes Manhattan point to New York City */
UPDATE job
SET location = 173
WHERE location = 1007;

/* makes Brooklyn, NY point to New York City */
UPDATE job
SET location = 173
WHERE location = 1024;

/* makes NEW YORK point to New York City */
UPDATE job
SET location = 173
WHERE location = 1041;

/* makes SF point to San Francisco */
UPDATE job
SET location = 24
WHERE location = 971;

/* makes SAN FRANCISCO point to San Francisco */
UPDATE job
SET location = 24
WHERE location = 1040;

/* makes Delhi point to New Delhi */
UPDATE job
SET location = 739
WHERE location = 960;

/* makes Padova point to Padua */
UPDATE job
SET location = 1005
WHERE location = 1006;

/* makes St Paul point to Saint Paul */
UPDATE job
SET location = 1029
WHERE location = 1028;	

/* makes Milano point to Milan */
UPDATE job
SET location = 455
WHERE location = 1036;

/* makes LONDON point to London */
UPDATE job
SET location = 397
WHERE location = 1039;

/* makes SEATTLE point to Seattle */
UPDATE job
SET location = 25
WHERE location = 1042;

/* sad but true in tech lol */
UPDATE city
SET country = 'United States'
WHERE name = 'Venice';

UPDATE city
SET country = 'Hong Kong'
WHERE country = 'HK';

UPDATE city
SET country = 'China'
WHERE country LIKE '%Republic of China';

/* manually delete false positives */
DELETE FROM job WHERE id IN (
3130, 6456, 4746, 6445, 6436, 7793, 2792, 4764, 4795, 5113, 1151,
6547, 7507, 7508, 4064, 4850, 6076, 30, 4765, 3725, 4065, 4799, 6751,
2297, 2298, 2299, 2300, 3963, 4643, 2334, 386, 2993, 2793,
6935, 1666, 2317, 6347, 977, 4670, 7794, 7795, 5193, 4018, 4019, 4020,
213, 6616, 6555, 5744, 5745, 7556, 4953, 6407, 2176, 4563,
4564, 3774, 5299, 2825, 4862, 51, 1750, 1751, 1752, 4151, 6437, 1334, 1247,
4793, 4794, 3487, 3617, 3943, 4040, 4041, 4042, 4043, 4044, 4045, 4046,
7569, 3961, 3962, 3215, 1147, 1148, 1149, 1150, 4907 );


/* deleting <NO REMOTE>, <REMOTE no> jobs and
   <REMOTE> jobs which appears in one of the other two */
DELETE FROM job
WHERE description IN (SELECT description FROM job
      WHERE location = 1009 OR location = 1010);


/* get rid of duplicates */
DELETE FROM job 
WHERE id NOT IN (SELECT MIN(id) FROM job GROUP BY description, location);

