from dmigrations.mysql import migrations as m
import datetime
migration = m.Migration(sql_up=["""
    CREATE TABLE `data_docstatus` (
        `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
        `project_id` integer NOT NULL,
        `type` varchar(2) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    ;
""", """
    ALTER TABLE `data_docstatus` ADD CONSTRAINT project_id_refs_id_42feaee FOREIGN KEY (`project_id`) REFERENCES `data_project` (`id`);
"""], sql_down=["""
    DROP TABLE `data_docstatus`;
"""])
