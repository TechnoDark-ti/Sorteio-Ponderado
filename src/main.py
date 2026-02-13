import flet as ft
import json
import random

def main(page: ft.Page):
    page.title = "Sorteador Proporcional"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # Configuração da janela
    page.window.width = 600
    page.window.height = 750
    page.padding = 30

    # Estado da aplicação
    dados_carregados = []

    # --- Componentes de UI ---
    titulo = ft.Text("Sorteador de Fichas", size=30, weight=ft.FontWeight.BOLD)
    subtitulo = ft.Text("Carregue o arquivo JSON do 'weighted-random-picker'", size=12, color=ft.Colors.GREY_600)
    
    lista_view = ft.ListView(expand=True, spacing=10, padding=10)
    
    tipo_sorteio = ft.RadioGroup(content=ft.Row([
        ft.Radio(value="ponderado", label="Ponderado (Usa pesos)"),
        ft.Radio(value="normal", label="Normal (Chance igual)"),
    ]))
    tipo_sorteio.value = "ponderado"

    resultado_texto = ft.Text("", size=34, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700, text_align=ft.TextAlign.CENTER)
    
    container_resultado = ft.Container(
        content=resultado_texto,
        alignment=ft.alignment.center, 
        padding=30,
        bgcolor=ft.Colors.YELLOW_100,
        border=ft.border.all(2, ft.Colors.YELLOW_700),
        border_radius=15,
        visible=False, 
        animate_opacity=300,
    )

    def atualizar_lista():
        lista_view.controls.clear()
        if not dados_carregados:
            return

        for item in dados_carregados:
            lista_view.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.PERSON),
                    title=ft.Text(item['nome']),
                    trailing=ft.Text(f"{item['fichas']} fichas", weight=ft.FontWeight.BOLD),
                    bgcolor=ft.Colors.WHITE,
                )
            )
        page.update()

    def mostrar_snack(texto, cor):
        snack = ft.SnackBar(ft.Text(texto), bgcolor=cor)
        page.overlay.append(snack)
        snack.open = True
        page.update()

    def on_file_result(e: ft.FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    conteudo_bruto = json.load(f)
                    
                    nonlocal dados_carregados
                    dados_carregados = []

                    # Adaptação para ler a estrutura do seu arquivo específico
                    if isinstance(conteudo_bruto, dict) and "items" in conteudo_bruto:
                        # Arquivo do weighted-random-picker
                        for item in conteudo_bruto["items"]:
                            dados_carregados.append({
                                "nome": item.get("text", "Sem Nome"),
                                "fichas": item.get("weight", 1)
                            })
                    elif isinstance(conteudo_bruto, list):
                        # Arquivo simples (caso antigo)
                        dados_carregados = conteudo_bruto
                    else:
                        raise Exception("Formato de JSON não reconhecido.")

                atualizar_lista()
                
                if dados_carregados:
                    btn_sortear.disabled = False
                    stats_texto.value = f"Participantes: {len(dados_carregados)}"
                    container_resultado.visible = False
                    mostrar_snack("Base de dados importada com sucesso!", ft.Colors.GREEN_700)
                else:
                    mostrar_snack("O arquivo não contém participantes.", ft.Colors.RED_700)
                
            except Exception as ex:
                mostrar_snack(f"Erro ao carregar: {ex}", ft.Colors.RED_700)
            page.update()

    file_picker = ft.FilePicker(on_result=on_file_result)
    page.overlay.append(file_picker)

    def sortear(e):
        if not dados_carregados:
            return

        nomes = [item['nome'] for item in dados_carregados]
        
        if tipo_sorteio.value == "ponderado":
            pesos = [float(item['fichas']) for item in dados_carregados]
            # random.choices retorna uma lista, pegamos o primeiro elemento [0]
            vencedor = random.choices(nomes, weights=pesos, k=1)[0]
        else:
            vencedor = random.choice(nomes)

        resultado_texto.value = f"{vencedor}"
        container_resultado.visible = True
        page.update()

    btn_importar = ft.ElevatedButton(
        "Carregar JSON", 
        icon=ft.Icons.UPLOAD_FILE, 
        on_click=lambda _: file_picker.pick_files()
    )
    
    stats_texto = ft.Text("Nenhum arquivo carregado", italic=True)

    btn_sortear = ft.FilledButton(
        "REALIZAR SORTEIO", 
        icon=ft.Icons.CASINO, 
        on_click=sortear,
        disabled=True,
        height=60
    )

    page.add(
        titulo,
        subtitulo,
        ft.Divider(height=10),
        ft.Row([btn_importar, stats_texto], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Text("Lista de Participantes:", weight=ft.FontWeight.BOLD),
        ft.Container(
            content=lista_view, 
            height=200, 
            border=ft.border.all(1, ft.Colors.GREY_400), 
            border_radius=8,
            bgcolor=ft.Colors.GREY_50
        ),
        ft.Text("Modo de sorteio:"),
        tipo_sorteio,
        ft.Divider(height=20),
        btn_sortear,
        ft.Container(height=20),
        container_resultado
    )

ft.app(target=main)