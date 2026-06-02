from app.core.db import SessionDep
from app.modules.classroom.infrastructure.repository import PupitreRepositoryImpl
from app.modules.classroom.domain.service import PupitreService
from app.modules.enrollment.domain.service import EnrollmentService
from app.modules.enrollment.infrastructure.repository import SQLEnrollmentRepository
from app.modules.classroom.schemas.response import PupitreStudentOutSchema


class GetPupitreByStudent:
    def __init__(self, session: SessionDep):
        self.repository = PupitreRepositoryImpl(session=session)
        self.service = PupitreService(repositorio=self.repository)
        self.enrollment_service = EnrollmentService(
            repository=SQLEnrollmentRepository(session=session)
        )

    async def execute(self, estudiante_id: int) -> PupitreStudentOutSchema | None:
        pupitre = await self.service.obtener_pupitre_por_estudiante(estudiante_id)
        if not pupitre:
            return None

        estudiante = self.enrollment_service.get_student_by_id(estudiante_id)
        if not estudiante:
            return None

        return PupitreStudentOutSchema(
            id=pupitre.id,
            nombre_estudiante=estudiante.nombre,
            documento=estudiante.documento,
            estado_pupitre=pupitre.estado_pupitre,
            observacion=pupitre.observacion,
        )
