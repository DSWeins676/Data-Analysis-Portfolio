LOAD DATA LOCAL INFILE "D:\\FARS Data\\states_vmt.csv" INTO TABLE states
FIELDS terminated by ','
ENCLOSED BY '"'
ignore 1 rows;

LOAD DATA LOCAL INFILE 'D:\\FARS Data\\ncsa_makes.csv' INTO TABLE ncsa_makes
FIELDS terminated by ','
ENCLOSED BY '"'
ignore 1 rows;

LOAD DATA LOCAL INFILE 'D:\\FARS Data\\county.csv' INTO TABLE counties
FIELDS terminated by ','
ENCLOSED BY '"'
ignore 1 rows;

LOAD DATA LOCAL INFILE 'D:\\FARS Data\\restraint.csv' INTO TABLE restraints
FIELDS terminated by ','
ENCLOSED BY '"'
ignore 1 rows;

LOAD DATA LOCAL INFILE 'D:\\FARS Data\\Crashes.csv' INTO TABLE crashes
FIELDS terminated by ','
ENCLOSED BY '"'
ignore 1 rows;

LOAD DATA LOCAL INFILE 'D:\\FARS Data\\vehicle.csv' INTO TABLE vehicles
FIELDS terminated by ','
ENCLOSED BY '"'
ignore 1 rows;

LOAD DATA LOCAL INFILE 'D:\\FARS Data\\People.csv' INTO TABLE people
FIELDS terminated by ','
ENCLOSED BY '"'
ignore 1 rows;
