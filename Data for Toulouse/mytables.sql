CREATE TABLE network_combined (
	from_stop_I		integer,
	to_stop_I		integer,
	d			integer,
	duration_avg		float,
	n_vehicles		integer,
	route_I_counts		integer,
	route_type		integer
	);

CREATE TABLE network_nodes (
    stop_I INTEGER PRIMARY KEY,
    lat integer,
    lon integer,
    name TEXT
);


CREATE TABLE network_subway (
    from_stop_I INTEGER,
    to_stop_I INTEGER,
    d INTEGER,
    duration_avg FLOAT,
    n_vehicles INTEGER,
    route_I_counts TEXT
);

CREATE TABLE network_temporal_day (
    from_stop_I INTEGER,
    to_stop_I INTEGER,
    dep_time_ut BIGINT,
    arr_time_ut BIGINT,
    route_type INTEGER,
    trip_I INTEGER,
    seq INTEGER,
    route_I INTEGER
);

CREATE TABLE network_temporal_week (
    from_stop_I INTEGER,
    to_stop_I INTEGER,
    dep_time_ut BIGINT,
    arr_time_ut BIGINT,
    route_type INTEGER,
    trip_I INTEGER,
    seq INTEGER,
    route_I INTEGER
);

CREATE TABLE network_tram (
    from_stop_I INTEGER,
    to_stop_I INTEGER,
    d INTEGER,
    duration_avg FLOAT,
    n_vehicles INTEGER,
    route_I_counts TEXT
);

CREATE TABLE network_bus(
    from_stop_I INTEGER,
    to_stop_I INTEGER,
    d INTEGER,
    duration_avg FLOAT,
    n_vehicles INTEGER,
    route_I_counts TEXT
);

CREATE TABLE network_walk (
    from_stop_I INTEGER,
    to_stop_I INTEGER,
    d INTEGER,
    d_walk INTEGER
);

