from pydantic import BaseModel, PositiveInt


class CKStop(BaseModel):

    node: PositiveInt
    paths: list[list[PositiveInt]]
    start: PositiveInt
    end: PositiveInt
    max_steps: PositiveInt
