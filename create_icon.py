from PIL import Image, ImageDraw, ImageFont
import os

def create_app_icon():
    """Cria um ícone personalizado para o aplicativo"""
    
    # Tamanhos padrão para ícones
    sizes = [16, 32, 48, 64, 128, 256]
    
    # Cores do tema noturno
    bg_color = "#1e1e1e"      # Fundo escuro
    primary_color = "#00d4aa"  # Verde-azulado (microfone)
    accent_color = "#ffffff"   # Branco para texto
    
    images = []
    
    for size in sizes:
        # Criar imagem
        img = Image.new('RGBA', (size, size), bg_color)
        draw = ImageDraw.Draw(img)
        
        # Calcular proporções
        center = size // 2
        mic_width = size // 3
        mic_height = size // 2
        
        # Desenhar microfone
        # Corpo do microfone (retângulo arredondado)
        mic_left = center - mic_width // 2
        mic_right = center + mic_width // 2
        mic_top = center - mic_height // 2
        mic_bottom = center + mic_height // 4
        
        draw.rounded_rectangle(
            [mic_left, mic_top, mic_right, mic_bottom],
            radius=mic_width // 4,
            fill=primary_color
        )
        
        # Haste do microfone
        stem_width = size // 12
        stem_height = size // 6
        stem_left = center - stem_width // 2
        stem_right = center + stem_width // 2
        stem_top = mic_bottom
        stem_bottom = stem_top + stem_height
        
        draw.rectangle(
            [stem_left, stem_top, stem_right, stem_bottom],
            fill=primary_color
        )
        
        # Base do microfone
        base_width = mic_width
        base_height = size // 16
        base_left = center - base_width // 2
        base_right = center + base_width // 2
        base_top = stem_bottom
        base_bottom = base_top + base_height
        
        draw.rectangle(
            [base_left, base_top, base_right, base_bottom],
            fill=primary_color
        )
        
        # Detalhes do microfone (linhas horizontais)
        for i in range(3):
            line_y = mic_top + (mic_bottom - mic_top) * (i + 1) // 4
            line_left = mic_left + mic_width // 6
            line_right = mic_right - mic_width // 6
            draw.line(
                [line_left, line_y, line_right, line_y],
                fill=bg_color,
                width=max(1, size // 32)
            )
        
        # Adicionar pequeno círculo para representar som/ondas
        if size >= 32:
            wave_radius = size // 16
            wave_x = mic_right + size // 8
            wave_y = center - size // 6
            
            draw.ellipse(
                [wave_x - wave_radius, wave_y - wave_radius,
                 wave_x + wave_radius, wave_y + wave_radius],
                outline=accent_color,
                width=max(1, size // 32)
            )
        
        images.append(img)
    
    # Salvar como ICO
    try:
        images[0].save(
            'icon.ico',
            format='ICO',
            sizes=[(img.width, img.height) for img in images],
            append_images=images[1:]
        )
        print("✅ Ícone criado: icon.ico")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar ícone: {e}")
        return False

def create_simple_icon():
    """Cria um ícone simples usando apenas PIL básico"""
    try:
        # Criar ícone simples 32x32
        size = 32
        img = Image.new('RGBA', (size, size), '#1e1e1e')
        draw = ImageDraw.Draw(img)
        
        # Desenhar círculo simples com M (microfone)
        draw.ellipse([4, 4, 28, 28], fill='#00d4aa', outline='#ffffff', width=2)
        
        # Tentar adicionar texto 'M'
        try:
            font = ImageFont.truetype("arial.ttf", 16)
        except:
            font = ImageFont.load_default()
        
        # Desenhar M no centro
        text = "🎤"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size - text_width) // 2
        y = (size - text_height) // 2
        
        draw.text((x, y), text, fill='#ffffff', font=font)
        
        # Salvar
        img.save('icon.ico', format='ICO')
        print("✅ Ícone simples criado: icon.ico")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar ícone simples: {e}")
        return False

if __name__ == "__main__":
    print("🎨 Criando ícone personalizado...")
    
    try:
        # Tentar criar ícone detalhado
        if create_app_icon():
            print("✅ Sucesso!")
        else:
            # Fallback para ícone simples
            print("⚠️ Tentando ícone simples...")
            create_simple_icon()
    except ImportError:
        print("❌ PIL não encontrado. Instalando...")
        os.system("pip install Pillow")
        create_app_icon() 