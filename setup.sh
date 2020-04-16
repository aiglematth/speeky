#!/bin/bash

echo "### Début ###"
#Installation des modules
for module in `cat requirements.txt`
do
	pip3 install $module
done

#Création de la base de données
mysql < setup.sql

echo "### #Fin# ###"
