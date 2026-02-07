import flet as ft
import json
import random
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))


def main(page: ft.Page):
    page.title = "Sorteio Normal"
    page.window.width = 500
    page.window.height = 700
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 30

    # Nome do arquivo que o programa vai procurar
    ARQUIVO_DADOS = "src/normal.json"
    
    dados_participantes = []

    # --- Interface (Estilo Azul/Neutro) ---
    titulo = ft.Text("🍀 Sorteio da Lista", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_800)
    subtitulo = ft.Text("Sorteio equitativo (Todos com a mesma chance)", size=12, color=ft.Colors.GREY_600)
    
    lista_view = ft.ListView(expand=True, spacing=10, padding=10)
    stats_texto = ft.Text("Carregando...", italic=True, size=12)

    resultado_nome = ft.Text("", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900, text_align=ft.TextAlign.CENTER)
    
    container_resultado = ft.Container(
        content=resultado_nome,
        alignment=ft.alignment.center, 
        padding=40,
        bgcolor=ft.Colors.BLUE_50,
        border=ft.border.all(2, ft.Colors.BLUE_300),
        border_radius=15,
        visible=False, 
        animate_opacity=300,
    )

    def carregar_dados_automaticamente():
        nonlocal dados_participantes
        if not os.path.exists(ARQUIVO_DADOS):
            stats_texto.value = f"ERRO: Arquivo '{ARQUIVO_DADOS}' não encontrado!"
            stats_texto.color = ft.Colors.RED
            page.update()
            return

        try:
            with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
                conteudo = json.load(f)
                
                if "items" in conteudo:
                    for item in conteudo["items"]:
                        dados_participantes.append({
                            "nome": item.get("text", "Sem Nome")
                            # Não importamos fichas aqui, pois não é relevante
                        })
                else:
                    stats_texto.value = "Erro: JSON inválido."
                    return

            # Preenche a lista apenas com nomes
            for p in dados_participantes:
                lista_view.controls.append(
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.PERSON, color=ft.Colors.BLUE_400),
                        title=ft.Text(p['nome']),
                    )
                )
            
            stats_texto.value = f"{len(dados_participantes)} participantes prontos."
            btn_sortear.disabled = False
            
        except Exception as e:
            stats_texto.value = f"Erro: {e}"
        
        page.update()

    def sortear(e):
        if not dados_participantes: return

        nomes = [p['nome'] for p in dados_participantes]
        
        # Sorteio Normal (Random puro)
        escolhido = random.choice(nomes)

        resultado_nome.value = f"✨ {escolhido} ✨"
        container_resultado.visible = True
        page.update()

    btn_sortear = ft.FilledButton(
        "SORTEAR", 
        icon=ft.Icons.STAR, 
        on_click=sortear,
        disabled=True,
        height=60,
        style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_600)
    )

    page.add(
        titulo,
        subtitulo,
        stats_texto,
        ft.Divider(),
        ft.Text("Lista:", weight=ft.FontWeight.BOLD),
        ft.Container(lista_view, height=200, border=ft.border.all(1, ft.Colors.GREY_300), border_radius=8),
        ft.Divider(),
        btn_sortear,
        ft.Container(height=20),
        container_resultado
    )

    carregar_dados_automaticamente()

ft.app(target=main)