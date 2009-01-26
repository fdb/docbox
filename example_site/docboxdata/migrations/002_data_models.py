from dmigrations.mysql import migrations as m
import datetime
migration = m.Migration(sql_up=["""
    CREATE TABLE `data_project` (
        `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
        `name` varchar(120) NOT NULL,
        `identifier` varchar(30) NOT NULL,
        `description` longtext NOT NULL,
        `username` varchar(30) NOT NULL,
        `password` varchar(30) NOT NULL,
        `homepage` varchar(200) NOT NULL,
        `doc_url` varchar(200) NOT NULL,
        `src_url` varchar(200) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    ;
"""], sql_down=["""
    DROP TABLE `data_project`;
"""])
