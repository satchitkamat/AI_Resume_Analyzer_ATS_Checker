from fastapi import UploadFile

from app.services.resume_service import (
    upload_resume
)

from app.services.ats_service import (
    calculate_ats_score
)

from app.services.pipeline import (
    create_pipeline_entry
)

def bulk_screen_resumes(
    db,
    files,
    job_description,
    current_user
):
    processed = 0

    successfull = 0

    failed = 0 

    results = []

    for file in files:
        try:

            resume = upload_resume(
                db=db,

                file=file,

                current_user=current_user
            )

            analysis = calculate_ats_score(
                db=db,

                resume=resume,
                resume_text=resume.extracted_text,

                job_description=job_description

            )

            create_pipeline_entry(
                db,

                resume.id
            )

            successful += 1
            results.append({
                "resume_id":
                resume.id,
                "ats_score":
                analysis[
                    "ats_score"
                ]
            })

        except Exception as e:

            failed += 1

            print(e)
        
        processed += 1

    return {
        "total_files":
        len(files),

        "processed_files":
        processed,

        "successful_files":
        successfull,

        "failed_files":
        failed,

        "results":
        results
    }