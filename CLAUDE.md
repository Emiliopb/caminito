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
cruce de su BBDD de clientes con los flujos → palancas de revenue).

**Marca del producto: `Stellae.ai`** (Compostela = *campus stellae*, campo de estrellas).

**Mensaje al cliente (importante):** a la pyme **no le interesa cómo se investigaron los
datos**. No se vende "el mejor forecast de peregrinos"; se vende *"te ayudo a encontrar
palancas de crecimiento y revenue"*. El dato y el mapa son el **gancho/prueba**. Todo en
**español**, tono consultor a dueño de pyme, sin jerga de data science.

## 👉 Estado actual y siguiente paso

**Hecho (Fase 1):** MVP web entregado en `web/` — one-pager de consultor con mapa animado
de flujos (canvas, self-contained) + la palanca de revenue de Sarria. Estéticamente
aprobado por el usuario.

**Siguiente paso: productivizar ese mock-up.** Detalle y orden en `@docs/ROADMAP.md`
(Fase 1.5). En corto: (1) responsive verificado en móvil real, (2) botón de contacto que
funcione, (3) deploy público, y después (4) reconstruir los datos de **un año completo**
(hoy la web solo cubre 40 días: 1 jun – 10 jul).

## Comandos

```bash
# Entorno
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt        # ⚠ incompleto: falta streamlit

# WEB (lo vivo del proyecto): regenera web/index.html desde los datos
python web/build.py

# ETL (único script productivo): data/raw/*.xlsx → data/interim/data_ds_y.csv
python src/etl_prediction.py

# App Streamlit: stub abandonado, NO se usa (la web es web/)
streamlit run app/app.py

# Notebooks
jupyter notebook
```

## Estructura

- `web/` — **el producto** (Stellae.ai). `template.html` = diseño y textos (se edita aquí);
  `build.py` = datos + cifras; `index.html` = **generado, no editar a mano**.
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
- `requirements.txt`: ya incluye `openpyxl` (lo necesita `web/build.py`); sigue faltando
  `streamlit`, pero el stub de Streamlit está **abandonado** y no es prioridad.
- **La web solo cubre 40 días** (1 jun – 10 jul), no un año: es la ventana que traen los
  datos ya reconstruidos. Ampliarlo a un año completo es tarea de datos, no de front.
- El **año 2026 es solo una etiqueta** (`ANIO_DEMO` en `web/build.py`); el dato real es de
  2023. Cambiarlo no recalcula ninguna predicción.
- Los **Perfiles A/B/C** de la web son los clusters 0/1/2 sin significado demográfico
  recuperado todavía (se sabe que se reparten por ruta: A/C ≈ Francés, B ≈ Portugués).
- `Data_prepro-Spain-EDA.ipynb` tiene una **ruta absoluta de Windows** que rompe reproducibilidad.
- El pipeline vive mayormente en notebooks con renombrados/pasos manuales; ver cabos sueltos
  en `docs/PIPELINE.md` antes de asumir que la cadena corre sola.

## Cómo trabajar aquí

- Usa **plan mode** para tareas no triviales (multi-archivo o de enfoque incierto).
- Da siempre una forma de **verificar** el trabajo (ejecutar, comparar output).
- No hacer commits ni cambios destructivos sin pedirlo.
- Antes de recomendar un archivo/función de este doc, verifica que sigue existiendo.
