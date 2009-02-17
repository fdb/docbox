from dmigrations.mysql import migrations as m
import datetime
migration = m.AddColumn('data', 'project', 'vcs', 'varchar(3) NOT NULL')
