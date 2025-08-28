import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os
from datetime import datetime

palette_custom = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
    "#aec7e8", "#ffbb78", "#98df8a", "#ff9896", "#c5b0d5",
    "#c49c94", "#f7b6d2", "#c7c7c7", "#dbdb8d", "#9edae5"
    ]


def edit_bar_plot(ax, title=None, xlabel=None, ylabel=None, ylim=None, tight_layout=True, despine=True, xticks=True, offset=0, grid=None):
    if title:
        ax.set_title(title, fontsize=14, weight="bold")
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=12, weight="bold", labelpad=15)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=12, weight="bold", labelpad=15)
    if ylim:
        ax.set_ylim(ylim)
    if despine:
        sns.despine(ax=ax)
    if tight_layout:
        plt.tight_layout()
    if grid:
        ax.set_axisbelow(True)
        ax.grid(axis="y", linestyle="--", alpha=0.7)
    
    for p in ax.patches:
        height = p.get_height()
        if height == 0:
            continue
        width = p.get_width()
        x = p.get_x() + width / 2
        y = height + offset
        text = f"{height:.1f}" if height % 1 else f"{int(height)}"
        ax.text(x, y, text, ha="center", va="bottom", fontsize=10, fontweight="bold", color="white",
        bbox=dict(facecolor='gray', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.1'))


def bar_plot_procedimentos_maior_quantidade(df, salvar=True):
    plt.figure(figsize=(12, 6))
    
    x="Procedimentos"
    y="Quantidade"
    title="Procedimentos Mais Frequentes"

    ax = sns.barplot(data=df, x=x, y=y, palette=palette_custom, hue=x, errorbar=None)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")

    ax = edit_bar_plot(ax, title=title, xlabel=x, ylabel=y, ylim=(0, max(df[y]) * 1.3), xticks=True, offset=2, grid=True)
    plt.subplots_adjust(bottom=0.30)
    

    if salvar:
        os.makedirs("figures", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        caminho = f"figures/bar_procedimentos_maior_quantidade_{timestamp}.png"
        plt.savefig(caminho, dpi=300, bbox_inches='tight')
        print(f"Gráfico salvo em: {caminho}")

    plt.show()
    return ax

def bar_plot_top_quantidade_parecer(df, salvar=True):
    plt.figure(figsize=(len(df) * 0.6, 6)) 

    x = "Procedimentos"
    y = "Quantidade_PARECER"
    title = "Procedimentos Mais Frequentes (em Parecer)"

    ax = sns.barplot(data=df, x=x, y=y, palette=palette_custom, hue=x, errorbar=None)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")

    ax = edit_bar_plot(ax, title=title, xlabel=x, ylabel="Quantidade", ylim=(0, max(df[y]) * 1.3), xticks=True, offset=0.7, grid=True)
    plt.subplots_adjust(bottom=0.25)

    if salvar:
        os.makedirs("figures", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        caminho = f"figures/bar_procedimentos_maior_quantidade_{timestamp}.png"
        plt.savefig(caminho, dpi=300, bbox_inches='tight')
        print(f"Gráfico salvo em: {caminho}")

    plt.show()

    plt.show()
    return ax

def bar_plot_top_quantidade_cobro(df):
    plt.figure(figsize=(12, 6))

    x = "Procedimentos"
    y = "Quantidade_COBRO"
    title = "Procedimentos Mais Frequentes (em Cobranças)"

    ax = sns.barplot(data=df, x=x, y=y, palette=palette_custom, hue=x, errorbar=None)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")

    ax = edit_bar_plot(ax, title=title, xlabel=x, ylabel="Quantidade", ylim=(0, max(df[y]) * 1.3), xticks=True, offset=0.7)
    plt.subplots_adjust(bottom=0.25)
    plt.show()
    return ax

def bar_plot_procedimento_media_dias_resolver_parecer(df):
    plt.figure(figsize=(12, 6))

    x = "Procedimentos"
    y = "Quantidade"
    title = "Média de Dias Para Resolução do Parecer (por Procedimento)"

    ax = sns.barplot(data=df, x=x, y=y, palette=palette_custom, hue=x, errorbar=None)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")

    ax = edit_bar_plot(ax, title=title, xlabel=x, ylabel="Média", ylim=(0, max(df[y]) * 1.3), xticks=True, offset=0.1)
    plt.subplots_adjust(bottom=0.25)
    plt.show()
    return ax

def bar_plot_assinaturas(df):
    plt.figure(figsize=(12, 6))

    x = "Assinaturas"
    y = "Quantidade"
    title = "Quantidade de Assinatura (por Operador)"

    ax = sns.barplot(data=df, x=x, y=y, palette=palette_custom, hue=x, errorbar=None)
    
    ax.set_xticklabels(ax.get_xticklabels(),  ha="right")

    ax = edit_bar_plot(ax, title=title, xlabel=x, ylabel=y, ylim=(0, max(df[y]) * 1.3), xticks=True, offset=50)
    plt.subplots_adjust(bottom=0.25)
    plt.show()
    return ax

def bar_plot_assinaturas_processos(df):
    plt.figure(figsize=(12, 6))


    x = "Assinaturas"
    y = "Quantidade"
    title = "Quantidade de Assinatura de Ação (por Operador)"


    ax = sns.barplot(data=df, x=x, y=y, palette=palette_custom, hue="Acao", errorbar=None)
    ax.set_xticklabels(ax.get_xticklabels(),  ha="right")
    ax.legend(title="Ação", loc='upper left', bbox_to_anchor=(1.01, 1), borderaxespad=0)
    
    ax = edit_bar_plot(ax, title=title, xlabel="Assinaturas", ylabel="Quantidade", ylim=(0, max(df[y]) * 1.3), offset=50)
    plt.subplots_adjust(bottom=0.25)
    plt.show()
    return ax

def bar_plot_assinaturas_processos_parecer(df):
    plt.figure(figsize=(12, 6))

    x = "nome_procedimento"
    y = "Quantidade"
    title = "Ranking de Solicitações de Parecer (por Procedimento)"

    ax = sns.barplot(data=df, x=x, y=y, palette=palette_custom, hue="Assinaturas", errorbar=None)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45,  ha="right")

    ax.legend(title="Operadores", loc='upper left', bbox_to_anchor=(1.01, 1), borderaxespad=0)
    
    ax = edit_bar_plot(ax, title=title, xlabel="Assinaturas", ylabel="Quantidade", ylim=(0, max(df[y]) * 1.3), offset=0.2)
    plt.subplots_adjust(bottom=0.25)
    plt.show()
    return ax

def stacked_plot_assinaturas_processos_parecer(df):
    pivot_df = df.pivot_table(index="nome_procedimento",columns="Assinaturas", values="Quantidade", aggfunc="sum", fill_value=0)                      
                          
    pivot_df.plot(kind="bar", stacked=True, figsize=(10,6))
    plt.xticks(rotation=45, ha="right")
    plt.title("Procedimentos por Assinatura (empilhado)", fontsize=14, weight="bold")
    plt.ylabel("Quantidade", fontsize=12, weight="bold")
    plt.xlabel("Procedimentos", fontsize=12, weight="bold")
    plt.tight_layout()
    plt.show()

def heatmap_plot_assinaturas_processos_parecer(df):

    pivot_df = df.pivot_table(index="nome_procedimento", columns="Assinaturas", values="Quantidade", aggfunc="sum",fill_value=0)
                                        
    plt.figure(figsize=(10,6))
    sns.heatmap(pivot_df, annot=True, fmt="d", cmap="Blues")
    plt.title("Distribuição de Procedimentos (por Assinatura)", fontsize=14, weight="bold")
    plt.ylabel("Procedimento", fontsize=12, weight="bold")
    plt.xlabel("Assinatura", fontsize=12, weight="bold")
    plt.show()

def bar_plot_procedimento_media_dias_cobrar_resolver_parecer(df):
    plt.figure(figsize=(12, 6))

    x = "nome_procedimento"
    y = "quantidade_cobro"
    title = "Frequência Média de Cobrança por Procedimento (Antes do Parecer)"

    ax = sns.barplot(data=df, x=x, y=y, palette=palette_custom, hue=x, errorbar=None)
    ticks = range(len(df[x]))
    ax.set_xticks(ticks)
    ax.set_xticklabels(df[x], rotation=45, ha="right")

    ax = edit_bar_plot(ax, title=title, xlabel="Procedimentos", ylabel="Média", ylim=(0, max(df[y]) * 1.3), xticks=True, offset=0.1)
    plt.subplots_adjust(bottom=0.25)
    plt.show()
    return ax

def bar_plot_procedimento_media_dias_cobrar_resolver_exames(df):
    plt.figure(figsize=(12, 6))

    x = "nome_procedimento"
    y = "quantidade_cobro"
    title = "Frequência Média de Cobrança por Procedimento (até Devolver o Caso)"

    ax = sns.barplot(data=df, x=x, y=y, palette=palette_custom, hue=x, errorbar=None)
    ticks = range(len(df[x]))
    ax.set_xticks(ticks)
    ax.set_xticklabels(df[x], rotation=45, ha="right")

    ax = edit_bar_plot(ax, title=title, xlabel="Procedimentos", ylabel="Média", ylim=(0, max(df[y]) * 1.3), xticks=True, offset=0.1)
    plt.subplots_adjust(bottom=0.30)
    plt.show()
    return ax

def bar_plot_procedimento_media_dias_cobrar_resolver_exames_min5(df):
    plt.figure(figsize=(12, 6))

    x = "nome_procedimento"
    y = "quantidade_cobro"
    title = "Frequência Média de Cobrança por Procedimento mais Frequentes (até Devolver o Caso)"

    ax = sns.barplot(data=df, x=x, y=y, palette=palette_custom, hue=x, errorbar=None)
    ticks = range(len(df[x]))
    ax.set_xticks(ticks)
    ax.set_xticklabels(df[x], rotation=45, ha="right")

    ax = edit_bar_plot(ax, title=title, xlabel="Procedimentos", ylabel="Média", ylim=(0, 5), xticks=True, offset=0.1)
    plt.subplots_adjust(bottom=0.30)
    plt.show()
    return ax




def plot_quantidade_procedimentos(df, salvar=True):
    """
    Gráfico simples de quantidade de procedimentos.
    Eixo X = procedimentos
    Eixo Y = quantidade
    """

    # Limpar e remover procedimentos vazios
    df_plot = df.copy()
    df_plot["nome_procedimento"] = df_plot["nome_procedimento"].astype(str).str.strip()
    df_plot = df_plot[df_plot["nome_procedimento"] != ""]

    # Contagem de cada procedimento
    counts = df_plot["nome_procedimento"].value_counts()

    # Total de procedimentos
    total = len(df_plot)
    print(f"Total de procedimentos: {total}")
    print("\nQuantidade por procedimento:")
    print(counts)

    # Ajusta tamanho da figura baseado na quantidade de procedimentos
    width = max(10, len(counts) * 0.3)
    plt.figure(figsize=(width, 6))

    # Gráfico de barras verticais
    counts.plot(kind="bar", color="skyblue")
    plt.title(f"Quantidade de Procedimentos com Mais Retorno da Gerência para Solicitar Parecer(Total: {total})")
    plt.ylabel("Quantidade")
    plt.xlabel("Procedimento")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    if salvar:
        # cria pasta figures caso não exista
        os.makedirs("figures", exist_ok=True)
        # nome do arquivo com data/hora
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        caminho = f"figures/procedimentos_usuario_{timestamp}.png"
        plt.savefig(caminho, dpi=300, bbox_inches='tight')
        print(f"Gráfico salvo em: {caminho}")

    plt.show()





def plot_procedimentos_usuario(df, salvar=True):
    """
    Gráfico empilhado vertical:
    Eixo X = procedimentos
    Eixo Y = quantidade
    Cada cor = usuário
    """

    pivot = df.pivot_table(
        index="nome_procedimento",
        columns="nome",
        aggfunc="size",
        fill_value=0
    )

    total_procedimentos = len(df)
    print(f"Total de procedimentos: {total_procedimentos}")
    print("\nTabela resumo (quantidade de usuários por procedimento):")
    print(pivot)

    width = max(12, len(pivot) * 0.5)
    ax = pivot.plot(
        kind="bar",
        stacked=True,
        figsize=(width, 8),
        colormap="tab20"
    )
    plt.title(f"Distribuição de Procedimentos por Usuário com Mais Retorno da Gerência para Solicitar Parecer (Total de procedimentos: {total_procedimentos})")
    plt.ylabel("Quantidade")
    plt.xlabel("Procedimento")
    plt.legend(title="Usuário", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    if salvar:
        # cria pasta figures caso não exista
        os.makedirs("figures", exist_ok=True)
        # nome do arquivo com data/hora
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        caminho = f"figures/procedimentos_usuario_{timestamp}.png"
        plt.savefig(caminho, dpi=300, bbox_inches='tight')
        print(f"Gráfico salvo em: {caminho}")

    plt.show()


def stacked_bar_procedimentos(df, salvar=True):
    """
    Gráfico de barras empilhadas:
    Eixo X = procedimentos
    Eixo Y = quantidade
    Cada cor = Quantidade_PARECER na base e Quantidade_Total sobreposta
    Mostra os valores em cima das barras
    """
    df_plot = df.copy()
    df_plot = df_plot.sort_values(by="Quantidade_PARECER", ascending=False)

    plt.figure(figsize=(max(12, len(df_plot) * 0.3), 6))

    # Barra de Parecer na base
    barra_parecer = plt.bar(df_plot["Procedimento"], df_plot["Quantidade_PARECER"], 
                            label="Parecer", color="orange")
    
    # Barra Total acima do Parecer (só o que falta para atingir total)
    barra_total = plt.bar(df_plot["Procedimento"], df_plot["Quantidade_Total"] - df_plot["Quantidade_PARECER"],
                          bottom=df_plot["Quantidade_PARECER"],
                          label="Total", color="skyblue")

    # Adiciona os valores em cima das barras
    for idx, row in df_plot.iterrows():
        # Valor total no topo
        plt.text(idx, row["Quantidade_Total"] + 0.2, str(row["Quantidade_Total"]),
                 ha="center", va="bottom", fontsize=9)
        # Valor parecer dentro da barra laranja
        plt.text(idx, row["Quantidade_PARECER"]/2, str(row["Quantidade_PARECER"]),
                 ha="center", va="center", fontsize=9, color="white", fontweight="bold")

    plt.title("Quantidade de Procedimentos (Parecer / Total)")
    plt.ylabel("Quantidade")
    plt.xlabel("Procedimentos")
    plt.xticks(rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()

    if salvar:
        os.makedirs("figures", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        caminho = f"figures/stacked_bar_procedimentos_{timestamp}.png"
        plt.savefig(caminho, dpi=300, bbox_inches='tight')
        print(f"Gráfico salvo em: {caminho}")

    plt.show()
