drop table if exists Expanse;
drop table if exists Currency;
drop table if exists Project;
drop table if exists User;


create table Currency(
    curr_id integer primary key autoincrement,
    curr_name text unique not null,
    ex_rate float not null
);

create table Project(
    pj_id integer primary key autoincrement,
    owner_id integer not null,
    name text not null,
    location text,
    start_date date default CURRENT_DATE,
    end_date, 
    unique (owner_id, name),
    foreign key(owner_id) references User(user_id)
);

create table Expanse(
    exp_id integer primary key autoincrement,
    pj_id integer not null, 
    cat text not null default 'Misc',
    curr integer not null default 1,
    value float not null,
    label text not null,
    timestamp datetime not null default CURRENT_TIMESTAMP,
    foreign key(pj_id) references Project(pj_id),
    foreign key(curr) references Currency(curr_id)
);

create table User(
    user_id integer primary key autoincrement,
    username text unique not null,
    password text not null,
    admin boolean not null default 0
);