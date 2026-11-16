# JSONs de candles para tutorial BTC/USDT

Este pacote contém 18 conjuntos sintéticos de candles **idênticos numericamente aos gráficos do tutorial**.

O JSON enviado como exemplo segue o formato Binance Spot `/api/v3/klines` com **12 posições por candle** e intervalo de **1 minuto**. Os arquivos `data/*-binance-klines.json` seguem a mesma disposição de índices, mas são candles **sintéticos de 1 hora**, pois assim foram desenhados os gráficos originais.

| Índice | Campo |
|---|---|
| 0 | Abertura UTC em milissegundos |
| 1 | Abertura (string) |
| 2 | Máxima (string) |
| 3 | Mínima (string) |
| 4 | Fechamento (string) |
| 5 | Volume-base sintético (string) |
| 6 | Fechamento UTC em milissegundos |
| 7 | Volume sintético em USDT (string) |
| 8 | Número simulado de trades (inteiro) |
| 9 | Volume sintético de compra taker em BTC (string) |
| 10 | Volume sintético de compra taker em USDT (string) |
| 11 | Campo ignorado ("0") |

Os índices 7–10 são preenchidos por simulação determinística. Os arquivos **não são payloads autênticos retornados pela Binance**. Os preços, timestamps e volumes-base originais são preservados.

## Hipóteses dos campos auxiliares

- Preço médio estimado: `(open + high + low + close) / 4`, dentro dos limites do candle; não representa um VWAP observado.
- Volume em USDT: volume-base × preço médio estimado.
- Número de trades: volume-base dividido por um tamanho médio simulado entre 0,0001 e 0,0005 BTC, arredondado para inteiro, com mínimo de 1.
- Volume de compra taker em BTC: fração simulada entre 35% e 65% do volume-base.
- Volume de compra taker em USDT: volume taker em BTC já arredondado × preço médio estimado. Assume-se o mesmo preço médio para compras e vendas taker.

As faixas são escolhas didáticas sem calibração com dados reais. Não permitem inferir fluxo de ordens ou liquidez de mercado. Os volumes usam strings com 8 casas decimais; o número de trades é inteiro.

Para reproduzir os valores, execute `python3 tutorial_estrategias_cripto_candles/simular_campos_klines.py` a partir da raiz do repositório. O script usa SHA-256 dos campos originais de cada candle, sem aleatoriedade variável entre execuções. Cada arquivo de metadados registra as fórmulas e suas limitações.

O arquivo `data/<estrategia>-metadados.json` contém os sinais COMPRA/VENDA, a descrição da estratégia, resultado hipotético e a associação com a imagem. O arquivo original `data/<estrategia>.json` permanece preservado.

Não compare os resultados sintéticos com os 301 candles reais fornecidos: são períodos, intervalos e bases de preços diferentes. Caso a intenção seja analisar candles reais, será necessário refazer gráficos e exemplos, com regras de sinal verificáveis e sem garantia de trades lucrativos.
