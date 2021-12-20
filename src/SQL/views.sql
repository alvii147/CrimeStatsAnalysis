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
    Cr.weapon,
    Cr.domestic,
    Cr.description,
    Inc.status,
    Inc.police_department,
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
    INNER JOIN Incident AS Inc
    USING (incident_id)
    INNER JOIN Location AS Lo
    USING (location_id)
    LEFT JOIN Code AS Cd
    USING (code, organization)
    LEFT JOIN Person AS Ps
    ON Cr.victim_id = Ps.person_id;