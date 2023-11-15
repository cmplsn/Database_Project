create table "USERS"
(
    uuid        uuid default project_schema.uuid_generate_v4() not null
        primary key,
    name        varchar                                        not null,
    surname     varchar                                        not null,
    email       varchar                                        not null
        unique,
    dateofbirth date
);

alter table "USERS"
    owner to "user";

grant insert, select, update on "USERS" to evaluator;

grant delete, insert, references, select, trigger, truncate, update on "USERS" to admin_role;

grant insert, select, update on "USERS" to researcher;

grant delete, insert, references, select, trigger, truncate, update on "USERS" to admin_user;

