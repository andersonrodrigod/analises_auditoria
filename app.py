from models.procedures_model import load_excel
from utils.text_cleaner import clean_text, normalize_words 
from controllers.analysis_controller import top_procedimentos, filter_by_word, procedimentos_quantidade_total_palavra, procedimento_media_dias_resolver_parecer, quantidade_assinaturas, quantidade_assinatura_processo, procedimentos_mais_pedido_by_assinatura,procedimentos_mais_tempo_resolver_parecer, procedimentos_mais_tempo_resolver_cobro, procedimentos_mais_tempo_resolver_cobro_min_5, top_medicos, filter_cancelar, reconstruir_info, filtrar_multiplos_anexar, filtrar_anexar_parecer, resumo_procedimentos, filtrar_multiplos_acoes
from graphs.bar_plot import bar_plot_procedimentos_maior_quantidade, bar_plot_top_quantidade_parecer, bar_plot_top_quantidade_cobro, bar_plot_procedimento_media_dias_resolver_parecer, bar_plot_assinaturas, bar_plot_assinaturas_processos, bar_plot_assinaturas_processos_parecer, stacked_plot_assinaturas_processos_parecer, heatmap_plot_assinaturas_processos_parecer, bar_plot_procedimento_media_dias_cobrar_resolver_parecer, bar_plot_procedimento_media_dias_cobrar_resolver_exames, bar_plot_procedimento_media_dias_cobrar_resolver_exames_min5, plot_procedimentos_usuario, plot_quantidade_procedimentos, stacked_bar_procedimentos
import pandas as pd

#pd.set_option("display.max_rows", None)

df = load_excel("historico_consolidado.xlsx")
df = df.sort_values(by="data_hora_bot")

df_resultado = reconstruir_info(df, col_proc="nome_procedimento", col_data="data_hora_bot", col_info="info_medico")
#df_resultado = filtrar_multiplos_anexar(df_resultado, col_nome="nome", col_proc="nome_procedimento", col_info="info_medico")
#df_resultado = filtrar_anexar_parecer(df_resultado, col_nome="nome", col_proc="nome_procedimento", col_info="info_medico")
#df_resultado = filtrar_multiplos_acoes(df_resultado, col_nome="nome", col_proc="nome_procedimento", col_info="info_medico")

#print(df_resultado)

#df_resultado["nome_procedimento"] = df_resultado["nome_procedimento"].apply(clean_text)
#df_resultado = normalize_words(df_resultado, column="nome_procedimento")

#bar_plot_procedimentos_usuario = plot_procedimentos_usuario(df_resultado)
#bar_plot_plot_quantidade_procedimentos = plot_quantidade_procedimentos(df_resultado)


#print("Total de procedimentos:", total_procedimentos)
#print(quantidade_por_proc)


#print(df_resultado.tail(50))

#df_resultado.to_excel("historico_consolidado.xlsx", index=False)


df = df.drop_duplicates(subset=["nome", "nome_procedimento"], keep="last")
print("Linhas após remover duplicados:", len(df))


df["nome_procedimento"] = df["nome_procedimento"].apply(clean_text)
df = normalize_words(df, column="nome_procedimento")

#df_resumo = resumo_procedimentos(df, palavra_parecer="PARECER", top=50)
#plot_stacked_bar_procedimentos = stacked_bar_procedimentos(df_resumo)

#print(df_resumo)

df_top_procedimentos = top_procedimentos(df, top=40)

df_top_parecer = procedimentos_quantidade_total_palavra(df, palavra="PARECER")
df_top_cobro = procedimentos_quantidade_total_palavra(df, palavra="COBRO")

df_procedimento_media_dias_resolver_parecer = procedimento_media_dias_resolver_parecer(df, column_info="info_assistente", column_proc="nome_procedimento")


df_top_assinaturas = quantidade_assinaturas(df)

#df_top_info_assistente = top_palavras(df, coluna="info_assistente", top=50)

extraidos, ranking = quantidade_assinatura_processo(df)



df_procedimentos_mais_pedidos_parecer_por_assinatura = procedimentos_mais_pedido_by_assinatura(df, column_info="info_assistente", column_proc="nome_procedimento", word="PARECER SOLICITADO")

df_procedimentos_mais_tempo_resolver_parecer = procedimentos_mais_tempo_resolver_parecer(df, coluna_info="info_assistente")

df_procedimentos_mais_tempo_resolver_cobro = procedimentos_mais_tempo_resolver_cobro(df, coluna_info="info_assistente")

df_procedimentos_mais_tempo_resolver_cobro_min5 = procedimentos_mais_tempo_resolver_cobro_min_5(df, coluna_info="info_assistente")

df_top_medicos = top_medicos(df, column="medico_solicitante", top=21)

df_cancelar = filter_cancelar(df, column_info="info_assistente", column_info_medico="info_medico")

#print(df_cancelar)
#print(df_top_info_assistente)
#print(extraidos)
#print(df_top_medicos)


# --------------------------------------------------
#print(df_top_procedimentos)
#bar_plot_top_procedimentos = bar_plot_procedimentos_maior_quantidade(df_top_procedimentos)

print(df_top_parecer)
#print(df_top_cobro)
bar_plot_top_parecer = bar_plot_top_quantidade_parecer(df_top_parecer)
#bar_plot_top_cobro = bar_plot_top_quantidade_cobro(df_top_cobro)

#print(df_procedimento_media_dias_resolver_parecer)
#bar_plot_top_procedimento_media_dias_resolver_parecer = bar_plot_procedimento_media_dias_resolver_parecer(df_procedimento_media_dias_resolver_parecer)

#print(df_top_assinaturas)
#bar_plot_top_assinatuyras = bar_plot_assinaturas(df_top_assinaturas)

#print(ranking)
#ranking_assinaturas_processos = bar_plot_assinaturas_processos(ranking)

#print(df_procedimentos_mais_pedidos_parecer_por_assinatura)
#bar_plot_top_assinaturas_processos_parecer = bar_plot_assinaturas_processos_parecer(df_procedimentos_mais_pedidos_parecer_por_assinatura)
#stacked_plot_top_assinaturas_procesos_parecer = stacked_plot_assinaturas_processos_parecer(df_procedimentos_mais_pedidos_parecer_por_assinatura)
#heatmap_plot_top_assinaturas_procesos_parecer = heatmap_plot_assinaturas_processos_parecer(df_procedimentos_mais_pedidos_parecer_por_assinatura)

#print(df_procedimentos_mais_tempo_resolver_parecer)
#bar_plot_top_procedimento_media_dias_cobrar_resolver_parecer = bar_plot_procedimento_media_dias_cobrar_resolver_parecer(df_procedimentos_mais_tempo_resolver_parecer.head(20))

#print(df_procedimentos_mais_tempo_resolver_cobro)
#bar_plot_top_procedimentos_mais_tempo_resolver_exames_cobro = bar_plot_procedimento_media_dias_cobrar_resolver_exames(df_procedimentos_mais_tempo_resolver_cobro.head(20))

#print(df_procedimentos_mais_tempo_resolver_cobro_min5)
#bar_blot_top_procedimentos_mais_tempo_resolver_cobro_min5 = bar_plot_procedimento_media_dias_cobrar_resolver_exames_min5(df_procedimentos_mais_tempo_resolver_cobro_min5.head(20))

#cateter = filter_by_word(df, "TRANSEPTAL")

#print("\nProcedimentos com PUNCAO: ", cateter["nome_procedimento"].unique())









