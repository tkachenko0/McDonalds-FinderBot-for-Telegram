# NLP-Project

- Cosa potrei fare?

    - Usare la funzione preprocessing visto che per ora non ne facciamo. Ti ho messo nel notebook due linee di codice commentato. 
    
    
    >>>> Modifiche apportate: Ho integrato la funzione preprocessing e ho inserito le righe di codice per togliere alcune parole e caratteri che comparivano nel testo. 
    >>>> Ho cambiato la firma di alcune funzioni per considereare la colonna "review_clean" e non più quella originale 
    
    
    > Attenzione se la utilizzi in fase di induzione e test con la funzione test_classifier, servirà che to lo faccia anche per la funzione predict_sentences(). Ma non credo ti serva usarla.

    - Testare diverse configurazioni di Tf-idf vectorizer come nel esempio del notebook medico

    - Provare gli altri due classificatori (nel codice c'è svm)

    - Provare a fare la funzione che in base alla posizione ed un raggio va a consigliare il ristorante in base al numero delle stelline
    
    >>>>>FATTA la si trova nel modulo utils.py

    - Replicare l'esperimento del tipo che non riesce a raggiungere una accuratezza alta classificando le recensioni in base al numero di stelline (nel codice del notebook abbiamo quello sulla sentiment analysis)

- Lui ha detto di provare un'altra libreria per fare un confronto senza specificare altri dettagli... Vedremo dopo che abbiamo fatto le nostre di prove
