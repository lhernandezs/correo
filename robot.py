import os.path
import csv

from correo         import Correo
from modelo         import Instructor

class Robot:

    # constructor de la clase
    def __init__(self):
        self._fichas = []
        self._instructores = []

    # consigue los datos de las fichas a asignar
    def getFichas(self):
        with open(os.path.join('datos', 'fichas.csv'), 'rt') as csvfile:
            reader = csv.DictReader(csvfile, quotechar='|')
            for ficha in reader:
                self._fichas.append(ficha)

    def getInstructores(self):
        with open(os.path.join('datos', 'instructores.csv'), newline='') as csvfile:
            reader = csv.DictReader(csvfile, quotechar='|')
            for instructor in reader:
                self._instructores.append(instructor)

    # envia los correos segun las filas 
    def sendCorreos(self):
        for rowInstructor in self._instructores:
            lisRowFichasInstructor = list(filter(lambda rowFicha: rowFicha['INSTRUCTOR_2024'] == rowInstructor['NOMBRE'], self._fichas))
            lisFichasInstructor = []
            for rowFichas in lisRowFichasInstructor:
                lisFichasInstructor.append((rowFichas['NIVEL'], rowFichas['PROGRAMA'],rowFichas['FICHA'], rowFichas['FEC_INI'], rowFichas['APRENDICES'],'TECNICO', "TECNICAS"))
            instructor = Instructor(instructor = rowInstructor['NOMBRE'], email = rowInstructor['CORREO'], fichas = lisFichasInstructor)
            correo = Correo('lhernandezs', 'sena.edu.co', 'LeonardoSENA', instructor) # destino correo Leonardo
            # correo = Correo('jpulgarin', 'sena.edu.co', 'Juan Camilo Pulgarin Vanegas', instructor) # destino correo Juan Camilo
            correo.build_email(user=instructor)  


if __name__ == '__main__':
    robot = Robot()
    robot.getFichas()
    robot.getInstructores()
    robot.sendCorreos()
