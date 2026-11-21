# Direzione di gioco

## Idea

Un action open-world dall'alto, con città notturna, controlli immediati e colori da console a 32 bit. **Liberty Bay** è una città originale: scegli fra Nico, Mara, Teo e Lia e accetta incarichi dai telefoni sparsi per quattro quartieri.

L'identità è quella di un gioco arcade compatto: strade leggibili, edifici che bloccano il passaggio, auto da rubare, pedoni e traffico, polizia che risponde ai crimini, casse bonus e obiettivi chiari. Il livello di ricercato cresce con le azioni del giocatore; scappare lo riduce, mentre una mazzetta lo azzera. L'introduzione presenta in sequenza SN Colors come publisher e SN Colors Studio come team di sviluppo. Logo, colonna sonora ed effetti sono originali.

## Ciclo della prima missione

1. Scegli uno dei quattro personaggi e rispondi al telefono.
2. Recupera le buste per completare il primo incarico.
3. Accetta il secondo incarico, ruba un'auto e portala alla rimessa.
4. Evita le pattuglie, raccogli casse e aumenta il punteggio con il moltiplicatore.

Le pattuglie seguono la rete stradale e tentano di arrestare il giocatore. Se ti prendono, il ricercato si azzera, perdi le munizioni e il moltiplicatore si dimezza. Tre stazioni radio originali si possono cambiare mentre si guida.

## Scelte tecniche

- Pygame apre una finestra 16:9 e disegna a bassa risoluzione, ingrandendo i pixel per richiamare l'aspetto PS1.
- Il tasto F11 e l'opzione nel menu attivano lo schermo intero; musica, effetti, modalità schermo e lingua vengono salvati in `settings.json`.
- La localizzazione interna copre italiano, inglese, francese e spagnolo.
- Il mondo è generato con primitive e colori originali. Musica ed effetti sonori sono sintetizzati, quindi il prototipo non richiede file audio o immagini.
- `main.py` contiene il prototipo in un unico file per renderlo semplice da avviare e modificare. Quando aumentano missioni e sistemi, si potranno separare città, audio e interfaccia in moduli dedicati.

## Prossimi passi

1. Aggiungere nuove missioni telefoniche e luoghi riconoscibili.
2. Rifinire collisioni, servizi di emergenza e comportamenti della polizia.
3. Dare ai personaggi e ai veicoli più animazioni e caratteristiche.
