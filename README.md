# Progetto d'esame del corso di Basi di Dati - A.A. 2022/2023

Creazione di una Web App che utilizza Database di tipo relazionale (PostgreSQL).

L'applicazione è stata pensata, su traccia del Professore del corso, come portale di gestione dei progetti di ricerca di un ente. 
Essa deve rendere possibile la registrazione autonoma di nuovi utenti di tipo Ricercatore e l'inserimento invece solo da parte dell'Admin di nuovi Valutatori.
Viene inoltre implementata una sezione di messaggistica di base per permettere la comunicazione tra Ricercatore ed uno dei Valutatori (in forma anonima)

Le tre tipologie di utenti sono:

- Admin

- Valutatore: revisiona i progetti di ricerca, con eventuali commenti, e vi assegna un giudizio tra "Approvato", "Non Approvato", "In attesa di modifiche".
  Una volta che un progetto viene valutato come "Approvato" o "Non Approvato" esso viene considerato come concluso e non ne è più possibile la modifica o l'upload di altre versioni.

- Ricercatore: colui che può eseguire l'upload di nuovi progetti di ricerca in formato PDF e ne può modificare la versione fino a quando un Valutatore
  non vi assegna un gidizio finale.

  
