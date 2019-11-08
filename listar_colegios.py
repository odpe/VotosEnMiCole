import sys
import glob, os
import codecs
import csv
from bs4 import BeautifulSoup as bs

distritos = []

all_colegios = []

def list_colegios():
  os.chdir(".")
  for ubigeo in glob.glob("*.html"):
    distritos.append(ubigeo)

def load_colegios():

  for distrito in distritos:
    f= codecs.open(distrito, 'r')
    parse_colegio(f.read())

def parse_colegio(output):

  html = bs(output, 'html.parser')
  colegios  = html.find_all("option")

  for colegio in colegios:
    if(colegio['value'] != '-1?-1'):
      all_colegios.append([colegio['value'], colegio.get_text()])

def save_colegios():

  with open('colegios.csv', 'w') as colegiosFile:
    writer = csv.writer(colegiosFile)
    writer.writerows(all_colegios)

def init():

  list_colegios()

  load_colegios()

  save_colegios()

if __name__ == "__main__":

  init()
  