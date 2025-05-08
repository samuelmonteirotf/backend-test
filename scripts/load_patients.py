import pandas as pd
import requests
from datetime import datetime
import uuid

# Configurações
FHIR_SERVER_URL = "http://localhost:8080/fhir"
CSV_PATH = "../data/patients.csv"
HEADERS = {"Content-Type": "application/fhir+json"}

# Função auxiliar para gerar um resource Patient
def build_patient_resource(row):
    return {
        "resourceType": "Patient",
        "identifier": [
            {
                "system": "http://munai.local/cpf",
                "value": row["CPF"]
            }
        ],
        "name": [
            {
                "use": "official",
                "text": row["Nome"]
            }
        ],
        "gender": "male" if row["Gênero"].strip().lower() == "masculino" else "female",
        "birthDate": datetime.strptime(row["Data de Nascimento"], "%d/%m/%Y").strftime("%Y-%m-%d"),
        "telecom": [
            {
                "system": "phone",
                "value": row["Telefone"],
                "use": "home"
            }
        ],
        "address": [
            {
                "country": row["País de Nascimento"]
            }
        ]
    }

# Função auxiliar para criar Observation(s) se houver
def build_observations(patient_id, raw_obs):
    observations = []
    for obs_text in raw_obs.split("|"):
        obs_text = obs_text.strip()
        if not obs_text:
            continue
        obs = {
            "resourceType": "Observation",
            "status": "final",
            "code": {
                "coding": [
                    {
                        "system": "http://loinc.org",
                        "code": "ASSERTION",
                        "display": obs_text
                    }
                ],
                "text": obs_text
            },
            "subject": {
                "reference": f"Patient/{patient_id}"
            },
            "effectiveDateTime": datetime.now().isoformat()
        }
        observations.append(obs)
    return observations

# Carrega o CSV
df = pd.read_csv(CSV_PATH, encoding="latin1")
print(f"Total de pacientes: {len(df)}")

# Loop para carga dos dados
for index, row in df.iterrows():
    try:
        patient = build_patient_resource(row)
        # Envia Patient
        resp = requests.post(f"{FHIR_SERVER_URL}/Patient", json=patient, headers=HEADERS)
        resp.raise_for_status()
        patient_id = resp.json()["id"]
        print(f"[✓] Paciente {row['Nome']} criado com ID: {patient_id}")

        # Se houver observações, envia também
        if pd.notna(row.get("Observação")):
            observations = build_observations(patient_id, row["Observação"])
            for obs in observations:
                resp_obs = requests.post(f"{FHIR_SERVER_URL}/Observation", json=obs, headers=HEADERS)
                resp_obs.raise_for_status()
                print(f"    → Observação registrada: {obs['code']['text']}")

    except Exception as e:
        print(f"[✗] Erro ao processar paciente {row['Nome']}: {str(e)}")
