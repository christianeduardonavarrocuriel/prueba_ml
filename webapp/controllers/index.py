import web
import csv
import io

import pandas as pd
import numpy as np

render = web.template.render("webapp/views", base="template")

class Index:
    
    def __init__(self) -> None:
        pass
    
    def info(self):
        ruta_archivo = f"static/csv/datos.csv"
        df = pd.read_csv(ruta_archivo)
        
        informacion = {
            "shape":df.shape,
            "dtype":df.dtypes,
        }
        
        return informacion

    def crear_informe(self, df):
        tipos = [(str(columna), str(df[columna].dtype)) for columna in df.columns]
        nulos = [(str(columna), int(df[columna].isna().sum())) for columna in df.columns]

        estadisticas = []
        modas = []
        columnas_numericas = df.select_dtypes(include=[np.number]).columns

        for columna in df.columns:
            valores_modales = df[columna].dropna().mode()
            if valores_modales.empty:
                moda = "Sin moda"
            else:
                moda = ", ".join(str(valor) for valor in valores_modales)
            modas.append((str(columna), moda))

        for columna in columnas_numericas:
            serie = df[columna].dropna()
            estadisticas.append({
                "columna": str(columna),
                "maximo": self.formatear_valor(serie.max()),
                "minimo": self.formatear_valor(serie.min()),
                "mediana": self.formatear_valor(serie.median()),
                "media": self.formatear_valor(serie.mean()),
                "desviacion": self.formatear_valor(serie.std()),
            })

        primeras_filas = df.head(5)
        ultimas_filas = df.tail(5)

        return {
            "filas": int(df.shape[0]),
            "columnas": int(df.shape[1]),
            "tipos": tipos,
            "nulos": nulos,
            "estadisticas": estadisticas,
            "modas": modas,
            "encabezados": [str(columna) for columna in df.columns],
            "primeras_filas": primeras_filas.fillna("").astype(object).values.tolist(),
            "ultimas_filas": ultimas_filas.fillna("").astype(object).values.tolist(),
        }

    def formatear_valor(self, valor):
        if pd.isna(valor):
            return "Sin datos"
        if isinstance(valor, (np.integer, int)):
            return str(int(valor))
        if isinstance(valor, (np.floating, float)):
            return f"{float(valor):.6f}".rstrip("0").rstrip(".")
        return str(valor)
        
    
    def GET(self):
        return render.index() # type: ignore
    
    def POST(self):
        formulario = web.input(archivo_csv={})
        
        if "archivo_csv" not in formulario:
            return "No se puede procesar el archivo"

        archivo = formulario["archivo_csv"]

        if not getattr(archivo, "filename", "").lower().endswith(".csv"):
            return render.resultado_tabla(
                error="El archivo seleccionado no tiene formato CSV.",
                encabezados=None,
            )

        try:
            contenido_bytes = archivo.file.read()
            if not contenido_bytes:
                return render.resultado_tabla(
                    error="El archivo CSV está vacío.",
                    encabezados=None,
                )

            contenido_texto = contenido_bytes.decode("utf-8-sig")
            df = pd.read_csv(io.StringIO(contenido_texto))

            if df.empty:
                return render.resultado_tabla(
                    error="El archivo CSV no contiene filas de datos.",
                    encabezados=None,
                )
            if df.columns.empty:
                return render.resultado_tabla(
                    error="El archivo CSV no contiene columnas.",
                    encabezados=None,
                )
            if df.columns.str.strip().eq("").any():
                return render.resultado_tabla(
                    error="El archivo CSV contiene encabezados vacíos.",
                    encabezados=None,
                )

            ruta_archivo = "static/csv/datos.csv"
            df.to_csv(ruta_archivo, index=False, encoding="utf-8")

            informe = self.crear_informe(df)
            return render.resultado_tabla(
                error=None,
                informe=informe,
                encabezados=informe["encabezados"],
            )
        except UnicodeDecodeError:
            return render.resultado_tabla(
                error="El archivo debe estar codificado como UTF-8.",
                encabezados=None,
            )
        except (pd.errors.EmptyDataError, pd.errors.ParserError, csv.Error):
            return render.resultado_tabla(
                error="No fue posible validar el formato del archivo CSV.",
                encabezados=None,
            )