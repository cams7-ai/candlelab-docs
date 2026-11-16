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
| 7 | Volume em moeda de cotação (null) |
| 8 | Número de trades (null) |
| 9 | Volume de compra taker em moeda-base (null) |
| 10 | Volume de compra taker em moeda de cotação (null) |
| 11 | Campo ignorado ("0") |

Os índices 7–10 são `null` porque não existem nos dados sintéticos originais. Portanto os arquivos **não são payloads autênticos retornados pela Binance** e exigem tratamento de campos ausentes.

O arquivo `data/<estrategia>-metadados.json` contém os sinais COMPRA/VENDA, a descrição da estratégia, resultado hipotético e a associação com a imagem. O arquivo original `data/<estrategia>.json` permanece preservado.

Não compare os resultados sintéticos com os 301 candles reais fornecidos: são períodos, intervalos e bases de preços diferentes. Caso a intenção seja analisar candles reais, será necessário refazer gráficos e exemplos, com regras de sinal verificáveis e sem garantia de trades lucrativos.
