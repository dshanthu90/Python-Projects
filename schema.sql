DROP TABLE if exists honey_comb;
DROP TABLE if exists user_table;
DROP TABLE if exists task_list;

CREATE TABLE honey_comb(
    honey_comb_id INTEGER PRIMARY KEY,
    honey_comb_name TEXT  NOT NULL
);

CREATE TABLE user_table(
    user_id INTEGER PRIMARY KEY,
    user_name TEXT NOT NULL,
    comb_id INTEGER NOT NULL,
    FOREIGN KEY (comb_id) REFERENCES honey_comb (honey_comb_id)
);

CREATE TABLE task_list(
    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_detail TEXT NOT NULL,
    task_due DATE DEFAULT CURRENT_DATE,
    task_created_by INTEGER NOT NULL,
    task_assigned INTEGER ,
    task_comb_id INTEGER NOT NULL,
    task_status INTEGER CHECK (task_status =0 or task_status=1)
);

INSERT INTO honey_comb VALUES ( 1, 'SenShan');
INSERT INTO user_table VALUES( 1, 'Senthil',1);
INSERT INTO user_table VALUES (2,'Shanthini',1);
