from app.modules.classroom.domain.repositories import PupitreRepository


class PupitreService:
    def __init__(self, repositorio: PupitreRepository):
        self.repositorio = repositorio

    # Se actualiza el estado de UN pupitre, se retorna el pupitre actualizado
    async def update_desk_state(
        self, estudiante_id: int, nuevo_estado: bool, observacion: str | None
    ):
        pupitre = await self.repositorio.get_student_desk(estudiante_id)
        if not pupitre:
            return None
        pupitre.estado_pupitre = nuevo_estado
        pupitre.observacion = observacion
        return await self.repositorio.update_desk_state(pupitre)

    # Se actualiza el estado de varios pupitres, se retorna la cantidad de pupitres actualizados
    async def bulk_update_desk_states(
        self, estudiante_ids: list[int], nuevo_estado: bool, observacion: str | None
    ):
        pupitres = await self.repositorio.list_desks_by_students(estudiante_ids)
        if not pupitres:
            return None
        for pupitre in pupitres:
            pupitre.estado_pupitre = nuevo_estado
            pupitre.observacion = observacion
        total = await self.repositorio.bulk_update_desk_states(pupitres)
        return {"total_actualizados": total}

    # Se obtiene la lista de los pupitres asociados a los estudiantes que pertenecen a un mismo grado, si no se encuentran pupitres se retorna None
    async def get_desks_by_students(self, estudiante_ids: list[int]):
        pupitres = await self.repositorio.list_desks_by_students(estudiante_ids)
        if not pupitres:
            return None
        return pupitres

    # Se obtiene el pupitre al cual pertenece el estudiante, si no tiene pupitre se retorna None
    async def get_desk_by_student(self, estudiante_id: int):
        pupitre = await self.repositorio.get_student_desk(estudiante_id)
        if not pupitre:
            return None
        return pupitre

    # Un servicio para crear un nuevo pupitre, se retorna el pupitre creado
    async def create_desk(
        self, estudiante_id: int, estado_pupitre: bool, observacion: str | None
    ):
        return await self.repositorio.add_desk(
            estudiante_id, estado_pupitre, observacion
        )
