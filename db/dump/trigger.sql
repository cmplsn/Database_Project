-- Definizione dei trigger
SET search_path TO project_schema;

-- Creazione di Admin e degli utenti fantasma alla creazione del database
-- Creazione della funzione che sarà chiamata dal trigger


-- FUNCTION E TRIGGER PER IMPEDIRE UPDATE SU PROGETTI CON 
-- status == approvato o status == nonapprovato
create function status_function() returns trigger as $$
    begin
        if('approvato'=(SELECT status from projects where uuid=new.uuid)
               OR 'nonapprovato'=(SELECT status from projects where uuid=new.uuid))
        then return null;
        end if;
        return new;
    end;
$$ language plpgsql;

CREATE TRIGGER checkstatus before UPDATE on projects
    for each row
    execute function status_function();


-- FUNCTION E TRIGGER PER IMPEDIRE INSERT E UPDATE DI FILE CON
-- project.status==approvato OR project.status==nonapprovato
create or replace function file_ins_upd() returns trigger
language plpgsql
as
$$
    begin
        if('approvato' = (Select status from projects where uuid = new."ProjectUuid")
            OR 'nonapprovato'=(Select status from projects where uuid=new."ProjectUuid"))
        then return null;
        end if;
        return new;
    end;
$$;

create trigger file_ins_upd BEFORE INSERT OR UPDATE on files
    for each row
    execute function file_ins_upd();




-- FUNCTION E TRIGGER PER IMPEDIRE DELETE DI FILE CON 
-- project.status==approvato OR project.status==nonapprovato

create or replace function file_del() returns trigger
language plpgsql
as
$$
    begin
        if ('approvato' = (Select status from projects where uuid = old."ProjectUuid")
            OR 'nonapprovato'=(Select status from projects where uuid=old."ProjectUuid"))
        then return null;
        end if;
        return old;
    end;
$$;

create trigger file_del BEFORE DELETE on files
    for each row
    execute function file_del();

-- IMPEDIRE INSERT E UPDATE DI VERSIONS DI FILE CHE APPARTENGONO A PROGETTI CON 
-- status='approvato' o status='non approvato'

create or replace function vers_ins_upd() returns trigger language plpgsql
as
    $$
    begin
        if('approvato'=(select p.status from projects p join files f on p.uuid=f."ProjectUuid" where f.uuid=new."FileUuid")
            OR
           'nonapprovato'=(select p.status from projects p join files f on p.uuid=f."ProjectUuid" where f.uuid=new."FileUuid"))
            then return null;
            end if;
        return new;
    end;
    $$;

create trigger vers_ins_upd before insert or update on versions
    for each row
    execute function vers_ins_upd();


-- IMPEDIRE DELETE DI VERSIONS appartenenti a progetti già approvati o non approvati.

create or replace function vers_del() returns trigger
language plpgsql
as
    $$
    begin
        if('approvato'=(select status from projects p join files f on p.uuid=f."ProjectUuid" where f.uuid=old."FileUuid")
            OR
           'nonapprovato'=(select status from projects p join files f on p.uuid=f."ProjectUuid" where f.uuid=old."FileUuid"))
            then return null;
            end if;
        return old;
    end;
    $$;

create trigger vers_del before delete on versions
    for each row
    execute function vers_del();


--IMPEDIRE INSERT UPDATE DI REPORT SU progetti gia approvati/nonapprovati

create or replace function report_ins_upd() returns trigger
language plpgsql
as
    $$
    begin
        if('approvato'=(select status from projects p join files f on p.uuid=f."ProjectUuid" join versions v
            on f.uuid =v."FileUuid" where v.uuid=new."VersionsUuid")
            OR
           'nonapprovato'=(select status from projects p join files f on p.uuid=f."ProjectUuid" join versions v
            on f.uuid =v."FileUuid" where v.uuid=new."VersionsUuid"))
            then return null;
            end if;
        return new;
    end;
    $$;

create trigger report_ins_upd before insert or update on reports
    for each row
    execute function report_ins_upd();


--IMPEDIRE DELETE DI REPORT SU VERSIONI DI PROGETTI DEFINITIVAMENTE APPROVATI/NON APPROVATI
create or replace function report_del() returns trigger
language plpgsql
as
    $$
    begin
        if('approvato'=(select status from projects p join files f on p.uuid=f."ProjectUuid" join versions v
            on f.uuid =v."FileUuid" where v.uuid=old."VersionsUuid")
            OR
           'nonapprovato'=(select status from projects p join files f on p.uuid=f."ProjectUuid" join versions v
            on f.uuid =v."FileUuid" where v.uuid=OLD."VersionsUuid"))
            then return null;
            end if;
        return old;
    end;
    $$;

create trigger report_del before delete on reports
    for each row
    execute function report_del();
