drop table if exists Expanse;
drop table if exists Category;
drop table if exists Project;
drop table if exists User;

create table Expanse(
    exp_id integer primary key autoincrement,
    exp_type text not null default 'Misc',
    label text not null,
    curr_id integer not null default 1 foreign key references Currency(curr_id),
    value float not null
);

create table Currency(
    curr_id integer primary key autoincrement,
    ex_rate float not null
);

create table Project(
    pj_id integer primary key autoincrement,
    owner_id integer not null foreign key references User(user_id),
    location text,
    start_date date default getdate(),
    start_date date default getdate()
);

create table Expanse(
    exp_id integer primary key autoincrement,
    pj_id integer not null foreign key references Project(pj_id),
    exp_type text not null default 'Misc',
    curr integer foreign key references Currency(curr_id),
    value float not null,
    label text not null
);

create table User(
    user_id integer primary key autoincrement,
    username text unique not null,
    password text not null
);
