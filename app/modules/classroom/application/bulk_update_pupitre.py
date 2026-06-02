from app.core.db import SessionDep
from app.modules.classroom.infrastructure.repository import PupitreRepositoryImpl
from app.modules.classroom.domain.service import PupitreService
from app.modules.classroom.schemas.request import BulkUpdateRequest
from app.modules.enrollment.domain.service import EnrollmentService
from app.modules.enrollment.infrastructure.repository import SQLEnrollmentRepository


class BulkUpdatePupitreState:
    def __init__(self, session: SessionDep):
        self.repository = PupitreRepositoryImpl(session=session)
        self.service = PupitreService(repositorio=self.repository)
        self.enrollment_service = EnrollmentService(
            repository=SQLEnrollmentRepository(session=session)
        )

    async def execute(self, grado_id: int, request: BulkUpdateRequest):
        estudiantes = self.enrollment_service.get_students_by_grade(grado_id)
        if not estudiantes:
            return None
        estudiante_ids = [e.id for e in estudiantes]
        return await self.service.actualizar_estado_pupitres(
            estudiante_ids=estudiante_ids,
            nuevo_estado=request.estado_pupitre,
            observacion=request.observacion,
        )
