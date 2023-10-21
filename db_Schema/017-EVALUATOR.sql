create table "EVALUATOR"
(
    "userUuid" uuid    not null
        primary key
        references "USERS"
            on delete cascade,
    password   varchar not null,
    cv         bytea
);

alter table "EVALUATOR"
    owner to "user";

grant insert, select, update on "EVALUATOR" to evaluator;

grant select on "EVALUATOR" to researcher;

