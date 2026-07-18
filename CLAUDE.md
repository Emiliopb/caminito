# CLAUDE.md

Contexto persistente para trabajar en este repo. Ver también `@README.md`,
`@docs/PIPELINE.md` (flujo real de datos) y `@docs/ROADMAP.md` (plan por fases).

## Qué es

TFM sobre peregrinos del Camino de Santiago: datos demográficos + rutas de 10 años →
clustering de perfiles + predicción de afluencia (XGBoost/Prophet) → dataset futuro de
flujos → export a Power BI.

**Objetivo de producto:** web profesional para comercios del Camino (hoteles, albergues,
restaurantes, tiendas) que muestre qué peregrinos pasan/pasarán por su zona y cuándo. El
dato es la excusa; el negocio real es **consultoría** con esos comercios (culmina en el
cruce de su BBDD de clientes con los flujos → palancas de revenue). Norte actual del
roadmap: **MVP web cuanto antes**.

## Comandos

```bash
# Entorno
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt        # ⚠ incompleto: faltan streamlit y openpyxl

# ETL (único script productivo): data/raw/*.xlsx → data/interim/data_ds_y.csv
python src/etl_prediction.py

# App (hoy solo un stub con el título)
streamlit run app/app.py

# Notebooks
jupyter notebook
```

## Estructura

- `notebooks/` — todo el trabajo real (productivo + EDA + scratch mezclados; ver PIPELINE.md).
- `src/` — código productivo (por ahora solo `etl_prediction.py`).
- `app/` — app Streamlit (stub).
- `data/` — datos crudos, intermedios y derivados (**fuera de git**).
- `models/` — artefactos entrenados (`model_XGB.json`, `clust_mundial_model.joblib`; **sí** en git).
- `docs/` — documentación del proyecto (PIPELINE, ROADMAP).

## Gotchas (lo no obvio)

- **`data/` está ignorado en git** (`*.csv` / `*.xlsx` en `.gitignore`). Solo se versionan
  los 2 modelos de `models/`.
- Los **Excel raw** (`data/raw/2010..2022.xlsx`, ~178 MB) son la **fuente de verdad** y **no
  están en el repo** ni respaldados por git → requieren **backup manual** (ver PIPELINE.md).
- `prevision_prophet_f.csv` lo consume `XGBoost.ipynb` pero **ningún notebook lo escribe**
  (Prophet no persiste a CSV): se genera externamente.
- `requirements.txt` está **incompleto**: faltan `streamlit` y `openpyxl` (pendiente en ROADMAP).
- `Data_prepro-Spain-EDA.ipynb` tiene una **ruta absoluta de Windows** que rompe reproducibilidad.
- El pipeline vive mayormente en notebooks con renombrados/pasos manuales; ver cabos sueltos
  en `docs/PIPELINE.md` antes de asumir que la cadena corre sola.

## Cómo trabajar aquí

- Usa **plan mode** para tareas no triviales (multi-archivo o de enfoque incierto).
- Da siempre una forma de **verificar** el trabajo (ejecutar, comparar output).
- No hacer commits ni cambios destructivos sin pedirlo.
- Antes de recomendar un archivo/función de este doc, verifica que sigue existiendo.
