import pandas as pd
import folium
from folium.features import GeoJson, GeoJsonTooltip
import json

def get_color(value, min_value, max_value):
    """
    Retorna uma cor em escala de vermelho baseada no valor, onde o valor mínimo é vermelho claro e o valor máximo é vermelho escuro.
    """
    if value is None:
        return '#cccccc'  # Cor cinza claro para valores nulos
    
    # Normaliza o valor entre 0 e 1
    norm_value = (value - min_value) / (max_value - min_value)
    
    # Calcula a intensidade do vermelho (mais alto é mais escuro)
    red_value = int(255 * (1 - norm_value))  # Vermelho será mais intenso para valores mais baixos
    
    # Para criar um tom de vermelho, o verde e o azul devem ser 0
    return f'#{red_value:02x}00{0:02x}'  # Formato de cor hexadecimal para vermelho


def generate_map(data):
    file_geojson = "src/bairros.geojson"
    
    # Carrega o arquivo GeoJSON
    with open(file_geojson, 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)
    
    # Adiciona os dados do DataFrame ao GeoJson e encontra valores mínimos e máximos
    all_values = []
    for feature in geojson_data['features']:
        bairro = feature['properties']['NOME_DIST']
        row = data[data['Bairro'] == bairro]
        if not row.empty:
            total_roubo = int(row['Total de ROUBO - OUTROS'].values[0])
            total_furto = int(row['Total de FURTO - OUTROS'].values[0])
            feature['properties']['Total_de_ROUBO_OUTROS'] = total_roubo
            feature['properties']['Total_de_FURTO_OUTROS'] = total_furto
            all_values.extend([total_roubo, total_furto])
        else:
            feature['properties']['Total_de_ROUBO_OUTROS'] = None
            feature['properties']['Total_de_FURTO_OUTROS'] = None
    
    # Determina valores mínimo e máximo
    min_value = min(all_values) if all_values else 0
    max_value = max(all_values) if all_values else 1
    
    # Cria um mapa base
    m = folium.Map(location=[-23.55052, -46.633308], zoom_start=12)
    
    def style_function(feature):
        total_furto = feature['properties'].get('Total_de_FURTO_OUTROS')
        if total_furto is not None:
            fill_color = get_color(total_furto, min_value, max_value)
        else:
            fill_color = '#cccccc'  # Cor cinza claro para valores nulos
        
        return {
            'fillColor': fill_color,
            'color': 'black',
            'weight': 2,
            'dashArray': '5, 5',
            'fillOpacity': 1
        }
    
    folium.GeoJson(
        geojson_data,
        name="Bairros",
        tooltip=GeoJsonTooltip(
            fields=["NOME_DIST", "Total_de_ROUBO_OUTROS", "Total_de_FURTO_OUTROS"],
            aliases=["Bairro", "Total de ROUBO - OUTROS", "Total de FURTO - OUTROS"],
            localize=True
        ),
        style_function=style_function
    ).add_to(m)
    
    # Salva o mapa em um arquivo HTML
    m.save("mapa.html")

# Exemplo de uso
data = pd.DataFrame({
    "Bairro": ["JOSE BONIFACIO", "Bom Retiro", "Campos Elísios", "Consolação", "Aclimação"],
    "Total de ROUBO - OUTROS": [4315, 870, 6191, 2836, 1424],
    "Total de FURTO - OUTROS": [11624, 4106, 11092, 7180, 4183]
})

generate_map(data)
