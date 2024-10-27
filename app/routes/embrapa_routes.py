# app/routes/embrapa_routes.py
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
import httpx
import json
from app.helpers.jwt_helpers import get_current_user

embrapa_router = APIRouter()

@embrapa_router.get("/products")
async def get_products(current_user: dict = Depends(get_current_user)):
    try:
        print(datetime.strptime("1994-03-21", "%Y-%m-%d").date())
        print("Entrou aqui correto")
        # async with httpx.AsyncClient() as client:
        #     response = await client.get(EXTERNAL_URL)
        #     response.raise_for_status()  # Verifica se a requisição foi bem-sucedida

        #     # Usando BeautifulSoup para fazer o parsing do HTML
        #     soup = BeautifulSoup(response.text, "html.parser")
        #     table = soup.find("table")  # Encontrando a primeira tabela no HTML
            
        #     # Extrair os dados da tabela
        #     headers = [header.text for header in table.find_all("th")]
        #     rows = []
        #     for row in table.find_all("tr")[1:]:  # Ignora o cabeçalho
        #         cells = row.find_all("td")
        #         if cells:
        #             rows.append([cell.text for cell in cells])

        #     # Estruturar os dados em um formato legível
        #     table_data = {
        #         "headers": headers,
        #         "rows": rows
        #     }

        #     # Salva os dados em um arquivo JSON
        #     with open("table_data.json", "w") as f:
        #         json.dump(table_data, f, indent=4)

        #     return {"message": "Dados da tabela salvos com sucesso!", "data": table_data}

    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar dados: {str(e)}")
