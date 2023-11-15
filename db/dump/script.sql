-- Creazione schema

CREATE SCHEMA IF NOT EXISTS project_schema;
SET search_path TO project_schema;

-- Aggiunta estensioni
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Definizione dello schema del database

create table "USERS"
(
    uuid        uuid default uuid_generate_v4() not null
        primary key,
    name        varchar                                        not null,
    surname     varchar                                        not null,
    email       varchar                                        not null
        unique,
    dateofbirth date
);

create table "ADMIN"
(
    "userUuid" uuid    not null
        primary key
        references "USERS"
            on delete cascade,
    password   varchar not null
);

create table "RESEARCHERS"
(
    "userUuid" uuid    not null
        primary key
        references "USERS"
            on delete cascade,
    cv         bytea,
    password   varchar not null
);

create table "EVALUATOR"
(
    "userUuid" uuid    not null
        primary key
        references "USERS"
            on delete cascade,
    password   varchar not null,
    cv         bytea
);

create type evaluations_enum as enum ('approvato', 'sottomessoperval', 'modificare', 'nonapprovato');

create table "PROJECT"
(
    uuid        uuid default uuid_generate_v4() not null
        primary key,
    title       varchar                                        not null,
    description text,
    status      evaluations_enum                not null
);

create table "MESSAGES"
(
    uuid             uuid default uuid_generate_v4() not null
        primary key,
    object           varchar                                        not null,
    text             text,
    date             timestamp,
    "ResearcherUuid" uuid                                           not null
        references "RESEARCHERS",
    "ProjectUuid"    uuid                                           not null
        references "PROJECT"
);

create table "FILE"
(
    uuid          uuid default uuid_generate_v4() not null
        primary key,
    title         varchar                                        not null,
    "ProjectUuid" uuid                                           not null
        references "PROJECT"
);

create table "VERSIONS"
(
    uuid             uuid default uuid_generate_v4() not null
        primary key,
    "FileUuid"       uuid
        references "FILE"
            on delete cascade,
    details          text,
    "submitdate" timestamp,
    file             bytea,
    version          integer
);

create table "REPORT"
(
    uuid            uuid default uuid_generate_v4() not null
        primary key,
    "EvaluatorUuid" uuid
        references "EVALUATOR"
            on delete cascade,
    "VersionsUuid"  uuid
        references "VERSIONS"
            on delete cascade,
    description     text
);

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


-- Definizione dei ruoli: admin_role, ev_role, res_role
SET search_path TO project_schema;
create role ev_role;
create role admin_role
    superuser;
create role res_role;


-- Definizione di user:
create user admin_user with password 'pwd';
create user ev_user with password 'pwd';
create user res_user with password 'pwd';

grant admin_role to admin_user;
grant ev_role to ev_user;
grant res_role to res_user;


-- Definizione delle grant sulle tabelle:
---admin_role:
grant all on all tables in schema project_schema to admin_role;
grant usage on schema project_schema to admin_role;

---ev_role:
grant insert, select on "VERSIONS", "MESSAGES" to ev_role;
grant select on "AUTHORS", "FILE", "RESEARCHERS" to ev_role;
grant insert, select, update on "USERS", "PROJECT", "EVALUATOR", "REPORT" to ev_role;
grant usage on schema project_schema to ev_role;

---res_role:
grant select on "REPORT", "EVALUATOR" to res_role;
grant insert, select on "MESSAGES", "AUTHORS", "FILE" to res_role;
grant insert, select, update on "RESEARCHERS", "PROJECT", "USERS", "VERSIONS" to res_role;
grant usage on schema project_schema to res_role;