create table "AUTHORS"
(
    "ResearcherUuid" uuid not null
        constraint "ResearcherProjectAssociations_ResearcherUuid_fkey"
            references "RESEARCHERS"
            on delete cascade,
    "ProjectUuid"    uuid not null
        constraint "ResearcherProjectAssociations_ProjectUuid_fkey"
            references "PROJECT"
            on delete cascade,
    constraint "ResearcherProjectAssociations_pkey"
        primary key ("ResearcherUuid", "ProjectUuid")
);

alter table "AUTHORS"
    owner to "user";

grant select on "AUTHORS" to evaluator;

grant delete, insert, references, select, trigger, truncate, update on "AUTHORS" to admin_role;

grant insert, select on "AUTHORS" to researcher;

grant delete, insert, references, select, trigger, truncate, update on "AUTHORS" to admin_user;
