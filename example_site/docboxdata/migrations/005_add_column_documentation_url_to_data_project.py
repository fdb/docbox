from dmigrations.mysql import migrations as m
import datetime
migration = m.AddColumn('data', 'project', 'documentation_url', 'integer NULL', 'data_versionurl')
