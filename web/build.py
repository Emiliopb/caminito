#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build.py — Generador de la web self-contained de Camino Insights.

Lee los datos ya reconstruidos (data/processed/melted_con_long.xlsx) y el orden de
etapas (data/Caminos_con_etapas_2.csv), agrega los flujos de peregrinos por
fecha/ciudad/perfil, calcula las cifras de la "palanca" para la zona ejemplo y
lo inyecta en web/template.html -> web/index.html (una sola página, sin dependencias).

El dataset real es jun-jul 2023; se PRESENTA como 2026 (solo cambia la etiqueta de año).

Uso:
    python web/build.py
"""
import json
import os
import re
import unicodedata
from datetime import datetime

import pandas as pd

# --- Rutas -------------------------------------------------------------------
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XLSX = os.path.join(ROOT, "data", "processed", "melted_con_long.xlsx")
ETAPAS = os.path.join(ROOT, "data", "Caminos_con_etapas_2.csv")
TEMPLATE = os.path.join(ROOT, "web", "template.html")
OUTPUT = os.path.join(ROOT, "web", "index.html")

# --- Config del demo ---------------------------------------------------------
ANIO_DEMO = 2026          # año con el que se presenta (el dato real es 2023)
ZONA_EJEMPLO = "Sarria"   # zona protagonista de la palanca

# Coordenadas correctas para las 3 ciudades con geocoding sucio (fuera de Iberia).
COORDS_FIX = {
    "roncesvalles": (43.0092, -1.3193),
    "abadin": (43.3656, -7.4783),
    "la caridad": (43.5519, -6.8419),
}

# bbox Península (para descartar cualquier resto de geocoding sucio).
BBOX = dict(lat_min=36.0, lat_max=44.0, lng_min=-9.6, lng_max=-1.0)


def norm(s: str) -> str:
    """Normaliza nombre de ciudad: sin acentos, minúsculas, sin espacios extra."""
    s = str(s).strip().lower()
    s = "".join(c for c in unicodedata.normalize("NFD", s)
                if unicodedata.category(c) != "Mn")
    s = re.sub(r"\s+", " ", s)
    return s


def main():
    # --- Cargar flujos -------------------------------------------------------
    m = pd.read_excel(XLSX)
    m = m.rename(columns={"index": "fecha", "Cluster": "perfil",
                          "Latitud": "lat", "Longitud": "lng"})
    m["fecha"] = pd.to_datetime(m["fecha"])
    m["ciudad"] = m["ciudad"].astype(str).str.strip()
    m["cnorm"] = m["ciudad"].map(norm)
    m["frecuencia"] = m["frecuencia"].fillna(0).astype(float)

    # Corregir las 3 coords sucias
    for key, (la, lo) in COORDS_FIX.items():
        mask = m["cnorm"] == key
        m.loc[mask, "lat"] = la
        m.loc[mask, "lng"] = lo

    # Descartar cualquier resto fuera de bbox (no debería quedar nada tras el fix)
    fuera = ~(m["lat"].between(BBOX["lat_min"], BBOX["lat_max"]) &
             m["lng"].between(BBOX["lng_min"], BBOX["lng_max"]))
    if fuera.any():
        print(f"  aviso: descarto {int(fuera.sum())} filas aún fuera de bbox: "
              f"{sorted(m.loc[fuera, 'ciudad'].unique())}")
    m = m[~fuera].copy()

    # --- Registro de ciudades (coord representativa por ciudad) --------------
    coords = (m.groupby("ciudad")
                .agg(lat=("lat", "median"), lng=("lng", "median"),
                     cnorm=("cnorm", "first"))
                .reset_index())
    coords = coords.sort_values("ciudad").reset_index(drop=True)
    coords["id"] = coords.index
    id_por_norm = dict(zip(coords["cnorm"], coords["id"]))

    ciudades = [
        {"id": int(r.id), "nombre": r.ciudad,
         "lat": round(float(r.lat), 5), "lng": round(float(r.lng), 5)}
        for r in coords.itertuples()
    ]

    # --- Fechas (re-etiquetadas a ANIO_DEMO) ---------------------------------
    fechas = sorted(m["fecha"].unique())
    def etiqueta(dt64):
        d = pd.Timestamp(dt64)
        return f"{ANIO_DEMO:04d}-{d.month:02d}-{d.day:02d}"
    fechas_lbl = [etiqueta(f) for f in fechas]

    # --- Frames: por fecha, {ciudadId: [f0, f1, f2]} -------------------------
    id_por_ciudad = dict(zip(coords["ciudad"], coords["id"]))
    frames = []
    for f, lbl in zip(fechas, fechas_lbl):
        sub = m[m["fecha"] == f]
        acc = {}
        for r in sub.itertuples():
            cid = id_por_ciudad[r.ciudad]
            arr = acc.setdefault(cid, [0, 0, 0])
            p = int(r.perfil)
            if 0 <= p <= 2:
                arr[p] += int(round(r.frecuencia))
        # omitir ciudades sin nadie ese día
        c = {str(cid): v for cid, v in acc.items() if sum(v) > 0}
        frames.append({"d": lbl, "c": c})

    # --- Rutas (polilíneas por Camino, desde etapas) -------------------------
    et = pd.read_csv(ETAPAS, sep=";")
    et.columns = [c.strip() for c in et.columns]
    et["cnorm"] = et["Ciudad"].map(norm)
    rutas = []
    for camino, grp in et.groupby("Camino"):
        grp = grp.sort_values("Etapa", ascending=False)  # inicio -> Santiago
        seq = [int(id_por_norm[cn]) for cn in grp["cnorm"] if cn in id_por_norm]
        # deduplicar consecutivos conservando orden
        limpio = [x for i, x in enumerate(seq) if i == 0 or x != seq[i - 1]]
        if len(limpio) >= 2:
            rutas.append({"camino": str(camino).strip(), "ids": limpio})

    # --- Palanca (zona ejemplo) ----------------------------------------------
    z = m[m["ciudad"].map(norm) == norm(ZONA_EJEMPLO)]
    total = float(z["frecuencia"].sum())
    por_dia = z.groupby("fecha")["frecuencia"].sum()
    media = float(por_dia.mean())
    pico = float(por_dia.max())
    pico_fecha = pd.Timestamp(por_dia.idxmax())
    ratio_pico = round(pico / media, 1) if media else 0
    por_sem = z.copy()
    por_sem["semana"] = por_sem["fecha"].dt.isocalendar().week
    sem = por_sem.groupby("semana")["frecuencia"].sum().sort_values(ascending=False)
    pct_semana_pico = int(round(sem.iloc[0] / total * 100)) if total else 0
    mix = z.groupby("perfil")["frecuencia"].sum()
    mix_pct = {str(int(k)): int(round(v / mix.sum() * 100)) for k, v in mix.items()}

    zona_id = id_por_norm.get(norm(ZONA_EJEMPLO))
    palanca = {
        "zona": ZONA_EJEMPLO,
        "zonaId": int(zona_id) if zona_id is not None else None,
        "total": int(round(total)),
        "media": int(round(media)),
        "pico": int(round(pico)),
        "picoFecha": f"{ANIO_DEMO:04d}-{pico_fecha.month:02d}-{pico_fecha.day:02d}",
        "ratioPico": ratio_pico,
        "pctSemanaPico": pct_semana_pico,
        "mixPerfil": mix_pct,
    }

    # --- Ensamblar payload ---------------------------------------------------
    data = {
        "meta": {"marca": "Stellae.ai", "anio": ANIO_DEMO, "zona": ZONA_EJEMPLO},
        "ciudades": ciudades,
        "rutas": rutas,
        "frames": frames,
        "palanca": palanca,
    }

    # --- Inyectar en template ------------------------------------------------
    with open(TEMPLATE, "r", encoding="utf-8") as fh:
        html = fh.read()
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    if "__CAMINO_DATA__" not in html:
        raise SystemExit("El template no contiene el placeholder __CAMINO_DATA__")
    html = html.replace("__CAMINO_DATA__", payload)
    with open(OUTPUT, "w", encoding="utf-8") as fh:
        fh.write(html)

    # --- Log de verificación -------------------------------------------------
    print("web/index.html generado.")
    print(f"  fechas: {len(fechas)} ({fechas_lbl[0]} -> {fechas_lbl[-1]})")
    print(f"  ciudades: {len(ciudades)} | rutas: {len(rutas)} "
          f"| frames: {len(frames)} | payload: {len(payload)/1024:.0f} KB")
    print(f"  palanca {ZONA_EJEMPLO}: total={palanca['total']} media={palanca['media']} "
          f"pico={palanca['pico']} (x{palanca['ratioPico']}) "
          f"semana_pico={palanca['pctSemanaPico']}% mix={palanca['mixPerfil']}")
    # sanity clusters global
    glob = m.groupby("perfil")["frecuencia"].sum().to_dict()
    print(f"  sanity mix global: "
          f"{{0:{glob.get(0,0):.0f}, 1:{glob.get(1,0):.0f}, 2:{glob.get(2,0):.0f}}}")


if __name__ == "__main__":
    main()
