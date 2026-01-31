import json
from src.rag.retriever import retrieve_chunks
from src.llm.chat_model import complete



# Fonction interne qui crée le contexte à partir des chunk récupérer par le retriever
def _build_context(chunks: list[dict]) -> str:
    return "\n\n".join(f"EXCERPT:\n{c['text']}" for c in chunks)  # On concatène tous les textes des chunks en les séparant par des sauts de ligne
                                                               # Chaque chunk est précédé du mot "EXCERPT" pour bien signaler au modèle
                                                                # qu’il s’agit d’extraits du texte original


# Fonction principale qui construit le prompt envoyé au LLM
def build_prompt(question: str, chunks: list[dict], history: list[str]) -> str:
    context = _build_context(chunks)     # Construction du bloc de contexte à partir des chunks récupérés par le retriever
    history_block = "\n".join(history) if history else "" # Construction de l’historique de conversation sous forme de texte, s’il n’y a pas d’historique, on met une chaîne vide

    # Retour du prompt complet sous forme de string
    return f"""
You are a literature assistant answering questions about Shakespeare's Othello.

Conversation history:
{history_block}

Context excerpts from the play:
{context}

Question:
{question}

Instructions:
- YOU KNOW ONLY ABOUT OTHELLO IF SOMEONE ASK YOU ABOUT OTHTER OPERA IT'S NOT YOUR ROLE (but considere title like OTHELLO with spelling mistakes)
- Answer the question directly and concisely.
- Use the context ONLY as background knowledge.
- DO NOT repeat, summarize, or paraphrase the context in the answer.
- DO NOT mention the context explicitly.
- Write a single, clean answer as if you already knew the play.

CITATIONS RULES (VERY IMPORTANT):
- Citations MUST be copied verbatim from the excerpts.
- Do NOT summarize or shorten citations.
- Each citation must be at least 2 full sentences when possible.
- Prefer longer excerpts over short ones.
- If a paragraph is too short, include the following paragraph as well.
- Do NOT invent or modify any wording.

At the end, add citations using the exact format below:

---SOURCES---
<verbatim excerpt 1>
<verbatim excerpt 2>
<verbatim excerpt 3>

Do not add anything after the sources.

""".strip()


# Fonction qui orchestre toute la chaîne de question/réponse
def answer_question(question: str, history: list[str] | None = None) -> dict:
    
    history = history or [] # Si aucun historique n’est fourni, on utilise une liste vide

    
    chunks = retrieve_chunks(question, k=5) # Recherche les 5 chunks les plus pertinents dans la base vectorielle


    prompt = build_prompt(question, chunks, history)  # Construction du prompt complet avec la question, le contexte et l’historique
 
    # Appel du LLM en mode non-streaming pour obtenir la réponse brute
    raw = complete(
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    
    data = json.loads(raw)# Parsing du JSON de réponse

    
    cite_ids = data.get("cite_paragraph_ids", []) # Récupération des IDs de paragraphes cités par le modèle pour les sources

    # Construction d’un dictionnaire qui mappe chaque ID de paragraphe à son texte
    id_to_text = {}
    for c in chunks:
        for pid in c["paragraph_ids"]:
            if pid not in id_to_text:
                id_to_text[pid] = c["text"]

    # Reconstruction des citations à partir des IDs
    citations = []
    for pid in cite_ids:
        txt = id_to_text.get(pid)
        if txt:
            citations.append(txt[:200].replace("\n", " ") + "...") # On limite volontairement la longueur pour éviter des citations trop longues

    # Retour final sous forme de dictionnaire structuré 
    return {
        "answer": data.get("answer", ""),
        "citations": citations,
    }
