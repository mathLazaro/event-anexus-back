import re
from sqlite3 import IntegrityError


def parse_integrity_error(err: IntegrityError) -> str:
    orig = getattr(err, "orig", None)
    text = str(orig) if orig else str(err)

    m = re.search(r"UNIQUE constraint failed: (?:[\w_]+\.)?([\w_.]+)", text)
    if m:
        col = m.group(1).split(".")[-1]
        return {f"{col}": "Valor duplicado"}

    m = re.search(r"NOT NULL constraint failed: (?:[\w_]+\.)?([\w_.]+)", text)
    if m:
        col = m.group(1).split(".")[-1]
        return {f"{col}": "Não pode ser nulo."}

    if "duplicate key value violates unique constraint" in text.lower():
        m = re.search(r"Key \((.+)\)=\((.+)\)", text, re.IGNORECASE)
        if m:
            col = m.group(1)
            val = m.group(2)
            return {f"{col}": "Valor duplicado."}
        return {"error": "Violação de unique constraint (valor duplicado)."}

    m = re.search(
        r"Duplicate entry .* for key ['`\"]?([\w.]+)['`\"]?", text, re.IGNORECASE)
    if m:
        col = m.group(1).split(".")[-1]
        return {f"{col}": "Valor duplicado."}

    print("IntegrityError não mapeado: %s", text)
    return {"error": text}
