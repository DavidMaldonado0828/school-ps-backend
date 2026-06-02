from app.modules.classroom.domain.repositories import PupitreRepository


class PupitreService:
    def __init__(self, repositorio: PupitreRepository):
        self.repositorio = repositorio

    async def actualizar_estado_pupitre(
        self, estudiante_id: int, nuevo_estado: bool, observacion: str | None
    ):
        pupitre = await self.repositorio.obtener_detalle_estudiante(estudiante_id)
        if not pupitre:
            return None
        pupitre.estado_pupitre = nuevo_estado
        pupitre.observacion = observacion
        return await self.repositorio.actualizar_estado_pupitre(pupitre)

    async def actualizar_estado_pupitres(
        self, estudiante_ids: list[int], nuevo_estado: bool, observacion: str | None
    ):
        pupitres = await self.repositorio.obtener_detalle_estudiantes(estudiante_ids)
        if not pupitres:
            return None
        for pupitre in pupitres:
            pupitre.estado_pupitre = nuevo_estado
            pupitre.observacion = observacion
        total = await self.repositorio.actualizar_estados_pupitres(pupitres)
        return {"total_actualizados": total}

    async def obtener_pupitres(self, estudiante_ids: list[int]):
        pupitres = await self.repositorio.obtener_detalle_estudiantes(estudiante_ids)
        if not pupitres:
            return None
        return pupitres

    async def obtener_pupitre_por_estudiante(self, estudiante_id: int):
        pupitre = await self.repositorio.obtener_detalle_estudiante(estudiante_id)
        if not pupitre:
            return None
        return pupitre

    async def crear_pupitre(
        self, estudiante_id: int, estado_pupitre: bool, observacion: str | None
    ):
        return await self.repositorio.crear_pupitre(
            estudiante_id, estado_pupitre, observacion
        )
