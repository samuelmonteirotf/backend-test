# 🧠 Backend Test – Integração com Servidor FHIR

Este projeto tem como objetivo demonstrar a ingestão de dados de pacientes a partir de um arquivo CSV, convertendo-os para o formato FHIR e persistindo-os em um servidor HAPI FHIR.

---

## 📌 Objetivo

> Automatizar o carregamento de um conjunto de pacientes (CSV) para um servidor FHIR local, garantindo a criação correta de recursos `Patient` e `Observation`, conforme as informações fornecidas.

---

## 📁 Estrutura do Projeto

```bash
project
├── data/
│   └── patients.csv            # Arquivo com os dados de entrada
├── docker/
│   └── docker-compose.yml      # Subida do servidor HAPI FHIR e Postgres
├── scripts/
│   ├── load_patients.py        # Script principal (teste técnico)
│   └── load_patients_bonus.py  # Script com bônus (uso de profile da RNDS)
├── requirements.txt
└── README.md
```

---

## 🐳 Subindo o Servidor FHIR

Este projeto utiliza [HAPI FHIR Server](https://hapifhir.io/) com suporte a PostgreSQL, tudo rodando em Docker.

### Pré-requisitos

- Docker
- Docker Compose

### Subir o ambiente

```bash
docker compose -f docker/docker-compose.yml up -d
```

Aguarde a inicialização completa (~30 segundos) e acesse:

- 🌐 Interface do FHIR: [http://localhost:8080/fhir](http://localhost:8080/fhir)
- 📃 OpenAPI (Swagger): [http://localhost:8080/fhir/api-docs](http://localhost:8080/fhir/api-docs)

---

## 🧪 Executando o Script Principal

### 1. Instale as dependências

> Recomendado: usar um ambiente virtual (venv, poetry, etc.)

```bash
pip install -r requirements.txt
```

### 2. Execute o script para carregar os pacientes

```bash
cd scripts/
python load_patients.py
```

Você pode verificar os dados carregados acessando:

- [http://localhost:8080/fhir/Patient](http://localhost:8080/fhir/Patient)

---

## 🏅 Adicional

O script `load_patients_bonus.py` implementa um requisito adicional:

✔️ **Adição de perfil oficial RNDS no recurso Patient**  
Cada recurso `Patient` enviado ao servidor inclui a seguinte referência de profile:

```json
"meta": {
  "profile": [
    "https://simplifier.net/redenacionaldedadosemsaude/brindividuo"
  ]
}
```

### Como executar

```bash
cd scripts/
python load_patients_bonus.py
```

---

## 👨‍💻 Autor

**Samuel**
