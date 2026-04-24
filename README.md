# 📊 Previsão de Evasão Escolar - Sistema de Apoio à Gestão Educacional

Este projeto utiliza Regressão Logística para prever o risco de evasão escolar com base em dados acadêmicos e comportamentais dos alunos. O objetivo é apoiar instituições de ensino na identificação precoce de estudantes em risco, permitindo intervenções antes que a evasão aconteça.

---

## 🎯 Objetivo

Construir um modelo preditivo capaz de identificar alunos com maior probabilidade de evasão escolar, utilizando variáveis como:

- desempenho acadêmico (notas)
- frequência escolar
- número de faltas
- ocorrências disciplinares
- avaliação/recomendação do professor

O foco não é substituir decisões humanas, mas fornecer suporte inteligente para ações preventivas.

---

## 🧱 Estrutura do Projeto

### 📥 Leitura e Preparação dos Dados

- Arquivo de entrada: `dados_alunos.xlsx`
- Etapas:
  - remoção de duplicatas
  - tratamento de valores ausentes
  - padronização de dados

---

### 🧮 Criação de Variáveis

- média de notas
- percentual de frequência
- total de faltas
- ocorrências disciplinares


### 📊 Estatísticas por Aluno

- consolidação de indicadores individuais
- análise de desempenho e comportamento

---

### 🤖 Modelo de Previsão

- Algoritmo: Regressão Logística
- Objetivo: prever a probabilidade de evasão escolar

---

### 📈 Avaliação do Modelo

Métricas utilizadas:

- Acurácia  
- Matriz de Confusão  
- Precision, Recall e F1-score  
- AUC-ROC  

---

### 📉 Visualizações

- distribuição de frequência vs evasão  
- relação entre notas e evasão  
- análise de faltas por grupo de risco  

---

## ⚙️ Requisitos

Instale as dependências:

```bash
pip install pandas numpy matplotlib scikit-learn
