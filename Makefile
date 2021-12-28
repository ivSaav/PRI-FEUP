# PRI 2021/2022 - T4G3
# Ivo Saavedra, José Ferrão, Pedro Simões

# Python version
PYTHON = python

# Available functions
.PHONY = help run setup clean

# This target is executed whenever we just type `make`
.DEFAULT_GOAL = help

help:
	@echo "---------------HELP-----------------"
	@echo "To create the necessary folders type make setup"
	@echo "To run the project type make run"
	@echo "To clean the outputed file type make clean"
	@echo "------------------------------------"

setup:
	@echo "Checking if img dir exists."
	[ -d img ] || (echo "No directory found, generating..." && mkdir img)
	
run:
# Merging "imdb.csv" with "imdb_all_plots.csv" by id and title
	${PYTHON} ./py_scripts/merge_data.py ;
# ----- Cleaning up of data -----
# The ouput of marge_data.py is taken and the following operations are executed:
# - droping duplicate entries
# - removing rows with no plots
# - removing rows pertaining to "video games" category
# - renaming "tv movie" and "video movie" into "movie"
# - removing plots which were too extensive
# - removing rows with NaN values in key attributes
# At the end all information is stored in "imdb_final.csv"
	${PYTHON} ./py_scripts/processing.py ; 
# Generates images with plots, charts and tables that better describe the dataset
	${PYTHON} ./py_scripts/analysis.py

# Removing generated files
clean:
	rm -r ./data/imdb_final.csv | rm -rf img