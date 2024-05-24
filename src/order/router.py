from fastapi import APIRouter

router = APIRouter(prefix='/order', tags=['Order'])


@router.get('/')
async def get_orders():
    return {'orders': ['order1','order2']}