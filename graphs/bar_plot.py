import seaborn as sns
import matplotlib.pyplot as plt

palette = sns.color_palette("pastel", n_colors=20)

def edit_bar_plot(ax, title=None, xlabel=None, ylabel=None, ylim=None, xticks=True, tight_layout=True, despine=True):
    if title:
        ax.set_title(title, fontsize=14, weight="bold")
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=12)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=12)
    if ylim:
        ax.set_ylim(ylim)
    if despine:
        sns.despine(ax=ax)
    if tight_layout:
        plt.tight_layout()
    
    # Adiciona valores em cima das barras
    for p in ax.patches:
        height = p.get_height()
        width = p.get_width()
        x = p.get_x() + width / 2
        y = height
        ax.text(x, y, f"{height:.0f}", ha="center", va="bottom", fontsize=10)
    
    # Rotaciona os labels do eixo X
    if xticks:
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    else:
        ax.set_xticklabels([])

    return ax

def procedimentos_bar_plot(df, x="word", y="count", title="Procedimentos Mais Frequentes"):
    plt.figure(figsize=(12, 6))
    
    # Garantir que a paleta seja longa o suficiente
    palette_extended = palette * (len(df) // len(palette) + 1)
    
    ax = sns.barplot(data=df, x=x, y=y, palette=palette_extended[:len(df)], errorbar=None)
    ax = edit_bar_plot(ax, title=title, xlabel=x, ylabel=y, ylim=(0, max(df[y]) * 1.1), xticks=True)
    plt.subplots_adjust(bottom=0.25)
    #plt.show()
    return ax



