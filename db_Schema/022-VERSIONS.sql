create table "VERSIONS"
(
    uuid             uuid default project_schema.uuid_generate_v4() not null
        primary key,
    "FileUuid"       uuid
        references "FILE"
            on delete cascade,
    details          text,
    "submitiongData" date,
    file             bytea,
    version          integer
);

alter table "VERSIONS"
    owner to "user";

grant insert, select on "VERSIONS" to evaluator;

grant delete, insert, references, select, trigger, truncate, update on "VERSIONS" to admin_role;

grant insert, select, update on "VERSIONS" to researcher;

grant delete, insert, references, select, trigger, truncate, update on "VERSIONS" to admin_user;

