import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

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
        bbox=dict(facecolor='gray', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.3'))


def bar_plot_procedimentos_maior_quantidade(df):
    plt.figure(figsize=(12, 6))
    
    x="Procedimentos"
    y="Quantidade"
    title="Procedimentos Mais Frequentes"

    ax = sns.barplot(data=df, x=x, y=y, palette=palette_custom, hue=x, errorbar=None)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")

    ax = edit_bar_plot(ax, title=title, xlabel=x, ylabel=y, ylim=(0, max(df[y]) * 1.3), xticks=True, offset=2, grid=True)
    plt.subplots_adjust(bottom=0.30)
    plt.show()

    return ax

def bar_plot_top_quantidade_parecer(df):
    plt.figure(figsize=(len(df) * 0.6, 6)) 

    x = "Procedimentos"
    y = "Quantidade_PARECER"
    title = "Procedimentos Mais Frequentes (em Parecer)"

    ax = sns.barplot(data=df, x=x, y=y, palette=palette_custom, hue=x, errorbar=None)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")

    ax = edit_bar_plot(ax, title=title, xlabel=x, ylabel="Quantidade", ylim=(0, max(df[y]) * 1.3), xticks=True, offset=0.7, grid=True)
    plt.subplots_adjust(bottom=0.25)
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



