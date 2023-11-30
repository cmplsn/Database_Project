-- Definizione dei trigger
SET search_path TO project_schema;

-- Quando viene eliminato un Evaluator viene posto nelle altre tabelle
-- a lui associate un Evaluator fantasma

