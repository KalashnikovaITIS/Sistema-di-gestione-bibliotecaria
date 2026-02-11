import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class Libro:
    """Classe che rappresenta un libro in biblioteca"""
    def __init__(self, isbn: str, titolo: str, autore: str, anno: int, copie_disponibili: int):
        self.isbn = isbn
        self.titolo = titolo
        self.autore = autore
        self.anno = anno
        self.copie_disponibili = copie_disponibili
        self.copie_totali = copie_disponibili
        self.prestiti = []

    def __str__(self):
        return f"{self.titolo} di {self.autore} ({self.anno})"

    def to_dict(self):
        return {
            "isbn": self.isbn,
            "titolo": self.titolo,
            "autore": self.autore,
            "anno": self.anno, 
            "copie_disponibili": self.copie_disponibili,
            "copie_totali": self.copie_totali
        }


class Utente:
    """Classe che rappresenta un utente della biblioteca"""
    def __init__(self, id_utente: str, nome: str, email: str):
        self.id_utente = id_utente
        self.nome = nome
        self.email = email
        self.libri_presi_in_prestito: List[Dict] = []
        self.data_registrazione = datetime.now()

    def __str__(self):
        return f"Utente: {self.nome} ({self.id_utente})"

    def to_dict(self):
        return {
            "id_utente": self.id_utente,
            "nome": self.nome,
            "email": self.email,
            "libri_in_prestito": len(self.libri_presi_in_prestito),
            "data_registrazione": self.data_registrazione.strftime("%Y-%m-%d")
        }


class Biblioteca:
    """Classe principale che gestisce la biblioteca"""
    def __init__(self, nome: str):
        self.nome = nome
        self.libri: Dict[str, Libro] = {}
        self.utenti: Dict[str, Utente] = {}
        self.giorni_prestito = 14
        self.multa_giornaliera = 2.0  # Euro al giorno

    def aggiungi_libro(self, libro: Libro) -> bool:
        """Aggiunge un libro alla biblioteca"""
        if libro.isbn in self.libri:
            print(f"❌ Errore: Il libro {libro.isbn} è già presente")
            return False
        
        self.libri[libro.isbn] = libro
        print(f"✅ Libro '{libro.titolo}' aggiunto con successo")
        return True

    def registra_utente(self, utente: Utente) -> bool:
        """Registra un nuovo utente"""
        if utente.id_utente in self.utenti:
            print(f"❌ Errore: L'utente {utente.id_utente} è già registrato")
            return False
        
        self.utenti[utente.id_utente] = utente
        print(f"✅ Utente '{utente.nome}' registrato con successo")
        return True

    def prendi_in_prestito(self, id_utente: str, isbn: str) -> bool:
        """Permette a un utente di prendere un libro in prestito"""
        if id_utente not in self.utenti:
            print(f"❌ Utente non trovato")
            return False
        
        if isbn not in self.libri:
            print(f"❌ Libro non trovato")
            return False
        
        libro = self.libri[isbn]
        utente = self.utenti[id_utente]

        if libro.copie_disponibili <= 0:
            print(f"❌ Nessuna copia disponibile di '{libro.titolo}'")
            return False

        if len(utente.libri_presi_in_prestito) >= 5:
            print(f"❌ Limite di 5 libri in prestito raggiunto")
            return False

        # Registra il prestito
        data_prestito = datetime.now()
        data_scadenza = data_prestito + timedelta(days=self.giorni_prestito)
        
        prestito = {
            "isbn": isbn,
            "titolo": libro.titolo,
            "data_prestito": data_prestito.strftime("%Y-%m-%d %H:%M"),
            "data_scadenza": data_scadenza.strftime("%Y-%m-%d"),
            "restituito": False,
            "multa": 0.0
        }

        utente.libri_presi_in_prestito.append(prestito)
        libro.prestiti.append(prestito)
        libro.copie_disponibili -= 1

        print(f"✅ '{libro.titolo}' preso in prestito da {utente.nome}")
        print(f"   Restituire entro il: {data_scadenza.strftime('%d-%m-%Y')}")
        return True

    def restituisci_libro(self, id_utente: str, isbn: str) -> Optional[float]:
        """Restituisce un libro e calcola eventuali multe"""
        if id_utente not in self.utenti:
            print(f"❌ Utente non trovato")
            return None

        utente = self.utenti[id_utente]
        libro = self.libri.get(isbn)

        # Trova il prestito attivo
        prestito = None
        for p in utente.libri_presi_in_prestito:
            if p["isbn"] == isbn and not p["restituito"]:
                prestito = p
                break

        if not prestito:
            print(f"❌ Nessun prestito attivo trovato")
            return None

        # Calcola la multa se in ritardo
        data_scadenza = datetime.strptime(prestito["data_scadenza"], "%Y-%m-%d")
        giorni_ritardo = (datetime.now() - data_scadenza).days

        multa = 0.0
        if giorni_ritardo > 0:
            multa = giorni_ritardo * self.multa_giornaliera
            print(f"⚠️  Libro restituito in ritardo di {giorni_ritardo} giorni")
            print(f"   Multa: €{multa:.2f}")

        prestito["restituito"] = True
        prestito["multa"] = multa
        libro.copie_disponibili += 1

        print(f"✅ '{prestito['titolo']}' restituito da {utente.nome}")
        return multa

    def mostra_libri_disponibili(self):
        """Mostra tutti i libri disponibili"""
        print("\n" + "="*60)
        print(f"📚 LIBRI DISPONIBILI IN {self.nome.upper()}")
        print("="*60)

        if not self.libri:
            print("Nessun libro in biblioteca")
            return

        for isbn, libro in self.libri.items():
            status = "✅ Disponibile" if libro.copie_disponibili > 0 else "❌ Non disponibile"
            print(f"\n📖 {libro.titolo}")
            print(f"   Autore: {libro.autore} ({libro.anno})")
            print(f"   Copie: {libro.copie_disponibili}/{libro.copie_totali}")
            print(f"   {status}")

    def mostra_prestiti_utente(self, id_utente: str):
        """Mostra i prestiti attivi di un utente"""
        if id_utente not in self.utenti:
            print(f"❌ Utente non trovato")
            return

        utente = self.utenti[id_utente]
        print(f"\n📋 Prestiti di {utente.nome}:")
        print("-" * 50)

        prestiti_attivi = [p for p in utente.libri_presi_in_prestito if not p["restituito"]]

        if not prestiti_attivi:
            print("Nessun libro in prestito")
            return

        for prestito in prestiti_attivi:
            data_scadenza = datetime.strptime(prestito["data_scadenza"], "%Y-%m-%d")
            giorni_rimanenti = (data_scadenza - datetime.now()).days
            
            if giorni_rimanenti < 0:
                print(f"🔴 {prestito['titolo']} (IN RITARDO di {abs(giorni_rimanenti)} giorni)")
            elif giorni_rimanenti <= 3:
                print(f"🟡 {prestito['titolo']} (Scade in {giorni_rimanenti} giorni)")
            else:
                print(f"🟢 {prestito['titolo']} (Scade in {giorni_rimanenti} giorni)")

    def genera_statistiche(self):
        """Genera statistiche sulla biblioteca"""
        print("\n" + "="*60)
        print("📊 STATISTICHE BIBLIOTECA")
        print("="*60)

        total_libri = sum(libro.copie_totali for libro in self.libri.values())
        libri_disponibili = sum(libro.copie_disponibili for libro in self.libri.values())
        libri_prestati = total_libri - libri_disponibili

        print(f"Numero titoli: {len(self.libri)}")
        print(f"Totale copie: {total_libri}")
        print(f"Copie disponibili: {libri_disponibili}")
        print(f"Copie in prestito: {libri_prestati}")
        print(f"Numero utenti registrati: {len(self.utenti)}")
        print(f"Tasso di utilizzo: {(libri_prestati/total_libri*100):.1f}%" if total_libri > 0 else "0%")


# ============ DEMO DEL SISTEMA ============

if __name__ == "__main__":
    # Creazione della biblioteca
    bib = Biblioteca("Biblioteca Centrale")

    print("🚀 SISTEMA DI GESTIONE BIBLIOTECA\n")

    # Aggiunta di libri
    print("📖 Aggiunta libri...")
    bib.aggiungi_libro(Libro("978-0-06-112008-4", "Il Grande Gatsby", "F. Scott Fitzgerald", 1925, 3))
    bib.aggiungi_libro(Libro("978-0-14-303943-3", "1984", "George Orwell", 1949, 2))
    bib.aggiungi_libro(Libro("978-0-7432-7356-5", "Il Signore degli Anelli", "J.R.R. Tolkien", 1954, 1))
    bib.aggiungi_libro(Libro("978-0-13-110362-7", "Clean Code", "Robert C. Martin", 2008, 5))

    # Registrazione utenti
    print("\n👥 Registrazione utenti...")
    bib.registra_utente(Utente("U001", "Marco Rossi", "marco@email.com"))
    bib.registra_utente(Utente("U002", "Anna Bianchi", "anna@email.com"))
    bib.registra_utente(Utente("U003", "Luca Verdi", "luca@email.com"))

    # Prestiti
    print("\n🔄 Gestione prestiti...")
    bib.prendi_in_prestito("U001", "978-0-06-112008-4")
    bib.prendi_in_prestito("U001", "978-0-14-303943-3")
    bib.prendi_in_prestito("U002", "978-0-7432-7356-5")
    bib.prendi_in_prestito("U003", "978-0-13-110362-7")

    # Mostra libri disponibili
    bib.mostra_libri_disponibili()

    # Mostra prestiti
    print("\n")
    bib.mostra_prestiti_utente("U001")
    bib.mostra_prestiti_utente("U002")

    # Restituzione
    print("\n📤 Restituzione libri...")
    bib.restituisci_libro("U001", "978-0-06-112008-4")

    # Statistiche
    bib.genera_statistiche()

# codice fatto da Kalaskova_itis (utilizzabile tranquillamente in modo gratuito)
# creato il 10/02/2026
