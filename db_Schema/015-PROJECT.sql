create table "PROJECT"
(
    uuid        uuid default project_schema.uuid_generate_v4() not null
        primary key,
    title       varchar                                        not null,
    description text,
    status      project_schema.evaluations_enum                not null
);

alter table "PROJECT"
    owner to "user";

grant insert, select, update on "PROJECT" to evaluator;

grant delete, insert, references, select, trigger, truncate, update on "PROJECT" to admin_role;

grant insert, select, update on "PROJECT" to researcher;

grant delete, insert, references, select, trigger, truncate, update on "PROJECT" to admin_user;

