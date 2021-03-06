#!/bin/bash
SQL_DIR=$(pwd)'/datapoints/sql/'

## VIEWS ##
# psql polio -f $SQL_DIR'views/vw_missing_mappings.sql'

## FUNCTIONS ##

psql polio -f $SQL_DIR'functions/fn_agg_datapoint.sql'
psql polio -f $SQL_DIR'functions/fn_test_data_accuracy.sql'
psql polio -f $SQL_DIR'functions/fn_find_bad_data.sql'

psql polio -f $SQL_DIR'functions/fn_calc_prep.sql'
psql polio -f $SQL_DIR'functions/fn_calc_sum_of_parts.sql'
psql polio -f $SQL_DIR'functions/fn_calc_part_over_whole.sql'
psql polio -f $SQL_DIR'functions/fn_calc_part_of_difference.sql'
psql polio -f $SQL_DIR'functions/fn_calc_upsert_computed.sql'
psql polio -f $SQL_DIR'functions/fn_calc_datapoint.sql'
psql polio -f $SQL_DIR'functions/fn_get_authorized_regions_by_user.sql'

SRC_SQL_DIR=$(pwd)'/source_data/sql/'

psql polio -f $SRC_SQL_DIR'functions/fn_populate_doc_meta.sql'
psql polio -f $SRC_SQL_DIR'functions/fn_get_source_dps_to_sync.sql'
psql polio -f $SRC_SQL_DIR'functions/fn_sync_odk_regions.sql'
