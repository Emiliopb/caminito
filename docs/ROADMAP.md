# Roadmap — `caminito`

> Plan por fases para convertir el repo de TFM en un producto de datos.
> **Norte:** llegar a un **MVP web cuanto antes** (aunque el pipeline siga en notebooks),
> para poder enseñarlo pronto a comercios del Camino.

## Visión de producto

Web profesional para comercios del Camino (hoteles, albergues, restaurantes, tiendas)
que muestre **qué peregrinos pasan/pasarán por su zona y cuándo**. El dato es la excusa
comercial; el negocio real es **vender consultoría** y relación con esos comercios,
culminando en el cruce de su BBDD de clientes con los flujos de peregrinos para levantar
**palancas de revenue**.

---

## Fase 0 — Cimientos documentales ✅ (en curso)

**Objetivo:** dejar por escrito la foto del proyecto y el rumbo. 100% documental, sin tocar
código ni datos.

**Entregables:**
- `CLAUDE.md` — contexto persistente para cada sesión.
- `docs/PIPELINE.md` — mapa reconstruido del pipeline (notebooks, I/O, linaje de datos).
- `docs/ROADMAP.md` — este documento.

**Decisiones fijadas:**
- Datos raw: se documentan y se respaldan **manualmente** (sin DVC/LFS por ahora).
- Prioridad: **MVP web** por delante de la productivización completa del pipeline.

---

## Fase 1 — MVP web (rápido) 🎯 próximo hito

**Objetivo:** una web con look & feel profesional que visualice los flujos de peregrinos por
punto del Camino a lo largo del tiempo — replicando/mejorando lo que hoy se hace en Power BI,
pero **consumiendo los outputs que YA existen** (sin reconstruir el pipeline).

**Entradas disponibles (ya generadas):**
- `data/itinererio_powerbi_final.csv`
- `data/processed/melted_con_long.xlsx` (formato largo con lat/long)

**Entregables:**
- Web que, dada una fecha futura, muestre por ciudad/etapa del Camino cuántos peregrinos hay
  y de qué perfil (cluster), y cómo se mueven en el tiempo.
- Look profesional (base sobre la que enseñar a un comercio).

**Decisiones abiertas:**
- **Stack** — Streamlit (rápido, ya hay stub en `app/app.py`) vs. web "pro"
  (Next.js/React + API) vs. dashboard embebido. A decidir al entrar en la fase.
- Alojamiento/deploy (local demo vs. público).
- Nivel de interactividad del mapa temporal.

**Notas:** completar `requirements.txt` con `streamlit` y `openpyxl` (hoy faltan) forma parte
del arranque de esta fase.

---

## Fase 2 — Pipeline reproducible

**Objetivo:** poder regenerar los datos de la web sin depender de notebooks manuales.

**Entregables:**
- Portar la cadena productiva (ver `docs/PIPELINE.md`) de notebooks a módulos en `src/`.
- Cerrar cabos sueltos: productor real de `prevision_prophet_f.csv`; eliminar el renombrado
  manual `origenes_generados.csv` → `peres_futu.csv`; rutas robustas (sin rutas Windows).
- Higiene de repo: quitar `tmp/.DS_Store` de git, borrar notebooks descartables, deduplicar
  datos, `requirements.txt` completo.
- (Opcional) tests mínimos del ETL y estructura de proyecto Python estándar.

---

## Fase 3 — Vista por comercio / zona

**Objetivo:** que un comercio concreto vea "lo suyo".

**Entregables:**
- Filtrado de flujos y perfiles por punto concreto del Camino (Astorga, Sarria, Bayona…):
  qué segmentos de peregrinos pasan, en qué volumen y estacionalidad.
- Ficha/vista por comercio con esos indicadores.

---

## Fase 4 — Cruce con BBDD del comercio → palancas de revenue

**Objetivo:** la feature final, la excusa de dato para la consultoría.

**Entregables:**
- El comercio aporta su BBDD de clientes; se cruza con los flujos de peregrinos de su zona.
- Detección de segmentos **no captados** (p. ej. "pasan peregrinos alemanes que no estás
  captando") y recomendaciones/palancas comerciales.

**Consideraciones:** privacidad y tratamiento de datos de terceros (BBDD de clientes del
comercio) — a definir con cuidado antes de construir.

---

## Riesgos y decisiones transversales

- **Reproducibilidad de datos:** los Excel raw (~178 MB) están fuera de git; dependemos de
  un backup manual. Revisar DVC/LFS si el proyecto crece (pospuesto desde Fase 0).
- **Deuda técnica de notebooks:** mientras el pipeline siga en notebooks (Fases 0–1), cada
  regeneración de datos es manual y frágil. La Fase 2 salda esta deuda.
- **Elección de stack web** (Fase 1): condiciona el resto del producto; decidir pronto.
