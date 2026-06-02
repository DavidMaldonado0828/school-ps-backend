from abc import ABC, abstractmethod
from app.modules.classroom.infrastructure.models import Pupitre


class PupitreRepository(ABC):
    @abstractmethod
    async def obtener_detalle_estudiante(self, estudiante_id: int) -> Pupitre | None:
        pass

    @abstractmethod
    async def actualizar_estado_pupitre(self, pupitre: Pupitre) -> Pupitre:
        pass

    @abstractmethod
    async def obtener_detalle_estudiantes(
        self, estudiante_ids: list[int]
    ) -> list[Pupitre]:
        pass

    @abstractmethod
    async def actualizar_estados_pupitres(self, pupitres: list[Pupitre]) -> int:
        pass

    @abstractmethod
    async def crear_pupitre(
        self, estudiante_id: int, estado_pupitre: bool, observacion: str | None
    ) -> Pupitre:
        pass
