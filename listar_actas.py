import sys
import glob, os
import codecs
import csv
from bs4 import BeautifulSoup as bs

actas = []

all_actas = []

def list_actas():
   os.chdir(".")
   for acta in glob.glob("*.acta"):
    actas.append(acta)

def load_actas():

  for acta in actas:
    ubigeo,colegio,nro_acta = (acta.replace(".html","")).split("_")
    f= codecs.open(acta, 'r')
    parse_acta(f.read(), ubigeo, colegio, nro_acta)

def clear_column(value):

  value = value.get_text()

  value = value.strip()

  return value

def parse_acta(output, ubigeo, colegio, nro_acta):

  html = bs(output, 'html.parser')
  acta_detalle = html.find("table", {"class": "table13"})
  
  mesa = clear_column(acta_detalle.select("tbody td:nth-child(1)")[0])
  n_copia = clear_column((acta_detalle.select("tbody td:nth-child(2)"))[0])

  acta_ubicacion = html.find("table", {"class": "table14"})
  departamento = clear_column(acta_ubicacion.select("tbody tr:nth-child(2) td:nth-child(1)")[0])
  provincia = clear_column(acta_ubicacion.select("tbody tr:nth-child(2) td:nth-child(2)")[0])
  distrito = clear_column(acta_ubicacion.select("tbody tr:nth-child(2) td:nth-child(3)")[0])
  local_votacion = clear_column(acta_ubicacion.select("tbody tr:nth-child(2) td:nth-child(4)")[0])
  direccion = clear_column(acta_ubicacion.select("tbody tr:nth-child(2) td:nth-child(5)")[0])
  
  acta_informacion = html.find("table", {"class": "table15"})
  electores_habiles = clear_column(acta_informacion.select("tbody tr:nth-child(2) td:nth-child(1)")[0])
  total_votantes = clear_column(acta_informacion.select("tbody tr:nth-child(2) td:nth-child(2)")[0])
  estado_acta = clear_column(acta_informacion.select("tbody tr:nth-child(2) td:nth-child(3)")[0])

  lista_congreso = html.find("table", {"class": "table06_acta_congreso"})

  if(lista_congreso):

    partidos_votos = lista_congreso.find_all("tr")
  
    del partidos_votos[0]

    for votos in partidos_votos:
      partido = votos.find("td",{"class","ancho_acta_congreso_autoridad"})
      if(partido):
        partido = (partido.get_text()).strip()
        logo = votos.find("td",{"class","ancho_acta_congreso_imagen"})
        logo = logo.find("img")
        resultados = votos.find_all("td")
        del resultados[0:3]

        for num, r in enumerate(resultados, start=1):
          total = (r.get_text()).strip()
          _voto = [departamento, provincia, distrito, local_votacion, direccion,mesa, n_copia, electores_habiles, total_votantes, estado_acta, partido, num, total]
          
          all_actas.append(_voto)

def save_acta():

  with open('resultados_mesas.csv', 'w') as mesasFile:
    writer = csv.writer(mesasFile)
    writer.writerows(all_actas)

def init():

  list_actas()

  load_actas()

  save_acta()

if __name__ == "__main__":

  init()
  