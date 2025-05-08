import pandas as pd
import requests
import json

FHIR_SERVER_URL = "http://localhost:8080/fhir"
PATIENT_PROFILE_URL = "https://simplifier.net/redenacionaldedadosemsaude/brindividuo"

HEADERS = {
    "Content-Type": "application/fhir+json"
}

CSV_PATH = "../data/patients.csv"


def criar_paciente(row):
    """Cria um recurso Patient no servidor FHIR com o profile da RNDS"""
    resource = {
        "resourceType": "Patient",
        "meta": {
            "profile": [PATIENT_PROFILE_URL]
        },
        "identifier": [{
            "system": "http://munai.local/cpf",
            "value": row["cpf"]
        }],
        "name": [{
            "use": "official",
            "text": row["nome"]
        }],
        "telecom": [{
            "system": "phone",
            "value": row["telefone"],
            "use": "home"
        }],
        "gender": row["sexo"].lower(),
        "birthDate": row["nascimento"],
        "address": [{
            "country": "Brasil"
        }]
    }

    response = requests.post(f"{FHIR_SERVER_URL}/Patient", headers=HEADERS, data=json.dumps(resource))
    if response.status_code in [200, 201]:
        patient_id = response.json()["id"]
        print(f"[✓] Paciente {row['nome']} criado com ID: {patient_id}")
        return patient_id
    else:
        print(f"[!] Erro ao criar paciente {row['nome']}: {response.status_code} - {response.text}")
        return None


def criar_observacoes(row, patient_id):
    """Cria recursos Observation com base na coluna 'observacao' do CSV"""
    observacoes_raw = str(row.get("observacao", "")).strip()
    if not observacoes_raw:
        return

    observacoes = [obs.strip() for obs in observacoes_raw.split(",") if obs.strip()]
    for obs in observacoes:
        resource = {
            "resourceType": "Observation",
            "status": "final",
            "code": {
                "text": obs
            },
            "subject": {
                "reference": f"Patient/{patient_id}"
            }
        }

        response = requests.post(f"{FHIR_SERVER_URL}/Observation", headers=HEADERS, data=json.dumps(resource))
        if response.status_code in [200, 201]:
            print(f"    → Observação registrada: {obs}")
        else:
            print(f"    [!] Erro ao criar observação '{obs}': {response.status_code} - {response.text}")


def main():
    df = pd.read_csv(CSV_PATH)
    print(f"Total de pacientes: {len(df)}")

    for _, row in df.iterrows():
        patient_id = criar_paciente(row)
        if patient_id:
            criar_observacoes(row, patient_id)


if __name__ == "__main__":
    main()
