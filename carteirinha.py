
from PIL import Image, ImageDraw, ImageFont

def gerar_carteirinha(nome, nascimento, endereco, funcao, status):
    base = Image.new("RGB", (400, 250), color=(255, 255, 255))
    draw = ImageDraw.Draw(base)
    fonte = ImageFont.load_default()

    draw.text((10, 10), f"Nome: {nome}", font=fonte, fill="black")
    draw.text((10, 40), f"Nasc: {nascimento}", font=fonte, fill="black")
    draw.text((10, 70), f"Endereço: {endereco}", font=fonte, fill="black")
    draw.text((10, 100), f"Função: {funcao}", font=fonte, fill="black")
    draw.text((10, 130), f"Status: {status}", font=fonte, fill="black")

    path = f"img/{nome.replace(' ', '_')}_carteirinha.png"
    base.save(path)
    return path
