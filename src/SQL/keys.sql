ALTER TABLE Complaint ADD CONSTRAINT Complaint_Incident
    FOREIGN KEY (incident_id) REFERENCES Incident(incident_id);

ALTER TABLE Crime ADD CONSTRAINT Crime_Incident
    FOREIGN KEY (incident_id) REFERENCES Incident(incident_id);

ALTER TABLE Search ADD CONSTRAINT Search_Incident
    FOREIGN KEY (incident_id) REFERENCES Incident(incident_id);

ALTER TABLE Incident ADD CONSTRAINT happensIn
    FOREIGN KEY (location_id) REFERENCES Location(location_id);

ALTER TABLE Complaint ADD CONSTRAINT complaintOfCode
    FOREIGN KEY (code, organization) REFERENCES Code(code, organization);

ALTER TABLE Crime ADD CONSTRAINT crimeOfCode
    FOREIGN KEY (code, organization) REFERENCES Code(code, organization);

ALTER TABLE Crime ADD CONSTRAINT victimOf
    FOREIGN KEY (victim_id) REFERENCES Person(person_id);

ALTER TABLE Search ADD CONSTRAINT suspectOf
    FOREIGN KEY (suspect_id) REFERENCES Person(person_id);
