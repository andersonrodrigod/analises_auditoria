from collections import Counter
import pandas as pd
import re

def top_words(df, column="nome_procedimento", top=20):

    # Junta todo o texto da coluna e separa em palavras
    all_text = " ".join(df[column].dropna())
    
    # Conta as ocorrências
    counts = Counter(all_text.split())
    
    # Pega o top N
    top_list = counts.most_common(top)
    
    # Cria DataFrame
    df_top = pd.DataFrame(top_list, columns=["word", "count"])
     
    return df_top

def top_medicos(df, column="medico_solicitante", top=21):

    counts = df[column].value_counts().head(top)
    df_top = counts.reset_index()
    df_top.columns = ["medico_solicitante", "quantidade"]

    return df_top

def filter_names(df, words, column="info_assistente"):
    pattern = "|".join(words)
    df["matches"] = df[column].str.findall(pattern, re.IGNORECASE)

    exploded = df["matches"].explode()
    counts = exploded.value_counts().reset_index()
    counts.columns = ["word", "count"]

    return counts
    
def filter_by_word(df, word, column="nome_procedimento"):
    return df[df[column].str.contains(word, case=False, na=False)]

def counter_words(df, column_info="info_assistente", column="nome_procedimento", word="PARECER", top=21, add_value=False):
    # Filtra apenas os registros com "PARECER"
    filtered = df[df[column_info].str.contains(word, case=False, na=False)]

    # Junta todos os procedimentos em uma lista de palavras
    all_text = []

    for proc in filtered[column].dropna():
        word = proc.split() # quebra em palavras
        all_text.extend(word) # adiciona na lista geral

    # Conta as palavras
    counts = Counter(all_text)
    if add_value:
        for k in counts:
            counts[k] *= 2  # Adiciona o dobro do valor

    top_words = counts.most_common(top)
    df_top = pd.DataFrame(top_words, columns=['word', 'count'])

    return df_top

def top20_mean_parecer(df, column_info="info_assistente", column_proc="nome_procedimento", top=21):
    # Passo 1: filtra registros com "PARECER"
    filtered = df[df[column_info].str.contains("PARECER", case=False, na=False)].copy()
    
    # Passo 2: cria coluna de contagem de "PARECER" por linha
    filtered["qtd_parecer_linha"] = filtered[column_info].str.upper().str.count("PARECER")
    
    # Passo 2.1: ignora linhas sem nenhum "PARECER"
    filtered = filtered[filtered["qtd_parecer_linha"] > 1]
    
    # Passo 3: junta todas as palavras dos procedimentos
    all_words = []
    for proc in filtered[column_proc].dropna():
        all_words.extend(proc.split())
    
    # Passo 4: pega top 20 palavras
    counts = Counter(all_words)
    top20_words = [w for w, c in counts.most_common(top)]
    
    # Passo 5: para cada palavra do top 20, calcula média de qtd_parecer_linha
    result = []
    for word in top20_words:
        temp = filtered[filtered[column_proc].str.contains(word, case=False, na=False)]
        mean_parecer = temp["qtd_parecer_linha"].mean()
        result.append((word, mean_parecer))
    
    # Passo 6: retorna DataFrame final, arredondando média para 2 casas
    df_result = pd.DataFrame(result, columns=["word", "count"])
    df_result["count"] = df_result["count"].round(2)
    
    return df_result

def extrair_padroes(df, column="info_assistente"):
    # Define o padrão que será buscado nos textos da coluna:
    # (\d{1,2}/\d{1,2}) -> captura datas no formato DD/MM ou D/M
    # .*? -> qualquer texto intermediário, não ganancioso
    # (COBRO|PARECER SOLICITADO|FEITO CTT|CTT REALIZADO|EM ANEXO) -> captura as ações específicas
    # (RODRIGO|JOYCE|KEISI) -> captura a assinatura
    pattern = r"(\d{1,2}/\d{1,2}).*?(COBRO|PARECER SOLICITADO|FEITO CTT|CTT REALIZADO|EM ANEXO).*?(RODRIGO|JOYCE|KEISI)"

    # Aplica o regex na coluna desejada e cria um DataFrame temporário com 3 colunas
    extracted = df[column].str.extract(pattern, expand=True, flags=re.IGNORECASE)
    extracted.columns = ["data", "acao", "assinatura"]

    
    # Se não encontrar nenhum padrão, avisa
    if extracted.empty:
        print("Nenhum padrão encontrado. Verifique os textos da coluna.")

    # Remove linhas que ficaram com algum valor NaN após a extração
    extracted = extracted.dropna()

    # Agrupa por assinatura e ação, contando quantas vezes cada combinação aparece
    # size() -> retorna a contagem de linhas em cada grupo
    # reset_index(name="quantidade") -> transforma o índice múltiplo em colunas normais
    ranking = extracted.groupby(["assinatura", "acao"]).size().reset_index(name="quantidade")

    # Ordena o ranking por assinatura (alfabética) e quantidade (maior para menor)
    ranking = ranking.sort_values(by=["assinatura", "quantidade"], ascending=[True, False])

    # Retorna o DataFrame detalhado (cada ocorrência extraída) e o ranking resumido por assinatura e ação
    return extracted, ranking

def procedimentos_mais_pedido_by_assinatura(df, column_info="info_assistente", column_proc="nome_procedimento", word="PARECER SOLICITADO"):
    # Filtra apenas linhas que contem a palavra desejada
    df_filtered = df[df[column_info].str.contains(word, case=False, na=False)].copy()

    # Aplica regex na coluna info_assistente
    pattern = r"(\d{1,2}/\d{1,2}).*?(COBRO|PARECER SOLICITADO|FEITO CTT|CTT REALIZADO).*?(RODRIGO|JOYCE|KEISI)"
    extracted = df_filtered[column_info].str.extract(pattern, expand=True, flags=re.IGNORECASE)
    extracted.columns = ["data", "acao", "assinatura"]

    # Agora pegamos o procedimento correspondente apenas das linhas filtradas
    extracted["nome_procedimento"] = df_filtered[column_proc]

    # Agrupa por assinatura e procedimento
    contagem = extracted.groupby(["assinatura", "nome_procedimento"]).size().reset_index(name="quantidade")
    contagem = contagem.sort_values(by=["assinatura", "quantidade"], ascending=[True, False])

    return contagem



