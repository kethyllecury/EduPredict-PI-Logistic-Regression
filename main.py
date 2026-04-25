import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, roc_auc_score

# ----------------------------
# 1. CARREGAR BASE
# ----------------------------

df = pd.read_excel("base_dados_alunos_2000.xlsx")

# ----------------------------
# 2. CRIAR VARIÁVEL DE RISCO (REGRA BASE)
# ----------------------------

df["risco_evasao"] = (
    (df["Faltas_Consecutivas"] >= 5) |
    (df["Percentual_Presenca"] < 75) |
    (df["Entrega_Atividades"] < 50) |
    (df["Participacao"] == "Baixa") |
    (df["Reprovacoes_Anteriores"] >= 2)
).astype(int)

# ----------------------------
# 3. TRATAR CATEGÓRICAS
# ----------------------------

df["Participacao"] = df["Participacao"].map({
    "Baixa": 0,
    "Media": 1,
    "Alta": 2
})

df["Apoio_Familiar"] = df["Apoio_Familiar"].map({
    "Baixo": 0,
    "Medio": 1,
    "Alto": 2
})

df["Comportamento"] = df["Comportamento"].map({
    "Ruim": 0,
    "Regular": 1,
    "Bom": 2
})

# ----------------------------
# 4. FEATURES E TARGET
# ----------------------------

X = df[[
    "Frequencia_Indireta",
    "Nota",
    "Faltas",
    "Percentual_Presenca",
    "Faltas_Consecutivas",
    "Atrasos",
    "Participacao",
    "Entrega_Atividades",
    "Reprovacoes_Anteriores",
    "Apoio_Familiar",
    "Comportamento"
]].fillna(0)

y = df["risco_evasao"]

# ----------------------------
# 5. NORMALIZAÇÃO
# ----------------------------

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ----------------------------
# 6. TREINO E TESTE
# ----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# ----------------------------
# 7. TREINAR MODELO
# ----------------------------

model = LogisticRegression()
model.fit(X_train, y_train)

# ----------------------------
# 8. PREVISÕES
# ----------------------------

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

# ----------------------------
# 9. AVALIAÇÃO
# ----------------------------

print("Acurácia:", accuracy_score(y_test, y_pred))
print("Matriz de Confusão:\n", confusion_matrix(y_test, y_pred))
print("Relatório:\n", classification_report(y_test, y_pred))
print("AUC-ROC:", roc_auc_score(y_test, y_prob))

# ----------------------------
# 10. GERAR PROBABILIDADE PARA TODOS
# ----------------------------

df["prob_risco"] = model.predict_proba(X_scaled)[:, 1]
df["risco_percentual"] = df["prob_risco"] * 100

# ----------------------------
# 11. CLASSIFICAÇÃO DE RISCO
# ----------------------------

def classificar(risco):
    if risco < 30:
        return "Baixo"
    elif risco < 70:
        return "Médio"
    else:
        return "Alto"

df["nivel_risco"] = df["risco_percentual"].apply(classificar)

# ----------------------------
# 12. TEMPO DE RECUPERAÇÃO
# ----------------------------

def tempo_recuperacao(row):
    if row["nivel_risco"] == "Alto":
        return "3 a 6 meses"
    elif row["nivel_risco"] == "Médio":
        return "1 a 3 meses"
    else:
        return "Monitoramento leve"

df["tempo_recuperacao"] = df.apply(tempo_recuperacao, axis=1)

# ----------------------------
# 13. INDICAÇÃO DE PROFESSOR
# ----------------------------

def indicar_professor(row):
    if row["Participacao"] == 0:
        return "Professor Engajador"
    elif row["Nota"] < 5:
        return "Professor Técnico"
    elif row["Faltas_Consecutivas"] > 5:
        return "Professor Tutor"
    else:
        return "Professor Regular"

df["professor_indicado"] = df.apply(indicar_professor, axis=1)

# ----------------------------
# 14. PLANO PERSONALIZADO
# ----------------------------

def plano_acao(row):
    plano = []

    if row["Faltas_Consecutivas"] > 5:
        plano.append("Contato com responsável")

    if row["Percentual_Presenca"] < 75:
        plano.append("Plano de frequência")

    if row["Entrega_Atividades"] < 50:
        plano.append("Reforço em atividades")

    if row["Participacao"] == 0:
        plano.append("Aulas mais interativas")

    if row["Reprovacoes_Anteriores"] >= 2:
        plano.append("Plano pedagógico individual")

    if not plano:
        plano.append("Monitoramento padrão")

    return " | ".join(plano)

df["plano_recuperacao"] = df.apply(plano_acao, axis=1)

# ----------------------------
# 15. RESULTADO FINAL
# ----------------------------

resultado = df[[
    "Matricula",
    "Nome",
    "Sobrenome",
    "risco_percentual",
    "nivel_risco",
    "tempo_recuperacao",
    "professor_indicado",
    "plano_recuperacao"
]]

# ordenar por maior risco
resultado = resultado.sort_values(by="risco_percentual", ascending=False)

print(resultado.head(50))

# ----------------------------
# 16. GRÁFICO
# ----------------------------

plt.figure(figsize=(10,6))
plt.hist(df["risco_percentual"], bins=30)
plt.title("Distribuição do Risco de Evasão (%)")
plt.xlabel("Risco (%)")
plt.ylabel("Quantidade de Alunos")
plt.show()
