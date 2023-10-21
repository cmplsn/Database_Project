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

grant insert, select, update on "PROJECT" to researcher;
