# Pipeline de datos — `caminito`

> Reconstrucción del flujo real de datos del proyecto (auditoría de los notebooks,
> datos y modelos). Sirve para saber qué notebook produce qué, en qué orden se ejecuta
> la cadena productiva, y qué archivos son fuente de verdad vs. derivados.

## Diagrama del pipeline

```
                        data/raw/2010..2022.xlsx  (Excel anuales crudos — FUENTE DE VERDAD)
                           │
          ┌────────────────┴───────────────────────────┐
          │ (rama SERIE TEMPORAL)                       │ (rama PERFILES)
          ▼                                             ▼
  src/etl_prediction.py                        Data_prepro.ipynb  [PRODUCTIVO]
          │                                     (limpieza + one-hot + PCA + KMeans)
          ▼                                             │
  data/interim/data_ds_y.csv                            ├─► Treated_csv/entries_all.csv
          │  (curado/renombrado manual)                 ├─► models/clust_mundial_model.joblib
          ▼                                             ├─► entries_all_with_labels.csv
  data/peregrinos_para_prophet.csv (ds,y)               └─► entries_with_labels_fin.csv ─┐
          │                                                                             │
   ┌──────┴───────┐        (exploratorios superados por Data_prepro:                    │
   ▼              ▼         Cluster_mundial / Cluster (1) / Cluster espana)             │
Prophet.ipynb   XGBoost.ipynb  [PRODUCTIVO]                                             │
[PRODUCTIVO]      │  ├─ lee prevision_prophet_f.csv (generado EXTERNAMENTE)             │
 forecast en      │  ├─► models/model_XGB.json                                          │
 memoria          │  └─► data/prediction_oneweek.csv ─────┐                             │
 (no escribe CSV) │                                        ▼                            ▼
                  │                          Generar perfiles futuros.ipynb  [PRODUCTIVO]
                  │                          (+ Caminos con etapas 2.xlsx)
                  │                                        │
                  │                                        ├─► data/clust_generado_0.csv
                  │                                        └─► data/origenes_generados.csv
                  │                                                    │ (renombrado manual → peres_futu.csv)
                  │                                                    ▼
                  │                          Peregrinos_futuro.ipynb  [PRODUCTIVO]
                  │                          (+ Caminos con etapas 2.xlsx)
                  │                                        ├─► data/itinerario_s.csv
                  │                                        ├─► data/itinererio_corregido_final.csv
                  │                                        ├─► data/itinererio_powerbi_final.csv  ◄── OUTPUT Power BI
                  │                                        └─► data/itinerario_desglosado_cluster.csv
                  │                                                    │
                  ▼                                                    ▼
          (comparación Prophet vs XGBoost)          melted.ipynb  [export Power BI]
                                                    └─► processed/melted_con_long.xlsx  ◄── OUTPUT Power BI
                                                       processed/iti_melted_PowerBI.xlsx
                                                                       │
                                                                       ▼
                                                              Power BI / reports (viz temporal de flujos)
```

## Cadena productiva mínima (orden de ejecución real)

1. `src/etl_prediction.py` → `data/interim/data_ds_y.csv` → (curado) `data/peregrinos_para_prophet.csv`
2. `Data_prepro.ipynb` → `entries_with_labels_fin.csv` + `models/clust_mundial_model.joblib`
3. `Prophet.ipynb` (+ `prevision_prophet_f.csv`) y `XGBoost.ipynb` → `models/model_XGB.json`, `data/prediction_oneweek.csv`
4. `Generar perfiles futuros.ipynb` → `data/clust_generado_0.csv`, `data/origenes_generados.csv`
5. `Peregrinos_futuro.ipynb` → `data/itinererio_powerbi_final.csv` + `data/itinerario_desglosado_cluster.csv`
6. `melted.ipynb` → `processed/melted_con_long.xlsx` (Power BI)

## Clasificación de notebooks

| Notebook | Propósito | Clasificación | Inputs | Outputs |
|---|---|---|---|---|
| **Data_prepro.ipynb** | Núcleo de preprocesado + clustering mundial: unifica Excel anuales, limpieza, one-hot, PCA, KMeans de perfiles | **PRODUCTIVO** | `raw_csv_per_year/*`, `Caminos con etapas 2.xlsx` | `Treated_csv/entries_all.csv`, `entries_all_with_labels.csv`, `PCA_Mundial.csv`, `clust_mundial.csv`, `entries_with_labels_fin.csv`, `models/clust_mundial_model.joblib` |
| **XGBoost.ipynb** | XGBRegressor de afluencia (predicción principal aguas abajo); train/test, RMSE, pronóstico semanal | **PRODUCTIVO** | `peregrinos_para_prophet.csv`, `prevision_prophet_f.csv` | `models/model_XGB.json`, `data/prediction_oneweek.csv` |
| **Prophet.ipynb** | Serie temporal Prophet con festivos (Xacobeo, Semana Santa, confinamiento) | **PRODUCTIVO** (forecast en memoria; **no** hace `to_csv`) | `peregrinos_para_prophet.csv` | Forecast en memoria / plots |
| **Generar perfiles futuros.ipynb** | Genera peregrinos futuros según predicción + distribución de perfiles por cluster | **PRODUCTIVO** | `prediction_oneweek.csv`, `entries_with_labels_fin.csv`, `Caminos con etapas 2.xlsx` | `clust_generado_0.csv`, `origenes_generados.csv` |
| **Peregrinos_futuro.ipynb** | Construye itinerarios/etapas de peregrinos futuros y prepara export Power BI | **PRODUCTIVO** | `peres_futu.csv`, `Caminos con etapas 2.xlsx` | `itinerario_s.csv`, `itinererio_corregido_final.csv`, `itinererio_powerbi_final.csv`, `itinerario_desglosado_cluster.csv` |
| **melted.ipynb** | Reshape/melt de itinerarios y perfiles a formato largo para Power BI | **PRODUCTIVO-auxiliar** (algo desordenado) | `iti_melted_PowerBI.xlsx`, `melted_con_long.xlsx`, `entries_with_labels_fin.csv` | `melted_con_long.xlsx` |
| **Data_prepro-Spain-EDA.ipynb** | Gemelo EDA (España) del prepro: mismo núcleo + gráficas masivas | **EXPLORATORIO** | Excel crudos (⚠ ruta absoluta Windows `C:/Users/.../TFM/DATA`) | `Treated_csv/entries_all.csv` |
| **Cluster_mundial.ipynb** | KMeans(3) sobre origen/profesión + geocoding | **EXPLORATORIO** (superado por Data_prepro) | `Treated_csv/entries_all.csv` | `origen.csv` |
| **Cluster espana.ipynb** | Clustering KMeans(3) del subconjunto España | **EXPLORATORIO** (sin outputs) | `entries_all.csv` | — |
| **Cluster (1).ipynb** | Variante/duplicado de Cluster_mundial (geocoding + KMeans) | **DESCARTABLE** (duplicado) | `Treated_csv/entries_all.csv`, `origin_all.csv` | `origen.csv`, `origin_all.csv` |
| **Untitled.ipynb** | Scratch: inspección de tablas Origen/Profesión/Cluster | **DESCARTABLE** | `entries_with_labels_fin.csv` | — |
| **ver_excels.ipynb** | Comprobación rápida de dos Excel crudos | **DESCARTABLE** | `../data/raw/2018.xlsx`, `2019.xlsx` | — |
| **Predict-all.ipynb** | Vacío | **DESCARTABLE** | — | — |

## Linaje de datos

- **RAW (fuente de verdad):** `data/raw/2010.xlsx` … `2022.xlsx` (13 archivos, ~178 MB) —
  registros anuales de peregrinos (Oficina del Peregrino). Tablas de referencia curadas:
  `data/processed/Caminos con etapas 2.xlsx` (Camino/Etapa/Ciudad/km), `data/origen.csv`.
- **INTERIM (derivados intermedios):** `data/interim/data_ds_y.csv`,
  `data/peregrinos_para_prophet.csv`, `data/itinerario*.csv`, `data/clust_generado_0.csv`,
  `data/origenes_generados.csv`, `data/peres_futu.csv`, `data/prevision_prophet*.csv`.
- **OUTPUT (Power BI / futura web):** `data/itinererio_powerbi_final.csv`,
  `data/processed/melted_con_long.xlsx`, `data/processed/iti_melted_PowerBI.xlsx`,
  `data/prevision_prophet_f.csv`, `data/prediction_oneweek.csv`.
- **Modelos (versionados en git):** `models/model_XGB.json` (XGBoost, 4.7 MB),
  `models/clust_mundial_model.joblib` (KMeans, 11.9 MB). Prophet **no** se persiste como
  binario; solo sus salidas CSV.

## Datos y reproducibilidad ⚠

- **Todo `data/` está fuera de git** por las reglas `*.csv` / `*.xlsx` de `.gitignore`.
  Solo se versionan los 2 modelos de `models/`.
- Los 13 Excel raw (fuente de verdad) **no están en el repo** ni respaldados en control de
  versiones. **Deben respaldarse manualmente** (Drive/disco externo). Sin ellos, quien clone
  el repo obtiene los modelos pero **ningún dato**, y hay que regenerar toda la cadena `data/`.
- Origen de los datos raw: registros de la **Oficina del Peregrino** de Santiago (2010–2022).

## Cabos sueltos conocidos

- `prevision_prophet_f.csv` lo **consume** `XGBoost.ipynb` pero **ningún notebook lo escribe**
  (Prophet no hace `to_csv`); se genera manualmente/externamente desde el forecast de Prophet.
- El paso `origenes_generados.csv` → `peres_futu.csv` es un **renombrado manual**, no un
  traspaso en código.
- Rutas relativas al cwd de cada notebook (`Treated_csv/...` sin prefijo `data/`) y una ruta
  **absoluta de Windows** en `Data_prepro-Spain-EDA.ipynb` → rompen reproducibilidad fuera de
  la máquina original.
- Duplicados de datos: `data/itinerario.csv` ≈ `data/itinerario_s.csv` (mismo tamaño);
  `data/prevision_prophet.csv` (cruda) vs `data/prevision_prophet_f.csv` (final).
- `data/interim/Treated_csv/` y `tmp/gitfilter/` existen vacías; `tmp/.DS_Store` está
  versionado por error (debería salir de git en una fase de higiene).
