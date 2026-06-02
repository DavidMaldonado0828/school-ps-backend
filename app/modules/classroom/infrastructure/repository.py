from sqlmodel import select
from app.core.db import SessionDep
from app.modules.classroom.infrastructure.models import Pupitre
from app.modules.classroom.domain.repositories import PupitreRepository
from sqlmodel import col
from sqlalchemy.exc import SQLAlchemyError

class PupitreRepositoryImpl(PupitreRepository):
    def __init__(self, session: SessionDep):
        self.session = session

    async def obtener_detalle_estudiante(self, estudiante_id: int) -> Pupitre | None:
        return self.session.exec(
            select(Pupitre).where(Pupitre.estudiante_id == estudiante_id)
        ).one_or_none()

    async def actualizar_estado_pupitre(self, pupitre: Pupitre) -> Pupitre:
        self.session.commit()
        self.session.refresh(pupitre)
        return pupitre

    async def obtener_detalle_estudiantes(
        self, estudiante_ids: list[int]
    ) -> list[Pupitre]:
        return list(
            self.session.exec(
                select(Pupitre).where(col(Pupitre.estudiante_id).in_(estudiante_ids))
            ).all()
        )

    async def actualizar_estados_pupitres(self, pupitres: list[Pupitre]) -> int:
        try:
            self.session.commit()
            return len(pupitres)
        except SQLAlchemyError:
            self.session.rollback()
            raise
    
    async def crear_pupitre(self, estudiante_id: int, estado_pupitre: bool, observacion: str | None) -> Pupitre:
        try:
            nuevo_pupitre = Pupitre(
                estudiante_id=estudiante_id, estado_pupitre=estado_pupitre, observacion=observacion
            )
            self.session.add(nuevo_pupitre)
            self.session.commit()
            self.session.refresh(nuevo_pupitre)
            return nuevo_pupitre
        except SQLAlchemyError:
            self.session.rollback()
            raise
        