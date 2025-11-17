from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from typing import Optional
import logging

from app.schemas.produccion_huevos import ProduccionHuevosCreate, ProduccionHuevosUpdate

logger = logging.getLogger(__name__)

def create_produccion_huevos(db: Session, produccion: ProduccionHuevosCreate) -> Optional[bool]:
    try:
        sentencia = text("""
            INSERT INTO produccion_huevos (
                id_galpon, cantidad, fecha, id_tipo_huevo
            ) VALUES (
                :id_galpon, :cantidad, :fecha, :id_tipo_huevo
            )
        """)
        db.execute(sentencia, produccion.model_dump())
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear produccion_huevos: {e}")
        raise Exception("Error de base de datos al crear la producción de huevos")

def get_produccion_huevos_by_id(db: Session, produccion_id: int):
    try:
        query = text("""
            SELECT id_produccion, id_galpon, cantidad, fecha, id_tipo_huevo
            FROM produccion_huevos
            WHERE id_produccion = :id_produccion
        """)
        result = db.execute(query, {"id_produccion": produccion_id}).mappings().first()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener produccion_huevos por ID: {e}")
        raise Exception("Error de base de datos al obtener la producción de huevos")

def get_all_produccion_huevos(db: Session):
    try:
        query = text("""
            SELECT id_produccion, id_galpon, cantidad, fecha, id_tipo_huevo
            FROM produccion_huevos
        """)
        result = db.execute(query).mappings().all()
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener todas las producciones de huevos: {e}")
        raise Exception("Error de base de datos al obtener las producciones de huevos")

def update_produccion_huevos_by_id(db: Session, produccion_id: int, produccion: ProduccionHuevosUpdate) -> Optional[bool]:
    try:
        produccion_data = produccion.model_dump(exclude_unset=True)
        if not produccion_data:
            return False

        set_clauses = ", ".join([f"{key} = :{key}" for key in produccion_data.keys()])
        sentencia = text(f"""
            UPDATE produccion_huevos
            SET {set_clauses}
            WHERE id_produccion = :id_produccion
        """)

        produccion_data["id_produccion"] = produccion_id

        result = db.execute(sentencia, produccion_data)
        db.commit()

        return result.rowcount > 0

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al actualizar produccion_huevos {produccion_id}: {e}")
        raise Exception("Error de base de datos al actualizar la producción de huevos")
