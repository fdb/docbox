from dmigrations.mysql import migrations as m
import datetime
migration = m.AddColumn('data', 'project', 'source_url', 'integer NULL', 'data_sourceurl')
