import pandas as pd

# --- Dados de exemplo ---
data = [
    {"nome": "Maria", "procedimento": "ITM", "data_hora_bot": "2025-08-04 08:28", "info_medico": "04/08 ANEXAR TAL COISA. ITM"},
    {"nome": "Maria", "procedimento": "ITM", "data_hora_bot": "2025-08-05 10:15", "info_medico": "04/08 ANEXAR TAL COISA. ITM - 05/08 SOLICITAR PARECER COISA. ITM"},
    {"nome": "Maria", "procedimento": "ITM", "data_hora_bot": "2025-08-06 11:00", "info_medico": "06/08 OUTRA COISA NOVA"}
]

df = pd.DataFrame(data)
df["data_hora_bot"] = pd.to_datetime(df["data_hora_bot"])

# --- Reconstrução do histórico ---
historico_acumulado = []
info_completo_por_linha = []

for _, row in df.sort_values("data_hora_bot").iterrows():
    partes = [p.strip() for p in row["info_medico"].split("-")]
    for parte in partes:
        if parte not in historico_acumulado:
            historico_acumulado.append(parte)
    # adiciona a versão completa do histórico até essa linha
    info_completo_por_linha.append(" - ".join(historico_acumulado))

df["info_medico_completo"] = info_completo_por_linha

# --- Mostrar o resultado ---
print(df[["info_medico_completo"]])

ultima_linha = df.iloc[-1]

# mostrar apenas o texto completo do histórico
print(ultima_linha["info_medico_completo"])
