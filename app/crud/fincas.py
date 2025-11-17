from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from typing import Optional
import logging

from app.schemas.fincas import FincaCreate, FincaUpdate

logger = logging.getLogger(__name__)

def create_finca(db: Session, finca: FincaCreate) -> Optional[bool]:
    try:
        sentencia = text("""
            INSERT INTO fincas (
                nombre, longitud, latitud,
                id_usuario, estado
            ) VALUES (
                :nombre, :longitud, :latitud,
                :id_usuario, :estado
            )
        """)
        db.execute(sentencia, finca.model_dump())
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear finca: {e}")
        raise Exception("Error de base de datos al crear la finca")

def get_finca_by_id(db: Session, finca_id: int):
    try:
        query = text("""
            SELECT id_finca, nombre, longitud, latitud,
            id_usuario, estado
            FROM fincas
            WHERE id_finca = :id_finca
        """)
        result = db.execute(query, {"id_finca": finca_id}).mappings().first()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener finca por ID: {e}")
        raise Exception("Error de base de datos al obtener la finca")

def get_all_finca(db: Session):
    try:
        query = text("""
            SELECT id_finca, nombre, longitud, latitud,
            id_usuario, estado
            FROM fincas
        """)
        result = db.execute(query).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener todas las fincas: {e}")
        raise Exception("Error de base de datos al obtener las fincas")

def get_fincas_by_usuario(db: Session, usuario_id: int):
    try:
        query = text("""
            SELECT id_finca, nombre, longitud, latitud,
            id_usuario, estado
            FROM fincas
            WHERE id_usuario = :id_user
        """)
        result = db.execute(query, {"id_user": usuario_id}).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener fincas por usuario: {e}")
        raise Exception("Error de base de datos al obtener las fincas")

def update_finca_by_id(db: Session, finca_id: int, finca: FincaUpdate) -> Optional[bool]:
    try:
        finca_data = finca.model_dump(exclude_unset=True)
        if not finca_data:
            return False

        set_clauses = ", ".join([f"{key} = :{key}" for key in finca_data.keys()])
        sentencia = text(f"""
            UPDATE fincas 
            SET {set_clauses}
            WHERE id_finca = :id_finca
        """)

        finca_data["id_finca"] = finca_id

        result = db.execute(sentencia, finca_data)
        db.commit()

        return result.rowcount > 0

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar finca {finca_id}: {e}")
        raise Exception("Error de base de datos al actualizar la finca")



# def delete_finca(db: Session, finca_id: int) -> Optional[bool]:
#     try:
#         query = text("""
#             DELETE FROM fincas 
#             WHERE id_finca = :id_finca
#         """)
#         result = db.execute(query, {"id_finca": finca_id})
#         db.commit()
#         return result.rowcount > 0
#     except SQLAlchemyError as e:
#         db.rollback()
#         logger.error(f"Error al eliminar finca {finca_id}: {e}")
#         raise Exception("Error de base de datos al eliminar la finca")