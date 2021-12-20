CREATE VIEW CrimeView AS
SELECT
    Cr.crime_id,
    Inc.incident_id,
    Inc.occurrence_date,
    Cd.code,
    Cd.organization,
    Cd.category,
    Cd.description AS code_description,
    Inc.type,
    Inc.status,
    Inc.police_department,
    Cr.weapon,
    Cr.domestic,
    Cr.description,
    Lo.location_id,
    Lo.latitude,
    Lo.longitude,
    Lo.premises,
    Lo.area,
    Lo.precinct,
    Lo.ward,
    Lo.borough,
    Lo.city,
    Lo.state,
    Lo.country,
    Cr.victim_id,
    Ps.first_name AS victim_first_name,
    Ps.last_name AS victim_last_name,
    Ps.age_range AS victim_age_range,
    Ps.gender AS victim_gender,
    Ps.ethnicity AS victim_ethnicity,
    Ps.phone_number AS victim_phone_number
FROM
    Crime AS Cr
    LEFT JOIN Incident AS Inc
    USING (incident_id)
    LEFT JOIN Location AS Lo
    USING (location_id)
    LEFT JOIN Code AS Cd
    USING (code, organization)
    LEFT JOIN Person AS Ps
    ON Cr.victim_id = Ps.person_id;

CREATE VIEW ComplaintView AS
SELECT
    Co.complaint_id,
    Inc.incident_id,
    Inc.occurrence_date,
    Co.reported_date,
    Cd.code,
    Cd.organization,
    Cd.category,
    Cd.description AS code_description,
    Inc.type,
    Inc.status,
    Inc.police_department,
    Co.description,
    Lo.location_id,
    Lo.latitude,
    Lo.longitude,
    Lo.premises,
    Lo.area,
    Lo.precinct,
    Lo.ward,
    Lo.borough,
    Lo.city,
    Lo.state,
    Lo.country
FROM
    Complaint AS Co
    LEFT JOIN Incident AS Inc
    USING (incident_id)
    LEFT JOIN Location AS Lo
    USING (location_id)
    LEFT JOIN Code AS Cd
    USING (code, organization);

CREATE VIEW SearchView AS
SELECT
    Sr.search_id,
    Inc.incident_id,
    Inc.occurrence_date,
    Inc.type,
    Inc.status,
    Inc.police_department,
    Sr.legislation,
    Sr.object,
    Sr.outcome,
    Sr.object_caused_outcome,
    Sr.clothing_removal,
    Lo.location_id,
    Lo.latitude,
    Lo.longitude,
    Lo.premises,
    Lo.area,
    Lo.precinct,
    Lo.ward,
    Lo.borough,
    Lo.city,
    Lo.state,
    Lo.country,
    Sr.suspect_id,
    Ps.first_name AS suspect_first_name,
    Ps.last_name AS suspect_last_name,
    Ps.age_range AS suspect_age_range,
    Ps.gender AS suspect_gender,
    Ps.ethnicity AS suspect_ethnicity,
    Ps.phone_number AS suspect_phone_number
FROM
    Search AS Sr
    LEFT JOIN Incident AS Inc
    USING (incident_id)
    LEFT JOIN Location AS Lo
    USING (location_id)
    LEFT JOIN Person AS Ps
    ON Sr.suspect_id = Ps.person_id;
