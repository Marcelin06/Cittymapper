CREATE TABLE network_combined_p (
	from_stop_I		integer,
	to_stop_I		integer,
	d			integer,
	duration_avg		float,
	n_vehicles		integer,
	route_I_counts		integer,
	route_type		integer
	);

CREATE TABLE network_nodes_p (
    stop_I INTEGER PRIMARY KEY,
    lat float,
    lon float,
    name TEXT
);


CREATE TABLE network_subway_p (
    from_stop_I INTEGER,
    to_stop_I INTEGER,
    d INTEGER,
    duration_avg FLOAT,
    n_vehicles INTEGER,
    route_I_counts TEXT
);

CREATE TABLE network_rail_p (
    from_stop_I INTEGER,
    to_stop_I INTEGER,
    d INTEGER,
    duration_avg FLOAT,
    n_vehicles INTEGER,
    route_I_counts TEXT
);

CREATE TABLE network_temporal_day_p (
    from_stop_I INTEGER,
    to_stop_I INTEGER,
    dep_time_ut BIGINT,
    arr_time_ut BIGINT,
    route_type INTEGER,
    trip_I INTEGER,
    seq INTEGER,
    route_I INTEGER
);

CREATE TABLE network_temporal_week_p (
    from_stop_I INTEGER,
    to_stop_I INTEGER,
    dep_time_ut BIGINT,
    arr_time_ut BIGINT,
    route_type INTEGER,
    trip_I INTEGER,
    seq INTEGER,
    route_I INTEGER
);

CREATE TABLE network_tram_p (
    from_stop_I INTEGER,
    to_stop_I INTEGER,
    d INTEGER,
    duration_avg FLOAT,
    n_vehicles INTEGER,
    route_I_counts TEXT
);

CREATE TABLE network_bus_p(
    from_stop_I INTEGER,
    to_stop_I INTEGER,
    d INTEGER,
    duration_avg FLOAT,
    n_vehicles INTEGER,
    route_I_counts TEXT
);

CREATE TABLE network_walk_p (
    from_stop_I INTEGER,
    to_stop_I INTEGER,
    d INTEGER,
    d_walk INTEGER
);
CREATE TABLE routes_paris (
    route_I INTEGER,
    route_name VARCHAR(50),
    route_type INTEGER
);
