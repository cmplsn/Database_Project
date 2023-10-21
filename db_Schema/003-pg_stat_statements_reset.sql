create function pg_stat_statements_reset(userid oid default 0, dbid oid default 0, queryid bigint default 0) returns void
    strict
    parallel safe
    language c
as
$$
begin
-- missing source code
end;
$$;

alter function pg_stat_statements_reset(oid, oid, bigint) owner to "user";

