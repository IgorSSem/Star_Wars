create_table = "
CREATE TABLE 'hangars' ('hangar_id' TEXT,'type_of_aircraft' TEXT,'aircraft_in_hangar' INTEGER);"
insert_data = "
INSERT INTO 'hangars' ('hangar_id','type_of_aircraft','aircraft_in_hangar') VALUES
 ('R2-C1','X-Wing','3'),
 ('R2-C1','Jedi Starfighter','1'),
 ('R2-C4','X-Wing','2'),
 ('R2-C6','X-Wing','2'),
 ('R2-C6','B-Wing','2'),
 ('R5-D4','X-Wing','4'),
 ('R5-D4','Jedi Starfighter','2'),
 ('R5-D4','B-Wing','3'),
 ('R5-D4','Slave 1','1'),
 ('R5-D8','B-Wing','2'),
 ('R5-D8','Slave 1','2'),
 ('R5-D11','Slave 1','1'),
 ('R9-G3','X-Wing','5'),
 ('R9-G3','Jedi Starfighter','1'),
 ('R9-G3','B-Wing','2'),
 ('R9-G8','Slave 1','1'),
 ('R9-G11','B-Wing','2'),
 ('R9-G13','X-Wing','3'),
 ('R9-G13','B-Wing','4');
"
available_aircraft = "SELECT sum(aircraft_in_hangar) as cnt_a FROM hangars;"
most_popular_aircraft = "
SELECT type_of_aircraft, sum(aircraft_in_hangar) as Amount
FROM hangars
GROUP BY type_of_aircraft
ORDER BY Amount DESC
Limit 1;"
largest_number_of_aircraft = "SELECT hangar_id
FROM
(SELECT hangar_id, type_of_aircraft, SUM(aircraft_in_hangar) as Amount
FROM hangars
GROUP BY hangar_id
ORDER BY Amount DESC)
Limit 1;"
add_floor = "ALTER TABLE hangars
ADD COLUMN floor text;"
update_floor = "UPDATE hangars SET floor = substr(hangar_id, 0, 2);"