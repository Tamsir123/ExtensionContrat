#!/usr/bin/env python3
"""
Générateur d'icônes ConsentRadar
Crée les icônes PNG aux bonnes tailles pour l'extension
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_gradient_background(size, color1=(30, 58, 95), color2=(44, 82, 130)):
    """Crée un fond avec dégradé"""
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    for y in range(size):
        # Interpolation linéaire entre les deux couleurs
        ratio = y / size
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        
        draw.line([(0, y), (size, y)], fill=(r, g, b, 255))
    
    return image

def create_rounded_rectangle(size, radius_ratio=0.15):
    """Crée un rectangle arrondi pour le fond"""
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    radius = int(size * radius_ratio)
    
    # Dessiner le rectangle arrondi
    draw.rounded_rectangle([0, 0, size, size], radius=radius, fill=(30, 58, 95, 255))
    
    return image

def create_cr_logo(size):
    """Crée le logo CR avec effet 3D"""
    
    # Créer l'image de base avec fond arrondi
    image = create_rounded_rectangle(size)
    draw = ImageDraw.Draw(image)
    
    # Calculer la taille de la police
    font_size = int(size * 0.5)
    
    try:
        # Essayer d'utiliser une police système
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
            except:
                # Utiliser la police par défaut
                font = ImageFont.load_default()
    
    # Position du texte (centré)
    text = "CR"
    
    # Obtenir les dimensions du texte
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    # Ombre (effet 3D)
    shadow_offset = max(1, size // 32)
    draw.text((x + shadow_offset, y + shadow_offset), text, font=font, fill=(0, 0, 0, 100))
    
    # Texte principal
    draw.text((x, y), text, font=font, fill=(74, 144, 226, 255))
    
    # Reflet pour effet brillant
    overlay = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    
    # Dégradé de reflet
    for i in range(size // 2):
        alpha = int(50 * (1 - i / (size // 2)))
        overlay_draw.line([(0, i), (size, i)], fill=(255, 255, 255, alpha))
    
    # Appliquer le reflet
    image = Image.alpha_composite(image, overlay)
    
    return image

def generate_icons():
    """Génère toutes les icônes nécessaires"""
    sizes = [16, 48, 128]
    
    for size in sizes:
        print(f"Génération de l'icône {size}x{size}...")
        
        # Créer le logo
        logo = create_cr_logo(size)
        
        # Sauvegarder
        filename = f"icon{size}.png"
        logo.save(filename, "PNG")
        print(f"✅ {filename} créé avec succès!")
    
    print("\n🎉 Toutes les icônes ont été générées!")
    print("Vous pouvez maintenant remplacer les anciens fichiers d'icônes.")

if __name__ == "__main__":
    try:
        generate_icons()
    except ImportError:
        print("❌ PIL (Pillow) n'est pas installé.")
        print("Installez-le avec: pip install Pillow")
        print("\nAlternativement, utilisez le fichier create_icons.html dans votre navigateur.")
