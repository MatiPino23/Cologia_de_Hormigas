# Cologia_de_Hormigas


## Introducción


La presente tarea 2, correspondiente a la asignatura de Algoritmos Metaheurísticos inspirados en la naturaleza, se desarrolló en el lenguaje de programación Python 3, para la solución del problema del Vendedor viajero mediante el metodo de Sistema de colonia de Hormigas. Los integrantes responsables de la realización de dicha tarea fueron:
Matías Pino V. y María Suloaga V.

## Instalación de entorno


Para utilizar esta aplicación, se necesita instalar Visual Studio Code en la versión compatible con su sistema operativo. Dicho programa se puede descargar en el siguiente enlace: [Enlace](https://code.visualstudio.com/download)

## Clonación de repositorio


Luego de tener instalado el programa anterior, se debe descargar el repositorio que contiene la aplicación en Python 3, en el enlace: [Enlace](https://github.com/MatiPino23/Colonia_de_Hormigas/archive/refs/heads/main.zip)


## Compilación y ejecución de la aplicación


Iniciamos Visual Studio Code, y abrimos la aplicación. Una vez realizado el paso anterior, se debe instalar la libreria numpy, ingresando a la terminal de Visual Studio Code y digitando el siguiente comando para realizar la instalación:

***
```
pip install numpy
```
***

Luego de lo anterior, se debe ejecutar la aplicación desde la terminal utilizando el comando, teniendo en cuenta la siguiente nomenclatura:

```
"a" Numero de hormigas. 
"b" Numero de iteraciones maximas.
"c" Factor de evaporacion de la feromona.
"d" Peso del valor de la heuristica. 
"e" Valor de la probabilidad limite. 

```
```
 a b c d e 
```
python.exe .\main.py 2 .\berlin52.tsp.txt a b c d e

***
## Caso de prueba de la mejor solucion
```
 python.exe .\main.py 2 .\berlin52.tsp.txt 50 500 0.1 2.5 0.9
```
***
