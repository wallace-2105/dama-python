"""
Script para baixar a fonte Playfair Display Bold do Google Fonts.
Uso: python baixar_fonte.py

A fonte é opcional — o jogo usa Georgia como fallback.
"""

import urllib.request
import os
import zipfile
import io

# URL do pacote Playfair Display no Google Fonts
FONT_URL = "https://fonts.google.com/download?family=Playfair+Display"
DEST_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
DEST_FILE = os.path.join(DEST_DIR, "PlayfairDisplay-Bold.ttf")


def main():
    os.makedirs(DEST_DIR, exist_ok=True)

    if os.path.exists(DEST_FILE):
        print(f"✓ Fonte já existe: {DEST_FILE}")
        return

    print("Baixando Playfair Display do Google Fonts...")
    try:
        # Baixa o ZIP do Google Fonts
        req = urllib.request.Request(FONT_URL, headers={
            "User-Agent": "Mozilla/5.0"
        })
        response = urllib.request.urlopen(req, timeout=15)
        zip_data = response.read()

        # Extrai o arquivo Bold (.ttf) do ZIP
        with zipfile.ZipFile(io.BytesIO(zip_data)) as zf:
            # Procura pelo arquivo Bold (static ou variável)
            bold_file = None
            for name in zf.namelist():
                if "Bold" in name and name.endswith(".ttf"):
                    bold_file = name
                    break

            if bold_file:
                font_data = zf.read(bold_file)
                with open(DEST_FILE, "wb") as f:
                    f.write(font_data)
                print(f"✓ Fonte salva em: {DEST_FILE}")
            else:
                # Se não encontrou Bold, pega qualquer .ttf
                for name in zf.namelist():
                    if name.endswith(".ttf"):
                        font_data = zf.read(name)
                        with open(DEST_FILE, "wb") as f:
                            f.write(font_data)
                        print(f"✓ Fonte salva em: {DEST_FILE}")
                        break
                else:
                    print("✗ Nenhum arquivo .ttf encontrado no pacote.")

    except Exception as e:
        print(f"✗ Erro ao baixar: {e}")
        print("  O jogo usará a fonte Georgia como fallback.")
        print("  Você também pode baixar manualmente de:")
        print("  https://fonts.google.com/specimen/Playfair+Display")
        print(f"  E salvar o arquivo .ttf Bold em: {DEST_DIR}")


if __name__ == "__main__":
    main()
