SHELL:=bash
#PYTHON:=/data/mounts/scs-fs-20/kpsy/software/programming/python3/3.7.4/bin/python3.7

venv:
	python3 -m venv venv3.8
#setup_venv_legacy:
#	$(PYTHON) -m venv venv3.7


pip:
	python3 -m pip install --upgrade -r requirements.txt

install:
	# first increment the version to not use the old cached version
	vim +/MINOR_VERSION setup.py && python3 setup.py install

run:
	python3 realage/main.py


# `clean` is not perfect.
# For a full clean also remove venv3.*/ (recreating venv will take some time though)
clean:
	rm -r ./build ./dist ./realage.egg-info

clean_full:
	rm -r ./build ./dist ./realage.egg-info ./venv*/


backup:
	zip -r backup_thesis_notebooks.zip notebooks/*.ipynb && \
	zip -r backup_thesis_data.zip	DATA/ && \
	zip -r backup_thesis_models.zip models/


lab:
	jupyter-lab . --no-browser 



############################
# extras
############################
setup_venv3.8:
	python3.8 -m venv venv3.8

setup_pip_legacy:
	python3 -m pip install --use-feature=2020-resolver --upgrade -r requirements.txt



# If port 1991 is already taken 1992, 19993, ... etc is tried
lab_start_legacy:
	jupyter-lab --ip=0.0.0.0 --port=1991 .

lab_open_legacy:
	firefox.sh 'http://scs-kpsy-01.erasmusmc.nl:1991/'

# You might need to activate the venv first before running this
jupyter_extensions:
	jupyter nbextension enable --py widgetsnbextension &&\
    jupyter labextension install @jupyter-widgets/jupyterlab-manager &&\
    jupyter labextension install @jupyterlab/debugger


