# NLP-Project

- Dove posso trovare il dataset?

    Lo ho messo in gitignore e mandato su telegram. Mitti solo la cartella dataset nella root del progetto

- Dove posso scrivere?

    Ovunque, io sto lavorando sul file [nb_progetto.ipynb](nb_progetto.ipynb)

- Puoi leggerti velocemente il codice degli altri due notebook (consigliato) che adesso sono molto corti, oppure passare direttamente a [nb_progetto.ipynb](nb_progetto.ipynb). Ci sono alcune commenti che ti renderanno più facile capire cosa ho fatto, cosa serve fare (ad esempio il preprocessing) e dove andare a cercare codice già pronto.

- Cosa potrei fare?

    - Usare la funzione preprocessing visto che per ora non ne facciamo. Ti ho messo nel notebook due linee di codice commentato. 
    > Attenzione se la utilizzi in fase di induzione e test con la funzione test_classifier, servirà che to lo faccia anche per la funzione predict_sentences(). Ma non credo ti serva usarla.

    - Testare diverse configurazioni di Tf-idf vectorizer come nel esempio del notebook medico

    - Provare gli altri due classificatori (nel codice c'è svm)

    - Provare a fare la funzione che in base alla posizione ed un raggio va a consigliare il ristorante in base al numero delle stelline

    - Replicare l'esperimento del tipo che non riesce a raggiungere una accuratezza alta classificando le recensioni in base al numero di stelline (nel codice del notebook abbiamo quello sulla sentiment analysis)

- Lui ha detto di provare un'altra libreria per fare un confronto senza specificare altri dettagli... Vedremo dopo che abbiamo fatto le nostre di prove


> Insomma, tutta sta lettura per non capire nulla invece di passare a [nb_progetto.ipynb](nb_progetto.ipynb) per capire tutto in meno di 2 minuti. 😅