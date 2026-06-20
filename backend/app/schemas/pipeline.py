from pydantic import BaseModel


class PipelineUpdateRequest(
    BaseModel
):

    status: str


class PipelineResponse(
    BaseModel
):

    id: int

    resume_id: int

    status: str

    class Config:

        from_attributes = True