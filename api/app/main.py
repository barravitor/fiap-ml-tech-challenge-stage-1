# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routes.index_routes import router
from shared.db.database import create_table

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting the application...")
    create_table()
    yield
    print("Closing the application...")

app = FastAPI(
    lifespan=lifespan,
    title="FIAP ML API | Embrapa",
    description="""
<h2>Welcome to the <strong>FIAP ML API | Embrapa</strong> documentation.</h2>
<p>Here you will find endpoints for:</p>
<ul>
    <li><b><a href="#tag/Authentication">Authentication</a></b>: Authentication user on the platform.</li>
    <li><b><a href="#tag/Embrapa">Embrapa</a></b>: Embrapa data.</li>
</ul>
<p>This API is intended to return Embrapa data taken from the official website: <a href="http://vitibrasil.cnpuv.embrapa.br/index.php" target="_blank">http://vitibrasil.cnpuv.embrapa.br/index.php</a></p>
<p>An API for querying Embrapa data to train a non-profit machine learning algorithm</p>
<p>For more information, visit our <a href="https://github.com/barravitor/fiap-ml-tech-challenge-stage-1" target="_blank">GitHub</a>.</p>
    """,
    version="1.0.0",
    openapi_tags=[{
        "name": "Authentication",
        "description": "Operations related to user authentication on the platform."
    }, {
        "name": "Embrapa",
        "description": "Operations related to Embrapa data."
    }]
)

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the API!"}