VALID_STATUSES = [

    "Applied",

    "Screening",

    "Shortlisted",

    "Interview Scheduled",

    "Interviewed",

    "Selected",

    "Rejected",

    "Hired"
]

def update_pipeline_status(
    candidate,
    status
):

    if status not in VALID_STATUSES:

        raise ValueError(
            "Invalid status"
        )

    candidate.status = status

    return candidate