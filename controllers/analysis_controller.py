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
    return df_final.sort_values(by=f"Quantidade_{palavra}", ascending=False).reset_index(drop=True).head(60)

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


def reconstruir_info(df, col_nome="nome", col_proc="nome_procedimento", col_data="data_hora_bot", col_info="info_medico"):
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


def filtrar_multiplos_anexar(df, col_nome="nome", col_proc="nome_procedimento", col_info="info_medico"):
    resultados = []

    # ignorar os registros cujo procedimento é "A_DEFINIR"
    df_filtrado = df[df[col_proc].str.upper() != "PROCEDIMENTO A DEFINIR ADMINISTRATIVAMENTE"].copy()

    for (nome, proc), grupo in df_filtrado.groupby([col_nome, col_proc]):
        texto = " ".join(grupo[col_info].astype(str))

        # pega só as partes que têm "ANEXAR" mas não "GUIA"
        partes_anexar = [p for p in texto.split("-") 
                         if "ANEXAR" in p.upper() and "GUIA" not in p.upper()]

        # extrai datas (formato dd/mm) dessas partes
        datas = set()
        for parte in partes_anexar:
            match = re.search(r"\b\d{2}/\d{2}\b", parte)
            if match:
                datas.add(match.group())

        # se tiver 2 ou mais datas diferentes com ANEXAR, guarda
        if len(datas) >= 2:
            resultados.append({
                "nome": nome,
                "nome_procedimento": proc
            })

    return pd.DataFrame(resultados)


def filtrar_anexar_parecer(df, col_nome="nome", col_proc="nome_procedimento", col_info="info_medico"):
    resultados = []

    df_filtrado = df[df[col_proc].str.upper() != "PROCEDIMENTO A DEFINIR ADMINISTRATIVAMENTE"].copy()

    for (nome, proc), grupo in df_filtrado.groupby([col_nome, col_proc]):
        texto = " ".join(grupo[col_info].astype(str)).upper()

        partes_anexar = [p for p in texto.split("-") if "ANEXAR" in p and "GUIA" not in p]
        partes_parecer = [p for p in texto.split("-") if "PARECER" in p]

        datas_anexar = set(re.findall(r"\b\d{2}/\d{2}\b", " ".join(partes_anexar)))
        datas_parecer = set(re.findall(r"\b\d{2}/\d{2}\b", " ".join(partes_parecer)))

        if datas_anexar and datas_parecer:
            resultados.append({
                "nome": nome,
                "nome_procedimento": proc
            })

    df_result = pd.DataFrame(resultados)

    # Remove completamente linhas vazias ou só espaços
    df_result["nome_procedimento"] = df_result["nome_procedimento"].astype(str).str.strip()
    df_result = df_result[df_result["nome_procedimento"] != ""]
    

    # Ordenar do mais frequente para o menos frequente
    df_result = df_result.groupby(["nome", "nome_procedimento"]).size().reset_index(name="quantidade")
    df_result = df_result.sort_values(by="quantidade", ascending=False).reset_index(drop=True)

    return df_result

def resumo_procedimentos(df, coluna_proc="nome_procedimento", coluna_info="info_medico", palavra_parecer="PARECER", top=20):
    """
    Retorna um DataFrame com:
    - Quantidade total de cada procedimento
    - Quantidade de procedimentos com 'PARECER'
    """

    # Limpa procedimentos vazios ou só espaços
    df_proc = df.copy()
    df_proc[coluna_proc] = df_proc[coluna_proc].astype(str).str.strip()
    df_proc = df_proc[df_proc[coluna_proc] != ""]

    # Contagem total de procedimentos
    total_proc = Counter(df_proc[coluna_proc])

    # Contagem de procedimentos que contêm a palavra "PARECER"
    df_parecer = df_proc[df_proc[coluna_info].str.contains(palavra_parecer, case=False, na=False)]
    parecer_proc = Counter(df_parecer[coluna_proc])

    # Monta lista final
    dados = []
    for proc, qtd_total in total_proc.items():
        qtd_parecer = parecer_proc.get(proc, 0)
        dados.append([proc, qtd_total, qtd_parecer])

    # Cria DataFrame
    df_final = pd.DataFrame(dados, columns=["Procedimento", "Quantidade_Total", f"Quantidade_{palavra_parecer}"])

    # Ordena pelo mais frequente de PARECER primeiro
    df_final = df_final.sort_values(by=f"Quantidade_{palavra_parecer}", ascending=False).reset_index(drop=True)

    return df_final.head(top)

def filtrar_multiplos_acoes(df, col_nome="nome", col_proc="nome_procedimento", col_info="info_medico"):
    """
    Filtra registros em que aparecem múltiplas datas em ações específicas
    como ANEXAR, REALIZOU, CHECAR, VERIFICAR, TROCAR.
    """
    resultados = []

    # Ignorar registros cujo procedimento é "A_DEFINIR"
    df_filtrado = df[df[col_proc].str.upper() != "PROCEDIMENTO A DEFINIR ADMINISTRATIVAMENTE"].copy()

    acoes = ["ANEXAR", "REALIZOU", "CHECAR", "VERIFICAR", "TROCAR", "PARECER"]

    for (nome, proc), grupo in df_filtrado.groupby([col_nome, col_proc]):
        texto = " ".join(grupo[col_info].astype(str)).upper()

        for acao in acoes:
            # pega partes que têm a ação e não "GUIA" (apenas para ANEXAR)
            if acao == "ANEXAR":
                partes = [p for p in texto.split("-") if acao in p and "GUIA" not in p]
            else:
                partes = [p for p in texto.split("-") if acao in p]

            # extrai datas (dd/mm) dessas partes
            datas = set(re.findall(r"\b\d{2}/\d{2}\b", " ".join(partes)))

            if len(datas) >= 2:
                resultados.append({
                    "nome": nome,
                    "nome_procedimento": proc,
                    "acao": acao,
                    "datas": sorted(datas)
                })

    return pd.DataFrame(resultados)




# exemplo de uso:



