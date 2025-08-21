from models.procedures_model import load_excel
from utils.text_cleaner import clean_text, normalize_words
from controllers.analysis_controller import top_words, filter_by_word, counter_words, top20_mean_parecer, filter_names, extrair_padroes, procedimentos_mais_pedido_by_assinatura, top_medicos
from graphs.bar_plot import procedimentos_bar_plot
import pandas as pd

pd.set_option("display.max_rows", None)

df = load_excel("dados.xlsx")
df = df.sort_values(by="data_hora_bot")


df = df.drop_duplicates(subset=["nome", "nome_procedimento"], keep="last")


df["nome_procedimento"] = df["nome_procedimento"].apply(clean_text)
df = normalize_words(df, column="nome_procedimento")


df_top_procedimentos = top_words(df, column="nome_procedimento", top=21)
df_top_info_assistente = top_words(df, column="info_assistente", top=50)

df_top_parecer = counter_words(df, column_info="info_assistente", column="nome_procedimento", word="PARECER")
df_top_cobro = counter_words(df, column_info="info_assistente", column="nome_procedimento", word="COBRO", add_value=True)

df_top_parecer_most_time = top20_mean_parecer(df, column_info="info_assistente", column_proc="nome_procedimento")

pattern = ["RODRIGO", "JOYCE", "KEISI"]
df_top_names = filter_names(df, pattern, column="info_assistente")

extraidos, ranking = extrair_padroes(df, column="info_assistente")

df_parecer_mais_pedidos = procedimentos_mais_pedido_by_assinatura(df, column_info="info_assistente", column_proc="nome_procedimento", word="PARECER SOLICITADO")

df_top_medicos = top_medicos(df, column="medico_solicitante", top=21)

#print(df_top_procedimentos)
#print(df_top_parecer_most_time)
#print(df_top_parecer)
#print(df_top_cobro)
#print(df_top_info_assistente)
#print(df_parecer_mais_pedidos.head(200))

#print("\nRanking de maiores assinaturas:")
#print(df_top_names)
#print("\nRanking por assinatura e ação:")
#print(ranking)

#print(df_top_medicos)



cateter = filter_by_word(df, "PROCED")

print("\nProcedimentos com PUNCAO: ", cateter["nome_procedimento"].unique())

#bar_plot_top_procedimentos = procedimentos_bar_plot(top_procedimentos)












