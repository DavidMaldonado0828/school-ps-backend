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

    async def execute(self, documento_estudiante: str) -> PupitreStudentOutSchema | None:
        estudiante = self.enrollment_service.get_student_by_document(documento_estudiante)
        if not estudiante:
            return None
        
        pupitre = await self.service.get_desk_by_student(estudiante.id)
        if not pupitre:
            return None

        grado = self.enrollment_service.get_grade(estudiante.grado_id)

        return PupitreStudentOutSchema(
            id=pupitre.id,
            nombre_estudiante=estudiante.nombre,
            documento=estudiante.documento,
            grado=grado.nombre if grado else 'Sin grado',
            estado_pupitre=pupitre.estado_pupitre,
            observacion=pupitre.observacion,
        )
