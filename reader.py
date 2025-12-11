from fastapi import FastAPI
import sqlite3
import uvicorn

app = FastAPI()

# Base de données 
DB_NAME = "cloudDB.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row # Pour avoir des réponses lisibles
    return conn

# --- Route 1 : Lire tous les tickets 
@app.get("/tickets")
def lire_historique():
    conn = get_db_connection()
    tickets = conn.execute("SELECT * FROM tickets").fetchall()
    conn.close()
    return {"tickets": tickets}

# --- Route 2 : Lire les stats 
@app.get("/stats/chiffre_affaires")
def lire_stats():
    conn = get_db_connection()
    ca = conn.execute("SELECT magasin, SUM(total) FROM tickets GROUP BY magasin").fetchall()
    conn.close()
    return {"CA": ca}
    
@app.get("/stats/nombre_articles_magasin")
def nombre_articles_magasin():
    conn = get_db_connection()
    data = conn.execute("""
        SELECT t.magasin, COUNT(a.id_article) AS nombre_articles
        FROM tickets t
        JOIN article a ON t.id_ticket = a.id_ticket
        GROUP BY t.magasin
    """).fetchall()
    conn.close()
    return {"nombre_articles_par_magasin": data}

@app.get("/stats/prix_par_article_magasin")
def prix_par_article_magasin():
    conn = get_db_connection()
    data = conn.execute("""
        SELECT t.magasin, a.Article, SUM(a.quantite * a.prix_unitaire) AS total_article
        FROM tickets t
        JOIN article a ON t.id_ticket = a.id_ticket
        GROUP BY t.magasin, a.Article
    """).fetchall()
    conn.close()
    return {"prix_par_article_par_magasin": data}

@app.get("/stats/quantite_articles_magasin")
def quantite_articles_magasin():
    conn = get_db_connection()
    data = conn.execute("""
        SELECT t.magasin, SUM(a.quantite) AS quantite_totale
        FROM tickets t
        JOIN article a ON t.id_ticket = a.id_ticket
        GROUP BY t.magasin
    """).fetchAll()
    conn.close()
    return {"quantite_articles_par_magasin": data}



if __name__ == "__main__":
    # Port 8001 obligatoire car le producer utilise le 8000)
    uvicorn.run(app, host="0.0.0.0", port=8001)
