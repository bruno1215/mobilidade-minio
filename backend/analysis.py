import pandas as pd
import matplotlib.pyplot as plt
import io # Para salvar a imagem em memória

def analyze_mobility_data(data_stream):
    """
    Realiza a análise de mobilidade e gera o gráfico.
    data_stream: Um stream de bytes do arquivo CSV.
    Retorna: Um buffer de bytes da imagem PNG do gráfico ou None em caso de erro.
    """
    try:
        # 1. Carregar os dados de mobilidade urbana (do stream)
        df = pd.read_csv(data_stream)
        # df.head() # Útil para debug, não necessário para a função principal
        # 2. Analisar os dados com pandas
        bairro_group = df.groupby('bairro')['passageiros'].sum().sort_values(ascending=False)
        # 3. Gerar gráficos com matplotlib
        plt.figure(figsize=(12, 6)) # Ajuste o tamanho se necessário
        bairro_group.plot(kind='bar')
        plt.title('Total de Passageiros por Bairro em Teresina-PI')
        plt.xlabel('Bairro') # Correção da label
        plt.ylabel('Total de Passageiros') # Correção da label
        plt.xticks(rotation=45, ha="right") # Melhorar a legibilidade dos bairros
        plt.tight_layout()
        # Salvar o gráfico em um buffer de bytes em memória
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0) # Retorna o cursor para o início do buffer
        plt.close() # Fecha a figura para liberar memória
        return img_buffer
    except Exception as e:
        print(f"Ocorreu um erro durante a análise ou geração do gráfico: {e}")
        return None