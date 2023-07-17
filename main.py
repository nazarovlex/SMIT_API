import uvicorn
from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import register_tortoise
from models import Tariff
from tortoise.exceptions import DoesNotExist
app = FastAPI()

register_tortoise(
    app,
    db_url='postgres://postgres:postgres@postgres:5432/SMIT_API',
    modules={'models': ['models']},
    generate_schemas=True,
    add_exception_handlers=True,
)


@app.get("/price")
async def get_price(date: str, price: float, cargo_type: str) -> dict:
    try:
        tariff = await Tariff.get(date=date, cargo_type=cargo_type)
        result = float(tariff.rate) * price
    except DoesNotExist as e:
        raise HTTPException(status_code=500, detail=str(f"Wrong data or tariff on this date doesn't exist"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"insurance": result}


@app.post("/tariff")
async def tariff(data: dict) -> dict:
    try:
        for date, values in data.items():
            for raw in values:
                await Tariff.create(date=date, cargo_type=raw["cargo_type"], rate=raw["rate"])
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

    return {"Tariff added": data}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
