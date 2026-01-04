import pandas as pd
import numpy as np
import statistics
from scipy import stats
from scipy.stats import kruskal

# Teste t para uma média
def teste_t_uma_media(df, var_quanti, valor_referencia, alfa=0.05):
    resultado_t_test = stats.ttest_1samp(df[var_quanti].dropna(), valor_referencia)
    print("Teste t para uma Média:")
    print("Estatística t:", resultado_t_test.statistic)
    print("Valor p:", resultado_t_test.pvalue)
    if resultado_t_test.pvalue <= alfa:
        print(f"Rejeita-se a hipótese nula. A média é significativamente diferente de {valor_referencia}.")
    else:
        print(f"Não se rejeita a hipótese nula. A média não é significativamente diferente de {valor_referencia}.")
    return resultado_t_test

# Teste de Levene para homogeneidade de variâncias
def teste_levene(group_a, group_b, column, alfa=0.05):
    resultado = stats.levene(
        group_a[column].dropna(),
        group_b[column].dropna()
    )

    print("Teste de Levene:")
    print("Estatística:", resultado.statistic)
    print("Valor p:", resultado.pvalue)

    if resultado.pvalue <= alfa:
        print("Rejeita-se a hipótese nula. As variâncias não são homogêneas.")
    else:
        print("Não se rejeita a hipótese nula. As variâncias podem ser consideradas homogêneas.")

    return resultado

def teste_mannwhitney(group_a, group_b, column, alfa=0.05):
    # Normalidade
    shapiro_a = stats.shapiro(group_a[column].dropna())
    shapiro_b = stats.shapiro(group_b[column].dropna())
    
    print("Teste de Shapiro-Wilk:")
    print(f"Grupo A - Estatística: {shapiro_a.statistic:.4f}, p-valor: {shapiro_a.pvalue:.4f}")
    print(f"Grupo B - Estatística: {shapiro_b.statistic:.4f}, p-valor: {shapiro_b.pvalue:.4f}")

    # Se algum grupo não for normal - usar Mann-Whitney
    if shapiro_a.pvalue <= alfa or shapiro_b.pvalue <= alfa:
        resultado = stats.mannwhitneyu(group_a[column].dropna(),
                                       group_b[column].dropna(),
                                       alternative="two-sided")
        print("\nTeste Mann–Whitney U:")
        print(f"U: {resultado.statistic:.4f}, p-valor: {resultado.pvalue:.4f}")
        if resultado.pvalue <= alfa:
            print("Rejeita-se a hipótese nula, logo, diferença significativa entre os grupos.")
        else:
            print("Não se rejeita a hipótese nula. Não há diferença significativa.")
    else:
        print("\nAmbos os grupos parecem normais → considere usar teste t.")

# Teste t para amostras independentes
def teste_t_amostras_ind(group_a, group_b, column, alfa):
    resultado_teste_levene = stats.levene(group_a[column], group_b[column])
    if resultado_teste_levene.pvalue <= alfa:
        equal_var=False
    else:
        equal_var=True
    resultado_t_test_ind = stats.ttest_ind(group_a[column], group_b[column], equal_var=equal_var)
    print("Teste t para Amostras Independentes:")
    print("Estatística t:", resultado_t_test_ind.statistic)
    print("Valor p:", resultado_t_test_ind.pvalue)
    if resultado_t_test_ind.pvalue <= alfa:
        print("Rejeita-se a hipótese nula, logo, há diferença significativa entre as médias nos grupos.")
    else:
        print("Não se rejeita a hipótese nula, logo, não há diferença significativa entre as médias nos grupos.")
    return 

# Intervalo de confiança
def intervalo_confianca(group_a, group_b, conf_level=0.95):
    conf_interval_a = stats.norm.interval(conf_level, loc=np.mean(group_a), scale=stats.sem(group_a))
    conf_interval_b = stats.norm.interval(conf_level, loc=np.mean(group_b), scale=stats.sem(group_b))
    print(f"Intervalo de Confiança a {conf_level*100:.0f}% para o grupo 'A':", conf_interval_a)
    print(f"Intervalo de Confiança a {conf_level*100:.0f}% para o grupo 'B':", conf_interval_b)
    return conf_interval_a, conf_interval_b

# Teste de normalidade Shapiro-Wilk
def teste_normalidade_shapirowilk(df, column, alfa=0.05):
    estatistica_teste, valor_p = stats.shapiro(df[column].dropna())
    print("Teste de Normalidade Shapiro-Wilk:")
    print("Estatística do Teste:", estatistica_teste)
    print("Valor p:", valor_p)
    if valor_p <= alfa:
        print("Rejeita-se a hipótese nula. A variável não segue uma distribuição normal.")
    else:
        print("Não se rejeita a hipótese nula. A variável segue uma distribuição normal.")
    return estatistica_teste, valor_p

# Teste t para amostras emparelhadas
def teste_t_amostras_emparelhadas(amostra_antes, amostra_depois, alfa=0.05):
    estatistica_t, valor_p = stats.ttest_rel(amostra_antes, amostra_depois)
    print("Teste t para Amostras Emparelhadas:")
    print("Estatística t:", estatistica_t)
    print("Valor p:", valor_p)
    print("Média antes:", statistics.mean(amostra_antes))
    print("Média depois:", statistics.mean(amostra_depois))
    if valor_p <= alfa:
        print("Houve diferença significativa entre as médias antes e depois.")
    else:
        print("Não houve diferença significativa entre as médias antes e depois.")
    return estatistica_t, valor_p

# Teste de Wilcoxon
def teste_wilcoxon(amostra_antes, amostra_depois, alfa=0.05):
    estatistica_teste, valor_p = stats.wilcoxon(amostra_antes, amostra_depois)
    print("Teste de Wilcoxon:")
    print("Estatística do Teste:", estatistica_teste)
    print("Valor p:", valor_p)
    if valor_p <= alfa:
        print("Houve uma diferença significativa entre os desempenhos antes e depois.")
    else:
        print("Não houve diferença significativa entre os desempenhos antes e depois.")
    return estatistica_teste, valor_p

# Teste ANOVA
def teste_anova(df, var_quali, var_quanti, alfa=0.05):
    grupos = [df[df[var_quali] == categoria][var_quanti].dropna() for categoria in df[var_quali].unique()]
    resultado_anova = stats.f_oneway(*grupos)
    print("Teste ANOVA:")
    print("Estatística F:", resultado_anova.statistic)
    print("Valor p:", resultado_anova.pvalue)
    if resultado_anova.pvalue <= alfa:
        print("Rejeita-se a hipótese nula. Há pelo menos um grupo com média diferente.")
    else:
        print("Não se rejeita a hipótese nula. Não há diferença significativa nas médias entre os grupos.")
    return resultado_anova

# Teste do Qui-Quadrado
def teste_qui_quadrado(df, var_quali1, var_quali2, alfa=0.05):
    tabela_contingencia = pd.crosstab(df[var_quali1], df[var_quali2])
    resultado_quiquadrado = stats.chi2_contingency(tabela_contingencia)
    print("Teste Qui-Quadrado:")
    print(tabela_contingencia)
    print("Estatística Qui-Quadrado:", resultado_quiquadrado.statistic)
    print("Valor p:", resultado_quiquadrado.pvalue)
    if resultado_quiquadrado.pvalue <= alfa:
        print("Rejeita-se a hipótese nula. Existe associação entre as variáveis.")
    else:
        print("Não se rejeita a hipótese nula. Não há associação entre as variáveis.")
    return resultado_quiquadrado

# Teste Kruskal-Wallis
def teste_kruskal_wallis(df, group_column, value_column, alfa=0.05):
    grupos = [grupo[value_column].dropna() for nome, grupo in df.groupby(group_column)]
    estatistica_teste, valor_p = kruskal(*grupos)
    print("Teste Kruskal-Wallis:")
    print("Estatística do Teste:", estatistica_teste)
    print("Valor p:", valor_p)
    if valor_p <= alfa:
        print("Rejeita-se a hipótese nula. Há diferenças significativas entre os grupos.")
    else:
        print("Não se rejeita a hipótese nula. Não há diferenças significativas entre os grupos.")
    return estatistica_teste, valor_p
