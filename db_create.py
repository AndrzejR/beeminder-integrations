"""This is a one-off script to create the sqlite3 db."""

import sqlite3

DATABASE_FILE = 'bm_in.db'
CONNECTION = sqlite3.connect(DATABASE_FILE)

CURSOR = CONNECTION.cursor()

CURSOR.execute('''create table if not exists bm_datapoint
               (id text primary key
               , value real
               , timestamp integer
               , updated_at integer
               , daystamp text
               , comment text
               , requestid text
               , bm_url text)
               ''')

CURSOR.execute('''create table if not exists parameter
               (param_name text primary key
               , param_value text)
               ''')

CURSOR.execute('''create table if not exists bm_goal_xref
               (bm_url text primary key
               , bm_name text               
               , habitica_id text
               , habitica_name text
               , is_active int);
               ''')

CURSOR.execute('''create table if not exists dcm_toggl_datapoint
               (toggl_date text primary key
               , toggl_ms integer
               , status integer
               , bm_id text);
               ''')

CONNECTION.commit()
