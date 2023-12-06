-- Creazione schema

CREATE SCHEMA IF NOT EXISTS project_schema;
SET search_path TO project_schema;

-- Aggiunta estensioni
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Definizione dello schema del database

CREATE TABLE "users"
(
    "uuid"        UUID DEFAULT uuid_generate_v4(),
    "name"        VARCHAR NOT NULL,
    "surname"     VARCHAR NOT NULL,
    "email"       VARCHAR NOT NULL UNIQUE,
    "birthdate"   DATE NOT NULL,
    PRIMARY KEY ("uuid")

);

CREATE TABLE "admin"
(
    "userUuid"   UUID,
    "password"   VARCHAR NOT NULL,
    PRIMARY KEY ("userUuid"),
    FOREIGN KEY ("userUuid") REFERENCES "users" ("uuid") ON DELETE CASCADE
);

CREATE TABLE "researchers"
(
    "userUuid"   UUID,
    "password"   VARCHAR NOT NULL,
    "cv"         BYTEA,
    PRIMARY KEY ("userUuid"),
    FOREIGN KEY ("userUuid") REFERENCES "users" ("uuid") ON DELETE CASCADE
);

CREATE TABLE "evaluators"
(
    "userUuid"   UUID,
    "password"   VARCHAR NOT NULL,
    "cv"         BYTEA,
    PRIMARY KEY ("userUuid"),
    FOREIGN KEY ("userUuid") REFERENCES "users" ("uuid") ON DELETE CASCADE
);

CREATE TYPE evaluations_enum AS ENUM ('approvato', 'sottomessoperval', 'modificare', 'nonapprovato');

CREATE TABLE "projects"
(
    "uuid"        UUID DEFAULT uuid_generate_v4(),
    "title"       VARCHAR NOT NULL,
    "description" TEXT,
    "status"      evaluations_enum DEFAULT 'modificare',
    PRIMARY KEY ("uuid")
);

CREATE TABLE "messages"
(
    "uuid"             UUID DEFAULT uuid_generate_v4(),
    "object"           VARCHAR NOT NULL,
    "text"             TEXT,
    "date"             TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "ResearcherUuid"   UUID,
    "ProjectUuid"      UUID,
    PRIMARY KEY ("uuid", "ResearcherUuid", "ProjectUuid"),
    FOREIGN KEY ("ResearcherUuid") REFERENCES "researchers" ("userUuid") ON DELETE CASCADE,
    FOREIGN KEY ("ProjectUuid") REFERENCES "projects" ("uuid") ON DELETE CASCADE
);

CREATE TABLE "files"
(
    "uuid"          UUID DEFAULT uuid_generate_v4(),
    "title"         VARCHAR NOT NULL,
    "ProjectUuid"   UUID NOT NULL,
    PRIMARY KEY ("uuid"),
    FOREIGN KEY ("ProjectUuid") REFERENCES "projects" ("uuid") ON DELETE CASCADE
);

CREATE TABLE "versions"
(
    "uuid"             UUID DEFAULT uuid_generate_v4(),
    "FileUuid"         UUID NOT NULL,
    "details"          TEXT,
    "submitted"        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "file"             BYTEA,
    "version"          INTEGER,
    PRIMARY KEY ("uuid"),
    FOREIGN KEY ("FileUuid") REFERENCES "files" ("uuid") ON DELETE CASCADE
);

CREATE TABLE "reports"
(
    "uuid"            UUID DEFAULT uuid_generate_v4(),
    "EvaluatorUuid"   UUID NOT NULL,
    "VersionsUuid"    UUID NOT NULL,
    "description"     TEXT,
    "submitted"        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY ("uuid", "EvaluatorUuid", "VersionsUuid"),
    FOREIGN KEY ("EvaluatorUuid") REFERENCES "evaluators" ("userUuid") ON DELETE CASCADE,
    FOREIGN KEY ("VersionsUuid") REFERENCES "versions" ("uuid") ON DELETE CASCADE
);

-- Tabella di associazione tra ricercatori e progetti --
CREATE TABLE "authors"
(
    "ResearcherUuid" UUID,
    "ProjectUuid"    UUID,
    PRIMARY KEY ("ResearcherUuid", "ProjectUuid"),
    FOREIGN KEY ("ResearcherUuid") REFERENCES "researchers" ("userUuid") ON DELETE CASCADE,
    FOREIGN KEY ("ProjectUuid") REFERENCES "projects" ("uuid") ON DELETE CASCADE
);


-- Definizione dei ruoli: admin_role, ev_role, res_role
SET search_path TO project_schema;
CREATE ROLE ev_role;
CREATE ROLE admin_role SUPERUSER;
CREATE ROLE res_role;


-- Definizione di user:
CREATE USER admin_user WITH PASSWORD 'pwd';
CREATE USER ev_user WITH PASSWORD 'pwd';
CREATE USER res_user WITH PASSWORD 'pwd';

GRANT admin_role TO admin_user;
GRANT ev_role TO ev_user;
GRANT res_role TO res_user;


-- Definizione delle GRANT sulle tabelle:
---admin_role:
GRANT ALL ON ALL TABLES IN SCHEMA project_schema TO admin_role;
GRANT USAGE ON SCHEMA project_schema TO admin_role;

---ev_role:
GRANT INSERT, SELECT  ON "versions", "messages" TO ev_role;
GRANT SELECT  ON "authors", "files", "researchers" TO ev_role;
GRANT INSERT, SELECT , UPDATE ON "users", "projects", "evaluators", "reports" TO ev_role;
GRANT USAGE ON SCHEMA project_schema TO ev_role;

---res_role:
GRANT SELECT  ON "reports", "evaluators" TO res_role;
GRANT INSERT, SELECT  ON "messages", "authors", "files" TO res_role;
GRANT INSERT, SELECT , UPDATE ON "researchers", "projects", "users", "versions" TO res_role;
GRANT USAGE ON SCHEMA project_schema TO res_role;