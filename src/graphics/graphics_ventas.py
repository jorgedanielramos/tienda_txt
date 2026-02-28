import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def ventas_globales_12_mes(ventas_por_mes,var_x, var_y,titulo,titulo_eje_x,titulo_eje_y,tipo_grafico="linea"):
    # Asegurar un solo valor por mes
    ventas_por_mes = ventas_por_mes.groupby(var_x, as_index=False)[var_y].sum()
    fig, ax = plt.subplots(figsize=(12, 8))
    
    if tipo_grafico == "linea":
        sns.lineplot(
            data=ventas_por_mes,
            x=var_x,
            y=var_y,
            marker='o',
            ci=None,
            ax=ax
        )
    elif tipo_grafico == "barra":
        sns.barplot(
            data=ventas_por_mes.sort_values(var_y, ascending=False),
            x=var_x,
            y=var_y,
            ax=ax,
            ci=None,
            color='steelblue'           
        )
    ax.set_title(titulo)
    ax.set_xlabel(titulo_eje_x)
    ax.set_ylabel(titulo_eje_y)

    plt.setp(ax.get_xticklabels(), rotation=0, ha='right')

    # Etiquetas sobre cada punto
    for i, row in ventas_por_mes.iterrows():
        ax.text(
            row[var_x],
            row[var_y],
            f"{row[var_y]:.0f}",
            ha='center',
            va='bottom',
            fontsize=9,
            color='red'
        )

    plt.tight_layout()
    plt.show()
