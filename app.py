import os
import math
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

app = Flask(__name__, static_folder=".")
CORS(app)

# ----------------------------
# CARREGAR DADOS
# ----------------------------

df = pd.read_excel("base_dados_alunos.xlsx")

# ----------------------------
# CRIAR VARIÁVEL DE RISCO
# ----------------------------

df["risco_evasao"] = (
    (df["Faltas_Consecutivas"] >= 5) |
    (df["Percentual_Presenca"] < 75) |
    (df["Entrega_Atividades"] < 50) |
    (df["Participacao"] == "Baixa") |
    (df["Reprovacoes_Anteriores"] >= 2)
).astype(int)

# ----------------------------
# TRATAR CATEGÓRICAS
# ----------------------------

df["Participacao"] = df["Participacao"].map({"Baixa":0,"Media":1,"Alta":2})
df["Apoio_Familiar"] = df["Apoio_Familiar"].map({"Baixo":0,"Medio":1,"Alto":2})
df["Comportamento"] = df["Comportamento"].map({"Ruim":0,"Regular":1,"Bom":2})

# ----------------------------
# FEATURES
# ----------------------------

X = df[[
    "Frequencia_Indireta","Nota","Faltas","Percentual_Presenca",
    "Faltas_Consecutivas","Atrasos","Participacao",
    "Entrega_Atividades","Reprovacoes_Anteriores",
    "Apoio_Familiar","Comportamento"
]].fillna(0)

y = df["risco_evasao"]

# ----------------------------
# MODELO
# ----------------------------

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = LogisticRegression()
model.fit(X_scaled, y)

# ----------------------------
# GERAR RISCO
# ----------------------------

df["risco_percentual"] = model.predict_proba(X_scaled)[:,1] * 100

# ----------------------------
# CLASSIFICAÇÃO
# ----------------------------

def classificar(r):
    if r < 30:
        return "Baixo"
    elif r < 70:
        return "Médio"
    else:
        return "Alto"

df["nivel"] = df["risco_percentual"].apply(classificar)

# ----------------------------
# PLANO
# ----------------------------

def plano(row):
    p = []
    if row["Faltas_Consecutivas"] > 5:
        p.append("Contato com responsável")
    if row["Entrega_Atividades"] < 50:
        p.append("Reforço escolar")
    if row["Participacao"] == 0:
        p.append("Aulas interativas")
    if row["Percentual_Presenca"] < 75:
        p.append("Plano de frequência")
    if row["Reprovacoes_Anteriores"] >= 2:
        p.append("Plano pedagógico individual")
    if not p:
        p.append("Monitoramento")
    return " | ".join(p)

df["plano"] = df.apply(plano, axis=1)

# ----------------------------
# TEMPO DE RECUPERAÇÃO
# ----------------------------

def tempo_recuperacao(row):
    if row["nivel"] == "Alto":
        return "3 a 6 meses"
    elif row["nivel"] == "Médio":
        return "1 a 3 meses"
    else:
        return "Monitoramento leve"

df["tempo_recuperacao"] = df.apply(tempo_recuperacao, axis=1)

# ----------------------------
# PROFESSOR INDICADO
# ----------------------------

def professor_indicado(row):
    if row["Participacao"] == 0:
        return "Prof. Engajador"
    elif row["Nota"] < 5:
        return "Prof. Técnico"
    elif row["Faltas_Consecutivas"] > 5:
        return "Prof. Tutor"
    else:
        return "Prof. Regular"

df["professor_indicado"] = df.apply(professor_indicado, axis=1)

# ----------------------------
# API
# ----------------------------

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

def _clean(v):
    if isinstance(v, float) and math.isnan(v):
        return None
    return v

def to_safe_records(frame):
    return [{k: _clean(v) for k, v in row.items()}
            for row in frame.to_dict(orient="records")]

def safe_mean(series, decimals=1):
    val = series.mean()
    return round(float(val), decimals) if not math.isnan(val) else 0.0

@app.route("/alunos")
def alunos():
    cols = [
        "Nome", "Sobrenome", "risco_percentual", "nivel", "plano",
        "Nota", "Faltas", "Percentual_Presenca", "Faltas_Consecutivas",
        "Entrega_Atividades", "tempo_recuperacao", "professor_indicado"
    ]
    result = df[cols].sort_values("risco_percentual", ascending=False)
    return jsonify(to_safe_records(result))

@app.route("/stats")
def stats():
    contagem = df["nivel"].value_counts().to_dict()
    top10 = to_safe_records(
        df.nlargest(10, "risco_percentual")[["Nome", "Sobrenome", "risco_percentual"]]
    )
    return jsonify({
        "total": len(df),
        "por_nivel": {
            "Alto": int(contagem.get("Alto", 0)),
            "Medio": int(contagem.get("Médio", 0)),
            "Baixo": int(contagem.get("Baixo", 0)),
        },
        "media_nota": safe_mean(df["Nota"]),
        "media_presenca": safe_mean(df["Percentual_Presenca"]),
        "media_faltas": safe_mean(df["Faltas"]),
        "top10_risco": top10,
    })

# ----------------------------
# RODAR
# ----------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)