create table "RESEARCHERS"
(
    "userUuid" uuid    not null
        primary key
        references "USERS"
            on delete cascade,
    cv         bytea,
    password   varchar not null
);

alter table "RESEARCHERS"
    owner to "user";

grant select on "RESEARCHERS" to evaluator;

grant insert, select, update on "RESEARCHERS" to researcher;
