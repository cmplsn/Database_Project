create table "REPORT"
(
    uuid            uuid default project_schema.uuid_generate_v4() not null
        primary key,
    "EvaluatorUuid" uuid
        references "EVALUATOR"
            on delete cascade,
    "VersionsUuid"  uuid
        references "VERSIONS"
            on delete cascade,
    description     text
);

alter table "REPORT"
    owner to "user";

grant insert, select, update on "REPORT" to evaluator;

grant select on "REPORT" to researcher;

