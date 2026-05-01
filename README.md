# 🦠 Modelagem Epidemiológica e Autômatos Celulares

Este repositório registra um estudo desenvolvido no contexto de uma iniciação científica, com foco na modelagem matemática da propagação de doenças infecciosas e sua simulação computacional por meio de autômatos celulares.

O projeto busca conectar modelos epidemiológicos clássicos com abordagens discretas espaciais, investigando tanto suas capacidades quanto suas limitações.

---

## 🧠 Objetivos

* Estudar modelos epidemiológicos clássicos, com ênfase no modelo SIR
* Implementar simulações utilizando autômatos celulares (AC)
* Explorar a dinâmica espacial da propagação de doenças
* Analisar limitações numéricas e estruturais das abordagens utilizadas
* Investigar possíveis extensões do modelo

---

## 📚 Fundamentação Teórica

### Modelo SIR

O modelo SIR divide a população em três classes:

* **S (Suscetíveis)**
* **I (Infectados)**
* **R (Recuperados)**

A dinâmica clássica é dada por um sistema de equações diferenciais que descreve a evolução dessas populações ao longo do tempo.

---

### Autômatos Celulares

A abordagem por autômatos celulares permite:

* Introduzir estrutura espacial na modelagem
* Simular interações locais entre indivíduos
* Observar padrões emergentes da propagação

Cada célula da grade representa um indivíduo (ou região), cujo estado evolui conforme regras locais.

---

## ⚙️ Metodologia

### Discretização

A simulação foi construída a partir de uma aproximação discreta da dinâmica contínua do modelo SIR, utilizando uma abordagem inspirada no método de Euler.

Essa escolha permitiu:

* Simplicidade de implementação
* Controle direto sobre a dinâmica local

Por outro lado, também introduziu limitações numéricas importantes.

---

### Implementação

* Simulação em grade 2D
* Estados discretos: S, I, R
* Atualização baseada na vizinhança local
* Registro da evolução temporal dos infectados
* Visualização da dinâmica (quando aplicável)

---

## ⚠️ Limitações Identificadas

Durante o desenvolvimento, foram observados alguns pontos críticos:

### 1. Aproximação Numérica

* A discretização via Euler pode introduzir instabilidades
* Sensibilidade a parâmetros de passo temporal
* Diferenças em relação ao modelo contínuo

---

### 2. Modelagem SIR

* Ausência de reinfecção limita a aplicabilidade do modelo
* Dificuldade em capturar dinâmicas mais realistas

---

### 3. Estrutura do Autômato Celular

* Dependência forte da definição de vizinhança
* Simplificações no processo de contágio
* Necessidade de calibrar parâmetros locais

---

## 🔍 Resultados e Explorações

* Simulação da propagação espacial de infecções
* Análise qualitativa das curvas de infectados
* Observação de padrões emergentes na grade
* Comparação implícita com comportamento esperado do modelo contínuo

---

## 🚀 Possíveis Extensões

O projeto abre diversas possibilidades de aprofundamento:

### Modelagem

* Extensão para modelo SIRS (com perda de imunidade)
* Inclusão de natalidade e mortalidade
* Modelos mais complexos (SEIR, por exemplo)

### Numérico

* Métodos mais estáveis que Euler
* Ajuste de parâmetros com base em dados

### Computacional

* Otimização da simulação
* Execuções em lote para análise estatística
* Visualizações mais sofisticadas

---


## 📌 Contexto Acadêmico

Este trabalho foi desenvolvido no contexto de uma iniciação científica, com caráter exploratório e investigativo.

Mais do que apresentar soluções definitivas, o objetivo foi compreender profundamente os desafios envolvidos na modelagem e simulação de fenômenos epidemiológicos.

---

## 🤝 Contribuições

Discussões, sugestões e melhorias são bem-vindas!
