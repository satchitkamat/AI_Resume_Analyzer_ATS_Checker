from pydantic import BaseModel

class BulkScreeningResponse(
    BaseModel
):
    total_files: int

    processed_files: int

    failed_files: int

    successful_files: int