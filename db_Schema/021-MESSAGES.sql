create table "MESSAGES"
(
    uuid             uuid default project_schema.uuid_generate_v4() not null
        primary key,
    object           varchar                                        not null,
    text             text,
    date             date,
    "ResearcherUuid" uuid                                           not null
        references "RESEARCHERS",
    "ProjectUuid"    uuid                                           not null
        references "PROJECT"
);

alter table "MESSAGES"
    owner to "user";

grant insert, select on "MESSAGES" to evaluator;

grant delete, insert, references, select, trigger, truncate, update on "MESSAGES" to admin_role;

grant insert, select on "MESSAGES" to researcher;

grant delete, insert, references, select, trigger, truncate, update on "MESSAGES" to admin_user;

