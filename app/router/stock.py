from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List

from app.crud.permisos import verify_permissions
from app.router.dependencies import get_current_user
from app.schemas.users import UserOut
from app.schemas.stock import StockCreate, StockUpdate, StockOut
from core.database import get_db
from app.crud import crud_stock



router = APIRouter()
modulo = 5  # Ajusta el módulo correspondiente para stock

@router.post("/crear", status_code=status.HTTP_201_CREATED)
def create_stock(
    stock: StockCreate,
    db: Session = Depends(get_db),
    user_token: UserOut = Depends(get_current_user)
):
    try:
        id_rol = user_token.id_rol
        if not verify_permissions(db, id_rol, modulo, 'insertar'):
            raise HTTPException(status_code=401, detail="Usuario no autorizado")
        
        crud_stock.create_stock(db, stock)
        return {"message": "Stock creado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/by-id/{id_producto}", response_model=StockOut)
def get_stock(
    id_producto: int,
    db: Session = Depends(get_db),
    user_token: UserOut = Depends(get_current_user)
):
    try:
        id_rol = user_token.id_rol
        if not verify_permissions(db, id_rol, modulo, 'seleccionar'):
            raise HTTPException(status_code=401, detail="Usuario no autorizado")
        
        stock = crud_stock.get_stock_by_id(db, id_producto)
        if not stock:
            raise HTTPException(status_code=404, detail="Stock no encontrado")
        return stock
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/all", response_model=List[StockOut])
def get_all_stock(
    db: Session = Depends(get_db),
    user_token: UserOut = Depends(get_current_user)
):
    try:
        id_rol = user_token.id_rol
        if not verify_permissions(db, id_rol, modulo, 'seleccionar'):
            raise HTTPException(status_code=401, detail="Usuario no autorizado")

        stocks = crud_stock.get_all_stock(db)
        return stocks
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/by-id/{id_producto}")
def update_stock(
    id_producto: int,
    stock: StockUpdate,
    db: Session = Depends(get_db),
    user_token: UserOut = Depends(get_current_user)
):
    try:
        id_rol = user_token.id_rol
        if not verify_permissions(db, id_rol, modulo, 'actualizar'):
            raise HTTPException(status_code=401, detail="Usuario no autorizado")
        
        success = crud_stock.update_stock_by_id(db, id_producto, stock)
        if not success:
            raise HTTPException(status_code=400, detail="No se pudo actualizar el stock")
        return {"message": "Stock actualizado correctamente"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
