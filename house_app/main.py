import uvicorn
import fastapi
from fastapi import FastAPI
from house_app.api.entpoints import houses


house_app = fastapi.FastAPI(title='house_site')


house_app.include_router(houses.house_router, tags=['Houses'])


if __name__ == '__main__':
    uvicorn.run(house_app, host='127.0.0.1', port=8080)
