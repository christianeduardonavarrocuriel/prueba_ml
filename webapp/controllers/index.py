import web
import csv
import io

render = web.template.render("webapp/views", base="template")

class Index:
    
    def __init__(self) -> None:
        pass
    
    def GET(self):
        return render.index() # type: ignore
    
    def POST(self):
        formulario = web.input(archivo_csv={})
        
        if "archivo_csv" in formulario:
            
            archivo = formulario["archivo_csv"]
        
            nombre_archivo = archivo.filename
            
            contenido_bytes = archivo.file.read()
            contenido_texto = contenido_bytes.decode("utf-8")
            
            leer_csv = csv.reader(io.StringIO(contenido_texto))
            filas = list(leer_csv)
            
            respuesta = f"Archivo {nombre_archivo} recibido. Filas: {len(filas)}"
            
            #ruta_archivo = f"static/csv/{nombre_archivo}"
            ruta_archivo = f"static/csv/datos.csv"
            
            with open(ruta_archivo, mode="w", newline="",encoding="utf-8") as archivo:
                escritor= csv.writer(archivo)
                escritor.writerows(filas)
            
            return respuesta
        else:
            return "No se puede procesar el archivo"