CREATE TABLE insurance_data (
    ID INT Primary Key,
    County VARCHAR(100),
    Health_Plan_Name VARCHAR(255),
    Category_of_Aid VARCHAR(255),
    Lower_Bound VARCHAR(20),
    Midpoint VARCHAR(20),
    Upper_Bound VARCHAR(20)
);

CREATE TABLE taxonomy_data (
    PROVIDER_TAXONOMY_CODE TEXT Primary Key,
    MEDICARE_PROVIDER_SUPPLIER_TYPE_DESCRIPTION VARCHAR(255),
    PROVIDER_TAXONOMY_DESCRIPTION VARCHAR(255),
    MEDICARE_SPECIALTY_CODE VARCHAR(255),
    CONSTRAINT Taxonomy_code_check
        CHECK (PROVIDER_TAXONOMY_CODE ~ '^[A-Za-z0-9]+$')
);

CREATE TABLE Hospitals (
    OSHPD_ID INT PRIMARY KEY,
    FacilityName VARCHAR(255) NOT NULL,
    FacilityType VARCHAR(255),
    Address VARCHAR(255),
    Address2 VARCHAR(255),
    City VARCHAR(255),
    State VARCHAR(2),
    ZIP INT,
    County VARCHAR(255),
    Facility_level_desc VARCHAR(255),
    Total_number_beds INT,
    Er_service_level_desc VARCHAR(255),
    Facility_status_desc VARCHAR(255) CHECK (License_type_desc IN ('Open', 'Suspense')),
    License_type_desc VARCHAR(255) CHECK (License_type_desc IN ('Clinic', 'Home health', 'Hospital', 'Long term care facility')),
    License_category_desc VARCHAR(255)
);

CREATE TABLE hospital_ratings (
    id SERIAL PRIMARY KEY,
    OSHPD_ID INT REFERENCES hospitals(OSHPD_ID),
    Performance_measure VARCHAR(255) NOT NULL,
    No_of_adverse_events INT,
    No_of_cases INT,
    Risk_adjusted_rate FLOAT,
    Hospital_ratings VARCHAR(255)
);

CREATE TABLE ProviderNetwork (
    ProviderID SERIAL PRIMARY KEY,
    FirstName TEXT NOT NULL,
    LastName TEXT NOT NULL,
    ManagedCarePlan TEXT NOT NULL,
    SubNetwork TEXT,
    NPI INTEGER NOT NULL,
    Taxonomy VARCHAR CHECK (Taxonomy ~ '^[a-zA-Z0-9]+$'),
    MCNAProviderGroup TEXT,
    MCNAProviderType TEXT,
    LicensureType VARCHAR(4),
    PrimaryCare CHAR(1) CHECK (PrimaryCare IN ('Y', 'N')),
    Specialist CHAR(1) CHECK (Specialist IN ('Y', 'N')),
    SeesChildren TEXT CHECK (SeesChildren IN ('Both', 'Only', 'No')),
    Telehealth TEXT CHECK (Telehealth IN ('Both', 'Only', 'No')),
    BHIndicator TEXT,
    OSHPD_ID INTEGER
);