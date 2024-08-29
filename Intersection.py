# Gerando interseção

from qgis.core import (
    QgsVectorLayer,
    QgsVectorFileWriter
)
import os
import processing 

# Caminho do shapefile e do diretório de saída
input_layer_path = r'seu-caminho\Contorno_mundo.shp'
output_directory = r'pasta-de-destino'  # nessa pasta, serão enviadas todos as interseções da grade com o contorno

os.makedirs(output_directory, exist_ok=True)

# Verifico se a camada foi carregada corretamente
if not os.path.exists(input_layer_path):
    print("Erro: Caminho da camada de contorno_linhas não encontrado!")
else:
    print("Caminho da camada de contorno_linhas encontrado!")


# Realizo um laço para realizar a interseção com as features de x até y (aqui, você pode escolher o intervalo das interseções desejadas)
for i in range(574, 578):  # De 574 até 577, por exemplo
    feature_layer_path = f'caminho-das-grades-geradas-na-Unique_Grades\\feature_{i}.shp'  # Aqui, mantenha dupla barra
    
    # Verifico se o caminho da feature existe
    if not os.path.exists(feature_layer_path):
        print(f"Erro: Caminho da camada feature_{i} não encontrado!")
        continue
    
    # Configuração da interseção
    params_intersect = {
        'INPUT': input_layer_path,
        'OVERLAY': feature_layer_path,
        'OUTPUT': 'memory:'
    }
    
    try:
        result_intersect = processing.run("qgis:intersection", params_intersect)
        temp_layer = result_intersect['OUTPUT']
    except Exception as e:
        print(f"Erro ao executar a Interseção para feature_{i}: {e}")
        continue

    # Verifico se o resultado tem feições. Caso não, ele não irá gerar. Isso otimiza muito o processamento.
    if temp_layer and temp_layer.featureCount() > 0:
        # Configuração do caminho de saída para o shapefile resultante
        output_shapefile_path = os.path.join(output_directory, f'contorno_intersect_feature_{i}.shp')

        # Salvo o shapefile final
        error = QgsVectorFileWriter.writeAsVectorFormat(temp_layer, output_shapefile_path, "UTF-8", driverName="ESRI Shapefile")
        if error == QgsVectorFileWriter.NoError:
            print(f"Interseção concluída e salva em: {output_shapefile_path}")
        else:
            print(f"Erro ao salvar o shapefile: {output_shapefile_path}")
    else:
        print(f"Nenhuma interseção encontrada para feature_{i}. Shapefile não foi criado.")
