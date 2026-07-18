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

## Fase 1 — MVP web ✅ ENTREGADO

**Resultado:** `web/` — one-pager de consultor (**Stellae.ai**), en español, cuyo
protagonista es una **palanca de revenue** y donde el mapa animado es la prueba visual.
Estética aprobada por el usuario.

- **Stack:** página self-contained (canvas 2D a mano, sin dependencias ni tiles externos).
  Descartado Streamlit (estética de herramienta de datos); Next.js aplazado.
- **Concepto visual:** *campus stellae* — cielo nocturno sobre el Camino, peregrinos como
  estrellas que convergen en Santiago. Acento = la flecha amarilla del Camino.
- **La palanca (Sarria):** 6.028 peregrinos, pico ×6,9 sobre el día medio, **64 % del flujo
  en una sola semana** → pricing dinámico, capacidad para el pico, marketing al perfil que
  realmente pasa.
- **Generación:** `python web/build.py` (datos + cifras → inyecta en `template.html`).

---

## Fase 1.5 — Productivizar el mock-up 🎯 PRÓXIMO HITO

**Objetivo:** pasar de "mock-up precioso" a algo que se pueda mandar por WhatsApp a un
cliente sin sonrojarse.

1. **Responsive de verdad** — el CSS es responsive pero **nunca se ha verificado en un
   móvil real**, y el mapa (canvas) es la parte delicada en pantalla estrecha. Es el punto
   más urgente: los clientes abrirán el enlace desde el teléfono.
2. **Botón de contacto que funcione** — hoy el CTA es un `mailto:` a una dirección
   inventada (`hola@stellae.ai`). Sustituir por algo real y simple: correo del usuario,
   WhatsApp (`wa.me/<número>`) o un formulario sencillo. No hace falta complicarlo.
3. **Deploy público** — la web es un único HTML autocontenido, así que basta hosting
   estático. Opción rápida: Netlify Drop. Opción "seria": GitHub Pages / dominio propio.
   ⚠️ Cualquiera deja la web accesible a quien tenga el enlace.

---

## Fase 1.6 — Datos de un año completo

**Problema:** la web solo cubre **40 días (1 jun – 10 jul)**, que es la ventana de los datos
ya reconstruidos. Para vender estacionalidad hace falta **el año entero**: el argumento
"tu demanda es una ola" se sostiene mucho mejor con temporada alta *y* baja.

**Entregables:** reconstruir los flujos (fecha · ciudad · perfil) para un año completo,
idealmente ya con un pipeline reproducible en `src/` en vez de la cadena manual de
notebooks (ver Fase 2, que en la práctica se solapa con esto).

**Bonus de alto valor:** recuperar el **significado demográfico de los Perfiles A/B/C**
(nacionalidad, edad). Hoy la palanca de marketing dice "el peregrino del Francés, no el del
Portugués"; con la demografía real diría *"el alemán de 55+ que no estás captando"* — mucho
más vendible.

---

## Fase 1 (original) — MVP web (rápido) — histórico

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
