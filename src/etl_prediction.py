import logging
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent  # sube desde src/ al raíz
RAW_DIR = ROOT / "data" / "raw"
OUTPUT_CSV = ROOT / "data" / "interim" / "data_ds_y.csv"

DATE_COL = "Fecha"
COUNT_COL = "Edad"


def load_one_excel(path: Path) -> pd.DataFrame:
    df = pd.read_excel(path, usecols=[DATE_COL, COUNT_COL])
    lower_cols = {c.lower(): c for c in df.columns}
    date_col = lower_cols.get(DATE_COL.lower())
    count_col = lower_cols.get(COUNT_COL.lower())
    if not date_col or not count_col:
        raise ValueError(f"Faltan columnas {DATE_COL}/{COUNT_COL} en {path.name}: {df.columns.tolist()}")
    out = df[[date_col, count_col]].rename(columns={date_col: "ds", count_col: "y"})
    out["ds"] = pd.to_datetime(out["ds"]).dt.normalize() 
    out["y"] = pd.to_numeric(out["y"], errors="coerce")
    out = out.dropna(subset=["ds", "y"])
    out = out.groupby("ds", as_index=False)["y"].count()
    logging.info("Cargando archivo: %s (filas: %s)", path.name, len(out))
    return out


def build_dataset():
    files = sorted(RAW_DIR.glob("*.xlsx"))
    if not files:
        raise FileNotFoundError(f"No hay Excel en {RAW_DIR}")
    logging.info("Encontrados %s archivos en %s", len(files), RAW_DIR)
    frames = [load_one_excel(f) for f in files]
    df = pd.concat(frames, ignore_index=True).sort_values("ds")
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_CSV, index=False)
    logging.info("Guardado %s filas en %s", len(df), OUTPUT_CSV)
    return df


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")
    df = build_dataset()
