# 📚 Sistema di Gestione Biblioteca

Un sistema completo e professionale per la gestione di una biblioteca, sviluppato in Python. Permette di gestire libri, utenti, prestiti e restituzioni con calcolo automatico delle multe per ritardo.

## 🎯 Funzionalità Principali

### 📖 Gestione Libri
- Aggiungere nuovi libri al catalogo
- Tracciare il numero di copie disponibili e totali
- Visualizzare l'elenco completo dei libri con disponibilità
- Registrare automaticamente i prestiti di ogni libro

### 👥 Gestione Utenti
- Registrare nuovi utenti della biblioteca
- Memorizzare dati anagrafici (nome, email)
- Tracciare la cronologia dei prestiti per ogni utente
- Visualizzare i prestiti attivi e le scadenze

### 🔄 Gestione Prestiti
- Prendere libri in prestito con controllo della disponibilità
- Limite massimo di 5 libri per utente
- Scadenza automatica dopo 14 giorni
- Visualizzazione chiara delle scadenze con avvisi (🟢🟡🔴)

### 📤 Gestione Restituzione
- Restituire libri in modo semplice e veloce
- Calcolo automatico delle multe per ritardo
- Multa giornaliera di €2,00 per giorni di ritardo
- Aggiornamento automatico della disponibilità

### 📊 Statistiche e Monitoraggio
- Dashboard con statistiche generali
- Tasso di utilizzo della biblioteca
- Storico completo dei prestiti
- Stato dei ritardi

---

## 📋 Struttura del Codice

### Classi Principali

#### `Libro`
Rappresenta un libro nel catalogo della biblioteca.

**Attributi:**
- `isbn`: Codice identificativo univoco
- `titolo`: Nome del libro
- `autore`: Autore del libro
- `anno`: Anno di pubblicazione
- `copie_disponibili`: Numero di copie disponibili
- `copie_totali`: Numero totale di copie
- `prestiti`: Lista dei prestiti effettuati

**Metodi:**
- `to_dict()`: Converte il libro in dizionario

#### `Utente`
Rappresenta un utente registrato della biblioteca.

**Attributi:**
- `id_utente`: ID univoco dell'utente
- `nome`: Nome completo
- `email`: Indirizzo email
- `libri_presi_in_prestito`: Lista dei prestiti attuali
- `data_registrazione`: Data di iscrizione

**Metodi:**
- `to_dict()`: Converte l'utente in dizionario

#### `Biblioteca`
Classe principale che gestisce tutta la logica della biblioteca.

**Attributi:**
- `nome`: Nome della biblioteca
- `libri`: Dizionario di tutti i libri
- `utenti`: Dizionario di tutti gli utenti
- `giorni_prestito`: Durata del prestito (default: 14 giorni)
- `multa_giornaliera`: Importo della multa al giorno (default: €2,00)

**Metodi Principali:**
- `aggiungi_libro(libro)`: Aggiunge un libro al catalogo
- `registra_utente(utente)`: Registra un nuovo utente
- `prendi_in_prestito(id_utente, isbn)`: Effettua un prestito
- `restituisci_libro(id_utente, isbn)`: Restituisce un libro
- `mostra_libri_disponibili()`: Visualizza tutti i libri
- `mostra_prestiti_utente(id_utente)`: Mostra i prestiti di un utente
- `genera_statistiche()`: Mostra le statistiche della biblioteca

---

## 🚀 Come Utilizzare

### 1. Importare le Classi
```python
from sistema_gestione_biblioteca import Libro, Utente, Biblioteca
