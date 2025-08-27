from collections import Counter
import pandas as pd
import re


def contar_total(df):
    procedimentos = df["nome_procedimento"].dropna().str.strip()
    procedimentos = procedimentos[procedimentos != ""]
    return Counter(procedimentos)

# Conta só procedimentos com a palavra (ex.: "COBRO")
def contar_com_palavra(df, palavra="COBRO"):
    filtrado = df[df["info_assistente"].str.contains(palavra, case=False, na=False)]
    procedimentos = filtrado["nome_procedimento"].dropna().str.strip()
    procedimentos = procedimentos[procedimentos != ""]
    return Counter(procedimentos)

def top_procedimentos(df, top=20):

    total = contar_total(df)
    top_lista = total.most_common(top)
    df_top = pd.DataFrame(top_lista, columns=["Procedimentos", "Quantidade"])
     
    return df_top

def filter_by_word(df, word, column="nome_procedimento"):
    return df[df[column].str.contains(word, case=False, na=False)]

def procedimentos_quantidade_total_palavra(df, palavra="COBRO"):
    cobro = contar_com_palavra(df, palavra)
    total = contar_total(df)

    dados = []
    for proc, qtd_total in total.items():
        qtd_cobro = cobro.get(proc, 0)  # pega do cobro, se não tiver vira 0
        dados.append([proc, qtd_total, qtd_cobro])

    df_final = pd.DataFrame(dados, columns=["Procedimentos", "Quantidade_Total", f"Quantidade_{palavra}"])
    return df_final.sort_values(by=f"Quantidade_{palavra}", ascending=False).reset_index(drop=True).head(20)

def procedimento_media_dias_resolver_parecer(df, column_info="info_assistente", column_proc="nome_procedimento", top=21):
    # Passo 1: filtra registros com "PARECER"
    filtrado = df[df[column_info].str.contains("PARECER", case=False, na=False)].copy()
    
    # Passo 2: cria coluna de contagem de "PARECER" por linha
    filtrado["qtd_parecer_linha"] = (
        filtrado[column_info].str.upper().str.count("PARECER") +
        filtrado[column_info].str.upper().str.count("NOTIFICO")
    )
    
    # Passo 2.1: ignora linhas sem nenhum "PARECER"
    filtrado = filtrado[filtrado["qtd_parecer_linha"] > 0]
    
    # Passo 3: junta todas as palavras dos procedimentos
    todas_palavras = []
    for proc in filtrado[column_proc].dropna():
        todas_palavras.extend(proc.split())
    
    # Passo 4: pega top 20 palavras
    contagem = Counter(todas_palavras)
    top_20_palavras = [w for w, c in contagem.most_common(top)]
    
    # Passo 5: para cada palavra do top 20, calcula média de qtd_parecer_linha
    result = []
    for palavra in top_20_palavras:
        temp = filtrado[filtrado[column_proc].str.contains(palavra, case=False, na=False)]
        mean_parecer = temp["qtd_parecer_linha"].mean()
        result.append((palavra, mean_parecer))
    
    # Passo 6: retorna DataFrame final, arredondando média para 2 casas
    df_result = pd.DataFrame(result, columns=["Procedimentos", "Quantidade"])
    df_result["Quantidade"] = df_result["Quantidade"].round(2)

    df_result = df_result.sort_values(by="Quantidade", ascending=False).reset_index(drop=True)
    
    return df_result

def quantidade_assinaturas(df):
    palavras = ["RODRIGO", "JOYCE", "KEISI"]
    pattern = "|".join(palavras)
    matches = df["info_assistente"].str.findall(pattern, re.IGNORECASE)
    exploded = matches.explode()
    contagem = exploded.value_counts().reset_index()
    contagem.columns = ["Assinaturas", "Quantidade"]

    return contagem
    
def quantidade_assinatura_processo(df):
    pattern = r"(\d{1,2}/\d{1,2}).*?(COBRO|PARECER SOLICITADO|FEITO CTT|CTT REALIZADO|EM ANEXO).*?(RODRIGO|JOYCE|KEISI)"

    # Usa extractall em vez de extract -> captura TODAS as ocorrências
    extraido = df["info_assistente"].str.extractall(pattern, flags=re.IGNORECASE)
    extraido = extraido.reset_index(drop=True)  # remove o multi-index (opcional)
    extraido.columns = ["Data", "Acao", "Assinaturas"]

    if extraido.empty:
        print("Nenhum padrão encontrado. Verifique os textos da coluna.")

    # Normaliza ação
    extraido["Acao"] = extraido["Acao"].replace({"CTT REALIZADO": "FEITO CTT"})

    # Conta todas as combinações
    ranking = (
        extraido.groupby(["Assinaturas", "Acao"])
        .size()
        .reset_index(name="Quantidade")
    )

    # Ordena para ficar legível
    ranking = ranking.sort_values(by=["Assinaturas", "Quantidade"], ascending=[True, False])

    return extraido, ranking

def procedimentos_mais_pedido_by_assinatura(df, column_info="info_assistente", column_proc="nome_procedimento", word="PARECER SOLICITADO"):
    # Filtra apenas linhas que contem a palavra desejada
    df_filtered = df[df[column_info].str.contains(word, case=False, na=False)].copy()

    # Aplica regex na coluna info_assistente
    pattern = r"(\d{1,2}/\d{1,2}).*?(COBRO|PARECER SOLICITADO|FEITO CTT|CTT REALIZADO).*?(RODRIGO|JOYCE|KEISI)"
    extracted = df_filtered[column_info].str.extract(pattern, expand=True, flags=re.IGNORECASE)
    extracted.columns = ["Data", "Acao", "Assinaturas"]

    # Agora pegamos o procedimento correspondente apenas das linhas filtradas
    extracted["nome_procedimento"] = df_filtered[column_proc].replace("", None)
    extracted = extracted.dropna(subset=["nome_procedimento"])
    

    # Agrupa por assinatura e procedimento
    contagem = extracted.groupby(["Assinaturas", "nome_procedimento"]).size().reset_index(name="Quantidade")
    contagem = contagem.sort_values(by="Quantidade", ascending=False)

    return contagem.head(20)

def procedimentos_mais_tempo_resolver_parecer(df, coluna_info="info_assistente"):
    palavra_parecer = "PARECER SOLICITADO"
    palavra_cobro = "COBRO"

    df = df[df[coluna_info].str.contains(palavra_parecer, case=False, na=False)]
    df = df[df[coluna_info].str.contains(palavra_cobro, case=False, na=False)]

    df["quantidade_cobro"] = df[coluna_info].str.count(palavra_cobro)
    df["quantidade_cobro"] = df["quantidade_cobro"] + 1
    df["nome_procedimento"] = df["nome_procedimento"].str.strip()
    df["nome_procedimento"] = df["nome_procedimento"].replace("", None)
    df = df.groupby("nome_procedimento")["quantidade_cobro"].mean().reset_index()

    df = df.sort_values(by="quantidade_cobro", ascending=False)

    # 20 linhas com mais "COBRO"
    #top_20 = df.nlargest(20, "qtd_cobro")

    # 20 linhas com menos "COBRO"
    #bottom_20 = df.nsmallest(20, "qtd_cobro")

    return df

def procedimentos_mais_tempo_resolver_cobro(df, coluna_info="info_assistente"):
    palavracobro = "COBRO"

    df = df[df[coluna_info].str.contains(palavracobro,case=False, na=False)].copy()
    df["quantidade_cobro"] = df[coluna_info].str.count(palavracobro)
    df["quantidade_cobro"] = df["quantidade_cobro"] + 1
    df["nome_procedimento"] = df["nome_procedimento"].str.strip()

    df = df.groupby("nome_procedimento")["quantidade_cobro"].mean().reset_index()

    df = df.sort_values(by="quantidade_cobro", ascending=False)

    return df

def procedimentos_mais_tempo_resolver_cobro_min_5(df, coluna_info="info_assistente"):
    palavracobro = "COBRO"

    df = df.copy()

    # Filtra somente linhas que contenham "COBRO"
    df = df[df[coluna_info].str.contains(palavracobro, case=False, na=False)]

    # Conta ocorrências e soma +1
    df["quantidade_cobro"] = df[coluna_info].str.count(palavracobro) + 1
    df["nome_procedimento"] = df["nome_procedimento"].str.strip()
    df = df[df["nome_procedimento"] != ""]
    df = df[df["nome_procedimento"].str.lower() != "nan"]

    contagem = df["nome_procedimento"].value_counts()

    # mantém só quem aparece pelo menos 5 vezes
    procedimentos_validos = contagem[contagem >= 5].index
    df = df[df["nome_procedimento"].isin(procedimentos_validos)]

    df_final = (
        df.groupby("nome_procedimento")
          .agg(
              quantidade_cobro=("quantidade_cobro", "mean"),
              total_procedimentos=("nome_procedimento", "count")
          )
          .reset_index()
    )

    # ordena pela média de cobro
    df_final = df_final.sort_values(by="quantidade_cobro", ascending=False)

    return df_final

def top_medicos(df, column="medico_solicitante", top=21):

    df[column] = df[column].str.strip().str.upper()
    counts = df[column].value_counts().head(top)
    df_top = counts.reset_index()
    df_top.columns = ["medico_solicitante", "quantidade"]

    return df_top

def filter_cancelar(df,column_info="info_assistente", column_info_medico="info_medico"):
    
    coluna_info_medico = ["ACEITA CANCELAR", "DESEJA CANCELAMENTO", "CANCELARIAMOS", "SUGERIR QUE", "DESEJO DO CANCELAMENTO", "CTT GRAVADO"]
    
    coluna_info = ["ACEITA CANCELAMENTO MEDIANTE", "DESEJA CANCELAMENTO", "DESEJA CANCELAR", "ACEITA CANCELAMENTO DA SOLICITAÇÃO ATUAL", "ACEITA CANCELAMENTO DA SOLICITACAO ATUAL", "ACEITA CANCELAMENTO DA SOLICITACÃO ATUAL", "ACEITA CANCELAMENTO DESSE PROCEDIMENTO"]

    pattern_info_medico = "|".join(coluna_info_medico)
    pattern_info = "|".join(coluna_info)

    filtro_coluna_info = df[column_info].str.contains(pattern_info, case=False, na=False)
    filtro_coluna_info_medico = df[column_info_medico].str.contains(pattern_info_medico, case=False, na=False)

    df_cancelar = df[filtro_coluna_info | filtro_coluna_info_medico]

    return df_cancelar

def _ensure_date_series(s):
    """Converte para datetime com suporte a dd/mm/yyyy HH:MM e ISO. Retorna somente a data."""
    return pd.to_datetime(s, dayfirst=True, errors="coerce").dt.date

import pandas as pd

def reconstruir_info(df, col_nome="nome", col_proc="procedimento", col_data="data_hora_bot", col_info="info_medico"):
    # garantir que a data esteja em formato datetime
    df[col_data] = pd.to_datetime(df[col_data], errors="coerce")

    resultados = []

    # agrupa por paciente + procedimento
    for (nome, proc), grupo in df.groupby([col_nome, col_proc]):
        grupo = grupo.sort_values(col_data).copy()

        historico = []  # vai guardar todas as infos já vistas

        for _, row in grupo.iterrows():
            partes = [p.strip() for p in row[col_info].split("-")]
            for parte in partes:
                if parte not in historico:  # só adiciona se for novo
                    historico.append(parte)

        # pega a última linha do grupo
        ultima = grupo.iloc[-1].copy()
        # substitui info_medico pelo histórico completo
        ultima[col_info] = " - ".join(historico)

        resultados.append(ultima)

    # retorna dataframe consolidado
    return pd.DataFrame(resultados)


# exemplo de uso:



