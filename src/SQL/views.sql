CREATE VIEW CrimesData AS
SELECT
    crime_id,
    code,
    organization,
    occurrence_date,
    latitude,
    longitude,
    country,
    age_range,
    gender,
    ethnicity
FROM
    Crime INNER JOIN
    Incident USING (incident_id) INNER JOIN
    Location USING (location_id) LEFT JOIN
    Code USING (code, organization) LEFT JOIN
    Person ON victim_id = person_id;