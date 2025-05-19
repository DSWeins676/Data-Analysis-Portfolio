CREATE TABLE ncsa_makes (
    make_code INT NOT NULL,
    make VARCHAR(255) NOT NULL,
    PRIMARY KEY (make_code)
);

CREATE TABLE restraints(
    restraint_code INT NOT NULL,
    restraint_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (restraint_code)
);

CREATE TABLE states (
    state_code INT NOT NULL,
    state_name VARCHAR(255) NOT NULL,
    rural_vmt INT NOT NULL,
    urban_vmt INT NOT NULL,
    PRIMARY KEY (state_code)
);

CREATE TABLE counties (
    state_code INT NOT NULL,
    county_code INT NOT NULL,
    county_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (state_code, county_code)
);

CREATE TABLE crashes (
    st_case INT NOT NULL,
    state_code INT NOT NULL,
    county_code INT NOT NULL,
    crash_date DATE NULL,
    crash_time TIME NULL,
    rural_urban VARCHAR(255),
    latitude DECIMAL(12,9),
    longitude DECIMAL(12,9),
    light_cond VARCHAR(255),
    weather VARCHAR(255),
    PRIMARY KEY (st_case),
    FOREIGN KEY (state_code) REFERENCES states(state_code)
);

CREATE TABLE vehicles (
	vehicle_id INT NOT NULL,
    st_case INT NOT NULL,
    veh_no INT NOT NULL,
    hit_run VARCHAR(255),
    reg_stat INT NULL,
    veh_owner TEXT,
    vin VARCHAR(255),
    mod_year INT NULL,
    make_code INT NULL,
    body_typ TEXT,
    trav_sp INT NULL,
    PRIMARY KEY (vehicle_id),
	FOREIGN KEY (st_case) REFERENCES crashes(st_case)
);

CREATE TABLE people (
	person_id INT NOT NULL,
    st_case INT NOT NULL,
    veh_no INT NOT NULL,
    per_no INT NOT NULL,
    age INT NULL,
    sex VARCHAR(255),
    per_typ VARCHAR(255),
    inj_sev VARCHAR(255),
    seat_pos VARCHAR(255),
    restraint_code INT NULL,
    rest_mis VARCHAR(255),
    drinking VARCHAR(255),
    alc_res DECIMAL(5,3) NULL,
    PRIMARY KEY (person_id),
    FOREIGN KEY (st_case) REFERENCES crashes(st_case)
    );
