from abc import ABC, abstractmethod
from app.modules.classroom.infrastructure.models import Pupitre
from app.modules.enrollment.infrastructure.models import Estudiante


class PupitreRepository(ABC):
    @abstractmethod
    async def obtener_por_estudiante(self, estudiante_id: int) -> Pupitre | None:
        pass

    @abstractmethod
    async def guardar_pupitre(self, pupitre: Pupitre) -> Pupitre:
        pass

    @abstractmethod
    async def obtener_por_grado(self, grado_id: int) -> list[Pupitre]:
        pass

    @abstractmethod
    async def guardar_muchos_pupitres(self, pupitres: list[Pupitre]) -> int:
        pass

    @abstractmethod
    async def obtener_por_grado_con_estudiante(self, grado_id: int) -> list:
        pass

    @abstractmethod
    async def obtener_por_estudiante_con_datos(
        self, estudiante_id: int
    ) -> tuple[Pupitre, Estudiante] | None:
        pass
