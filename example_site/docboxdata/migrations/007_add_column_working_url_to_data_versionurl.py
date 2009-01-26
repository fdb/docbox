from dmigrations.mysql import migrations as m
import datetime
migration = m.AddColumn('data', 'versionurl', 'working_url', 'varchar(200) NOT NULL')
