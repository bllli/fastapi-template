import asyncio
import uuid

from fastapi import APIRouter, Depends, FastAPI
import redis.asyncio
from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide


async def get_redis_pool():
    pool = redis.asyncio.ConnectionPool(host="localhost", port=11452, db=0)
    yield pool
    await pool.aclose()


async def get_redis_client(pool: redis.asyncio.ConnectionPool):
    return redis.asyncio.Redis.from_pool(pool)


class RedisLock:
    def __init__(self, client: redis.asyncio.Redis, key: str):
        self.client = client
        self.key = key

    async def _lock(self):
        fine = await self.client.set(self.key, "1", ex=10, nx=True)
        if not fine:
            raise Exception("Lock already exists")

    async def _unlock(self):
        await self.client.delete(self.key)

    async def __aenter__(self):
        await self._lock()

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self._unlock()




class Service:
    def __init__(self, client: redis.asyncio.Redis):
        self.client = client

    async def process(self):
        lock_key = "lock_key" + str(uuid.uuid4())
        async with RedisLock(self.client, lock_key):
            return "locked"

class DI(containers.DeclarativeContainer):
    pool = providers.Resource(get_redis_pool)
    client = providers.Factory(get_redis_client, pool=pool)
    service = providers.Factory(Service, client=client)



router = APIRouter()

@router.get("/")
@inject
async def index(service: Service = Depends(Provide[DI.service])):
    print("service", id(service))
    value = await service.process()
    return {"result": value}


def create_app():
    container = DI()
    container.wire(modules=[__name__])
    app = FastAPI()
    app.container = container
    app.include_router(router)
    return app
