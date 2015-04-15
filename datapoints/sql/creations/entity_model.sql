-- Table Creation Script for Entity Models
-- psql -U djangoapp -d polio -a -f entity_model.sql

CREATE TABLE entity_allowed_values_table (
	id serial PRIMARY KEY,
	name TEXT
);

CREATE TABLE entity_field_input_type (
	id serial PRIMARY KEY,
	name TEXT
);

CREATE TABLE entity_field_style (
	table_weight INTEGER,
	weight_form INTEGER
);

CREATE TABLE entity_field_data_type (
	id serial PRIMARY KEY,
	entity_field_input_type_id INTEGER,
	FOREIGN KEY (entity_field_input_type_id) REFERENCES entity_field_input_type(id),
	name TEXT
);

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

CREATE TABLE entity_allowed_values_column (
	id serial PRIMARY KEY,
	entity_allowed_values_table_id INTEGER,
	FOREIGN KEY (entity_allowed_values_table_id) REFERENCES entity_allowed_values_table(id),
	name TEXT,
	entity_field_data_type_id INTEGER,
	FOREIGN KEY (entity_field_data_type_id) REFERENCES entity_field_data_type(id)
);
# django content type
# look at json spec foreign keys
/* put this in view
 calc_curs = AggDataPoint.objects\
            .raw("SELECT * FROM fn_calc_datapoint(%s)",[self.cache_job.id]) # fc_calc_datapoint proc

        calc_dp_ids = [x.id for x in calc_curs] # because of lazy querysets
*/

# create the models.py file with no syncdb
	# use all imports etc be able to import in shell
# generate one big migration maybe 3-4
# use django unit test testcases for the models

# go further with the view taking info from urls and returning it 
