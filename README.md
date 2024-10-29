# FIAP ML API | Embrapa

## API to return Embrapa data

### How to create the environment
```sh
python3 -m venv .venv
```

### How to start the environment
```sh
source .venv/bin/activate
```

### How to install the necessary packages
```sh
pip install -r requirements.txt
```

### How to run the seeds
```sh
python3 -m app.seeds.seed
```

### How to run in dev mode
```sh
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### How to run in production mode
```sh
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### How to finish the environment
```sh
deactivate
```

### How to update the dependency list if needed
```sh
pip freeze > requirements.txt
```