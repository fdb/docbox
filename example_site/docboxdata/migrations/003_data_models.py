from dmigrations.mysql import migrations as m
import datetime
migration = m.Migration(sql_up=["""
    CREATE TABLE `data_versionurl` (
        `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
        `url` varchar(200) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    ;
"""], sql_down=["""
    DROP TABLE `data_versionurl`;
"""])
