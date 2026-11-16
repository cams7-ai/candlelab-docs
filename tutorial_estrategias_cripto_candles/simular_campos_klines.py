"""Preenche campos auxiliares sintéticos sem alterar OHLCV ou sinais."""

import hashlib
import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


BASE = Path(__file__).resolve().parent
PRECISAO = Decimal("0.00000001")


def decimal_string(valor):
    return format(valor.quantize(PRECISAO, rounding=ROUND_HALF_UP), ".8f")


def main():
    for arquivo in sorted((BASE / "data").glob("*-binance-klines.json")):
        candles = json.loads(arquivo.read_text())
        for candle in candles:
            # O mesmo OHLCV e timestamp sempre produzem os mesmos valores.
            chave = json.dumps(candle[:7], separators=(",", ":"))
            digest = hashlib.sha256(chave.encode()).digest()
            abertura, maxima, minima, fechamento, volume = map(Decimal, candle[1:6])
            preco_medio = (abertura + maxima + minima + fechamento) / 4
            # Hipóteses didáticas; não calibradas com negócios reais da Binance.
            tamanho_medio = Decimal(10000 + int.from_bytes(digest[:4], "big") % 40001) / 100000000
            fracao_taker = Decimal(35000000 + int.from_bytes(digest[4:8], "big") % 30000001) / 100000000
            volume_taker = (volume * fracao_taker).quantize(PRECISAO, rounding=ROUND_HALF_UP)
            candle[7] = decimal_string(volume * preco_medio)
            candle[8] = max(1, int((volume / tamanho_medio).to_integral_value(rounding=ROUND_HALF_UP)))
            candle[9] = decimal_string(volume_taker)
            candle[10] = decimal_string(volume_taker * preco_medio)
        arquivo.write_text(json.dumps(candles, ensure_ascii=False, indent=2) + "\n")

        metadados_path = arquivo.with_name(arquivo.name.replace("-binance-klines.json", "-metadados.json"))
        metadados = json.loads(metadados_path.read_text())
        metadados.pop("campos_indisponiveis", None)
        metadados["convencao"] = "Todos os campos sao sinteticos; estrutura de 12 posicoes inspirada na Binance, sem representar resposta real da API. Volume no indice 5 preservado."
        metadados["simulacao_campos_auxiliares"] = {
            "versao": 1,
            "indices": [7, 8, 9, 10],
            "preco_medio_estimado": "(open + high + low + close) / 4; nao e VWAP observado",
            "indice_7": "volume_base * preco_medio_estimado",
            "indice_8": "max(1, arredondar(volume_base / tamanho_medio_simulado)); tamanho medio entre 0.0001 e 0.0005 BTC por negocio",
            "indice_9": "volume_base * fracao_taker_simulada; fracao entre 0.35 e 0.65",
            "indice_10": "volume_taker_base_arredondado * preco_medio_estimado",
            "determinismo": "SHA-256 do JSON compacto das posicoes 0 a 6; bytes 0:4 para tamanho medio e 4:8 para fracao taker, interpretados como inteiros big-endian",
            "arredondamento": "Volumes com 8 casas decimais e ROUND_HALF_UP; numero de negocios inteiro",
            "script": "../simular_campos_klines.py",
            "limitacoes": "Hipoteses didaticas sem calibracao empirica; nao reconstruem negocios, fluxo agressor ou liquidez reais. Mesmo preco medio assumido para compras e vendas taker."
        }
        metadados_path.write_text(json.dumps(metadados, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
