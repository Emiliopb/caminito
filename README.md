# Caminito: predicción y clusterización de peregrinos
Trabajo fin de máster centrado en el Camino de Santiago. Se analizan los datos de peregrinos de los últimos 10 años, se construyen modelos de predicción de afluencia y se generan clusters de perfiles/itinerarios para entender mejor los flujos.

## Objetivos
- Limpiar y unificar los registros históricos de peregrinos de 2010‑2023.
- Predecir la afluencia diaria/semanal usando modelos de series temporales / XGBoost.
- Agrupar peregrinos y recorridos para identificar patrones de comportamiento.
- Dejar reproducible el flujo de trabajo mediante notebooks y datos versionados.

## Datos
- `data/raw/2010.xlsx` … `data/raw/2022.xlsx`: series históricas en bruto (diarias) por año.
- `data/peregrinos_para_prophet.csv`: serie temporal lista para modelar (`ds`, `y`).
- `data/prevision_prophet*.csv`, `data/prediction_oneweek.csv`: predicciones generadas con Prophet y XGBoost.
- `data/itinerario*.csv`, `data/itinererio_*`: rutas y etapas consolidadas para clusterización.
- `data/clust_generado_0.csv`: asignaciones de cluster a orígenes/fechas.
- `models/`: artefactos entrenados (`model_XGB.json`, `clust_mundial_model.joblib`, etc.).
- `reports/output_total.html`: visualización exportada con los resultados.

## Estructura del repositorio
- `notebooks/`: experimentos principales (`Prophet.ipynb`, `XGBoost.ipynb`, `Cluster_mundial.ipynb`, `Cluster espana.ipynb`, `Data_prepro*.ipynb`, etc.).
- `data/`: datos crudos, intermedios y derivados.
- `models/`: modelos entrenados y evaluaciones de clustering.
- `reports/`: salidas analíticas renderizadas.
- `src/`: reservado para código productivo (actualmente vacío).

## Flujo de trabajo
1) **Preprocesado**  
   - Unificación de Excel anuales (`data/raw`) y depuración en `Data_prepro*.ipynb`.  
   - Generación de la serie temporal limpia `data/peregrinos_para_prophet.csv` y de rutas itinerario.

2) **Predicción de afluencia**  
   - `notebooks/Prophet.ipynb`: modelo Prophet con festivos específicos (Año Xacobeo, Semana Santa, confinamiento, etc.), produce `data/prevision_prophet_f.csv`.  
   - `notebooks/XGBoost.ipynb`: modelo de gradiente boosting como referencia; serializa el modelo en `models/model_XGB.json` y pronósticos semanales.

3) **Clusterización de peregrinos/itinerarios**  
   - `notebooks/Cluster_mundial.ipynb` y `Cluster espana.ipynb`: KMeans sobre variables de origen, profesión y rutas consolidadas.  
   - Resultados exportados a `data/clust_generado_0.csv` y `data/itinerario_desglosado_cluster.csv`; modelo guardado en `models/clust_mundial_model.joblib`.

4) **Reportes**  
   - Visualizaciones y tablas finales en `reports/output_total.html` y CSVs derivados en `data/`.

## Cómo reproducir
1. Crear entorno:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Abrir Jupyter y ejecutar los notebooks en este orden recomendado:
   - `Data_prepro.ipynb` (o `Data_prepro-Spain-EDA.ipynb`) para generar insumos limpios.
   - `Prophet.ipynb` y `XGBoost.ipynb` para entrenar y exportar predicciones.
   - `Cluster_mundial.ipynb` / `Cluster espana.ipynb` para recalcular clusters.
3. Los outputs se guardan automáticamente en `data/` y `models/`. Ajusta rutas si ejecutas desde otra ubicación.

## Notas
- Los CSV intermedios pesados y algunos datos tratados no están en control de versiones (ver `.gitignore`), por lo que pueden necesitar regenerarse desde los Excel en `data/raw/`.
- El directorio `src/` queda libre para portar el código de los notebooks a scripts reutilizables.
