-- Table Creation Script for Entity Models
CREATE TABLE entity_type (
	id serial PRIMARY KEY,
	slug VARCHAR(30) NOT NULL UNIQUE, 
	name TEXT,
	default_sort_direction BOOLEAN
);

CREATE TABLE entity_field (
	id serial PRIMARY KEY,
	entity_type_id INTEGER,
	FOREIGN KEY (entity_type_id) REFERENCES entity_type(id),
	entity_field_data_type_id INTEGER,
	FOREIGN KEY (entity_field_data_type_id) REFERENCES entity_field_data_type(id),
	on_table BOOLEAN,
	editable BOOLEAN,
	-- edit_permissions
	sortable BOOLEAN,
	searchable BOOLEAN,
	filterable BOOLEAN,
	entity_field_style_id INTEGER,
	entity_allowed_values_table INTEGER,
	entity_allowed_values_column INTEGER,
	FOREIGN KEY (entity_field_style_id) REFERENCES entity_field_style(id),
	FOREIGN KEY (entity_allowed_values_table_id) REFERENCES entity_allowed_values_table(id),
	FOREIGN KEY (entity_allowed_values_column_id) REFERENCES entity_allowed_values_column(id),
	is_default_sort_field BOOLEAN
);

CREATE TABLE entity_allowed_values_table (
	id serial PRIMARY KEY,
	name TEXT
);

CREATE TABLE entity_allowed_values_column (
	id serial PRIMARY KEY,
	entity_allowed_values_table_id INTEGER,
	FOREIGN KEY (entity_allowed_values_table_id) REFERENCES entity_allowed_values_table(id),
	name TEXT,
	entity_field_data_type_id INTEGER,
	FOREIGN KEY (entity_field_data_type_id) REFERENCES entity_field_data_type(id)
);

CREATE TABLE entity_field_input_type (
	id serial PRIMARY KEY,
	name TEXT
);

CREATE TABLE entity_field_data_type (
	id serial PRIMARY KEY,
	entity_field_input_type_id INTEGER,
	FOREIGN KEY (entity_field_input_type_id) REFERENCES entity_field_input_type(id),
	name TEXT
);

CREATE TABLE entity_field_style (
	table_weight INTEGER,
	weight_form INTEGER
);