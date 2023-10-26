create table "ADMIN"
(
    "userUuid" uuid    not null
        primary key
        references "USERS"
            on delete cascade,
    password   varchar not null
);

alter table "ADMIN"
    owner to "user";

