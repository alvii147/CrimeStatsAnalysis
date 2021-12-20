CREATE INDEX Incident_PK_IDX
ON Incident (incident_id);

CREATE INDEX Incident_Location_FK_IDX
ON Incident (location_id);

CREATE INDEX Location_PK_IDX
ON Location (location_id);

CREATE INDEX Crime_PK_IDX
ON Crime (crime_id);

CREATE INDEX Crime_Incident_FK_IDX
ON Crime (incident_id);

CREATE INDEX Crime_Code_FK_IDX
ON Crime (
    code,
    organization
);

CREATE INDEX Crime_Person_FK_IDX
ON Crime (victim_id);

CREATE INDEX Complaint_PK_IDX
ON Complaint (complaint_id);

CREATE INDEX Complaint_Incident_FK_IDX
ON Complaint (incident_id);

CREATE INDEX Complaint_Code_FK_IDX
ON Complaint (
    code,
    organization
);

CREATE INDEX Search_PK_IDX
ON Search (search_id);

CREATE INDEX Search_Incident_FK_IDX
ON Search (incident_id);

CREATE INDEX Search_Person_FK_IDX
ON Search (suspect_id);

CREATE INDEX Person_PK_IDX
ON Person (person_id);

CREATE INDEX Code_PK_IDX
ON Code (
    code,
    organization
);
