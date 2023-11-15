create table "FILE"
(
    uuid          uuid default project_schema.uuid_generate_v4() not null
        primary key,
    title         varchar                                        not null,
    "ProjectUuid" uuid                                           not null
        references "PROJECT"
);

alter table "FILE"
    owner to "user";

grant select on "FILE" to evaluator;

grant delete, insert, references, select, trigger, truncate, update on "FILE" to admin_role;

grant insert, select on "FILE" to researcher;

grant delete, insert, references, select, trigger, truncate, update on "FILE" to admin_user;

