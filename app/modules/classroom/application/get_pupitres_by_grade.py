from app.core.db import SessionDep
from app.modules.classroom.infrastructure.repository import PupitreRepositoryImpl
from app.modules.classroom.domain.service import PupitreService
from app.modules.enrollment.domain.service import EnrollmentService
from app.modules.enrollment.infrastructure.repository import SQLEnrollmentRepository
from app.modules.classroom.schemas.response import PupitreStudentOutSchema


class GetPupitresByGrade:
    def __init__(self, session: SessionDep):
        self.repository = PupitreRepositoryImpl(session=session)
        self.service = PupitreService(repositorio=self.repository)
        self.enrollment_service = EnrollmentService(
            repository=SQLEnrollmentRepository(session=session)
        )

    async def execute(self, grado_id: int) -> list[PupitreStudentOutSchema] | None:
        estudiantes = self.enrollment_service.get_students_by_grade(grado_id)
        estudiantes_map = {e.id: e for e in estudiantes}
        estudiante_ids = list(estudiantes_map.keys())
        pupitres = await self.service.obtener_pupitres(estudiante_ids)
        if not pupitres:
            return None
        return [
            PupitreStudentOutSchema(
                id=pupitre.id,
                nombre_estudiante=estudiantes_map[pupitre.estudiante_id].nombre,
                documento=estudiantes_map[pupitre.estudiante_id].documento,
                estado_pupitre=pupitre.estado_pupitre,
                observacion=pupitre.observacion,
            )
            for pupitre in pupitres
        ]
