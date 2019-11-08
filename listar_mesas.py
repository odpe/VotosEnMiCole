import sys
import glob, os
import codecs
import csv
from bs4 import BeautifulSoup as bs

mesas = []

all_mesas = []

def list_mesas():
  os.chdir(".")
  for mesa in glob.glob("*.html"):
    mesas.append(mesa)

def load_mesas():

  for mesa in mesas:
    ubigeo,colegio = (mesa.replace(".html","")).split("_")
    f= codecs.open(mesa, 'r')
    parse_mesa(f.read(), ubigeo, colegio)

def parse_mesa(output, ubigeo, colegio):

  html = bs(output, 'html.parser')
  table = html.find("table")
  mesas  = table.find_all("a")

  for mesa in mesas:
    mesa_id = mesa.get_text()
    all_mesas.append([ubigeo, colegio, mesa_id])

def save_mesas():

  with open('actas.csv', 'w') as mesasFile:
    writer = csv.writer(mesasFile)
    writer.writerows(all_mesas)

def init():

  list_mesas()

  load_mesas()

  save_mesas()

if __name__ == "__main__":

  init()
  