## Project

This project contains the publicly available code for my master project software engineering on vascular age.


## Architecture



![Architecture][./var/source_code_thesis.pdf]("Architecture: This project can both be used in a batch processor and in a library.")









## Usage Hints

0. Ensure you are in the root dir of the project
``bash
cd PROJECT_DIR
``

1. If no virtual environment exists yet (i.e. no `venv3.*` folder available) then create it:
```bash
make venv
```
2. Load the virtual environment:
```bash
source source.sh
```

3. install software requirements (if not done yet)
```bash
make pip
```

4. install the project itself:
```bash
make install
```

5. run the project 
```bash
python3 realage/main.py
# OR:
make run
```

5. Alternatively, run one of the notebooks (not publicly available because those contain private information)
```bash
make lab
# go to localhost:8080 (or the next port if 8080 was unavailable)
```






