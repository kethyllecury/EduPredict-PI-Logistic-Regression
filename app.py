import os
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

    if not p:
        p.append("Monitoramento")

    return " | ".join(p)

df["plano"] = df.apply(plano, axis=1)

# ----------------------------
# API
# ----------------------------

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/alunos")
def alunos():
    return jsonify(df[[
        "Nome",
        "Sobrenome",
        "risco_percentual",
        "nivel",
        "plano"
    ]].to_dict(orient="records"))

# ----------------------------
# RODAR
# ----------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)