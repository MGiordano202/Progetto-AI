# Simplified Explosive Bomberman (SEB)

## Descrizione del Progetto

Il progetto **Simplified Explosive Bomberman (SEB)** è un'implementazione semplificata del classico gioco **Bomberman**, sviluppata nell'ambito del corso di **Fondamenti di Intelligenza Artificiale** presso l'Università degli Studi di Salerno.

## Obiettivo

L'obiettivo del progetto è sviluppare un'intelligenza artificiale capace di risolvere il gioco di Bomberman utilizzando vari algoritmi, come A*, UCS e gli Algoritmi Genetici per ottimizzare la ricerca di soluzioni e strategie.

## Funzionalità
- **Algoritmi di ricerca**: L'algoritmo di **ricerca a costo uniforme** è utilizzato per calcolare il percorso ottimale tra il giocatore e l'obiettivo.
- **Algoritmi di ricerca**: L'algoritmo **A*** è utilizzato per calcolare il percorso tra il giocatore e l'obiettivo.
- **Algoritmo Genetico**: Viene impiegato un algoritmo genetico per trovare il percorso ottimale, utilizzando operatori di selezione, crossover e mutazione.


## Struttura del Codice

Il codice è strutturato in moduli separati, con una chiara divisione tra la logica di gioco e gli algoritmi di IA. I principali componenti sono:
-**Ricerca a Costo Uniforme**: Algoritmo di pathfinding che determina il percorso Ottimale tra due punti.
- **Astar**: Algoritmo di pathfinding utilizzato per determinare il percorso tra due punti.
- **Algoritmo Genetico**: Contiene la logica per generare, selezionare, incrociare e mutare gli individui, con lo scopo di ottimizzare il percorso del giocatore.

## Come Eseguire il Progetto

1. **Clonare il repository**:
   ```bash
   git clone https://github.com/MGiordano202/Simplified-Explosive-Bomberman-SEB
   ```
2. **Installare pygame**:
    Assicurati di avere **Python** installato sul tuo sistema. Puoi installare pygame come segue:
   ```bash
   pip install pygame
   ```
3. **Eseguire il gioco**:
   Una volta configurato l'ambiente, puoi eseguire il gioco con il comando:
   ```bash
   pytoh main.py
   ```

## Contributi

Se desideri contribuire al progetto, ti invitiamo a fare fork del repository e inviare una pull request con le tue modifiche. Assicurati di seguire le linee guida del progetto per garantire la coerenza del codice e migliorare la qualità complessiva.

## Licenza

Questo progetto è rilasciato sotto la Licenza MIT. Puoi copiare, modificare e distribuire il codice, ma ricordati di fornire il dovuto riconoscimento agli autori originali.
