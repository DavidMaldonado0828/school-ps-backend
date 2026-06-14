from pydantic import BaseModel, Field


class PupitreInSchema(BaseModel):
    valor_pagado: int
    observacion: str | None = Field(default=None, max_length=400)


class BulkUpdateRequest(BaseModel):
    detalle_ids: list[int]

