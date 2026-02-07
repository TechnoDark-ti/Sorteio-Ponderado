import flet as ft
import json
import random
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))

def main(page: ft.Page):
    page.title = "Sorteio Ponderado (Fichas)"
    page.window.width = 500
    page.window.height = 700
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 30

    # Nome do arquivo que o programa vai procurar na pasta
    ARQUIVO_DADOS = "src/fichas.json"
    
    dados_participantes = []

    # --- Elementos da Interface ---
    titulo = ft.Text("🏆 Sorteio Ponderado", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE_800)
    subtitulo = ft.Text("Quanto mais fichas, maior a chance!", size=14, color=ft.Colors.GREY_600)
    
    lista_view = ft.ListView(expand=True, spacing=10, padding=10)
    stats_texto = ft.Text("Carregando...", italic=True, size=12)

    resultado_nome = ft.Text("", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK, text_align=ft.TextAlign.CENTER)
    resultado_fichas = ft.Text("", size=20, weight=ft.FontWeight.W_500, color=ft.Colors.ORANGE_700)
    
    container_resultado = ft.Container(
        content=ft.Column([resultado_nome, resultado_fichas], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        alignment=ft.alignment.center, 
        padding=30,
        bgcolor=ft.Colors.ORANGE_50,
        border=ft.border.all(2, ft.Colors.ORANGE_400),
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
                
                # Lógica para ler o formato específico do seu arquivo
                if "items" in conteudo:
                    for item in conteudo["items"]:
                        dados_participantes.append({
                            "nome": item.get("text", "Sem Nome"),
                            "fichas": item.get("weight", 0) # Pega o peso (fichas)
                        })
                else:
                    stats_texto.value = "Erro: Formato do JSON inválido."
                    return

            # Preenche a lista visual
            for p in dados_participantes:
                lista_view.controls.append(
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.MONETIZATION_ON, color=ft.Colors.ORANGE_500),
                        title=ft.Text(p['nome']),
                        trailing=ft.Text(f"{p['fichas']}", weight=ft.FontWeight.BOLD),
                    )
                )
            
            stats_texto.value = f"{len(dados_participantes)} participantes carregados."
            btn_sortear.disabled = False
            
        except Exception as e:
            stats_texto.value = f"Erro ao ler arquivo: {e}"
        
        page.update()

    def sortear(e):
        if not dados_participantes: return

        nomes = [p['nome'] for p in dados_participantes]
        pesos = [float(p['fichas']) for p in dados_participantes] # Usa as fichas como peso
        
        # Sorteio ponderado
        escolhido_nome = random.choices(nomes, weights=pesos, k=1)[0]
        
        # Busca as fichas do ganhador para exibir
        fichas_ganhador = next(p['fichas'] for p in dados_participantes if p['nome'] == escolhido_nome)

        resultado_nome.value = f"🎉 {escolhido_nome}"
        resultado_fichas.value = f"Possui {fichas_ganhador} fichas"
        container_resultado.visible = True
        page.update()

    btn_sortear = ft.FilledButton(
        "SORTEAR AGORA", 
        icon=ft.Icons.CASINO, 
        on_click=sortear,
        disabled=True, # Começa desativado até carregar
        height=60,
        style=ft.ButtonStyle(bgcolor=ft.Colors.ORANGE_700)
    )

    page.add(
        titulo,
        subtitulo,
        stats_texto,
        ft.Divider(),
        ft.Text("Participantes:", weight=ft.FontWeight.BOLD),
        ft.Container(lista_view, height=200, border=ft.border.all(1, ft.Colors.GREY_300), border_radius=8),
        ft.Divider(),
        btn_sortear,
        ft.Container(height=20),
        container_resultado
    )

    # Carrega assim que abre
    carregar_dados_automaticamente()

ft.app(target=main)