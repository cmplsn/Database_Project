create type evaluations_enum as enum ('approvato', 'sottomesso per valutazione', 'richiede modifiche', 'non approvato');

alter type evaluations_enum owner to "user";

