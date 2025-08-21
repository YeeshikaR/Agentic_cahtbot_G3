def break_into_subtasks(query: str):
    subtasks_map = {
        "organize a robotics workshop": [
            "Book a venue",
            "Email the coordinator",
            "Prepare the poster",
            "Announce to students"
        ],
        "plan a hackathon": [
            "Form organizing team",
            "Decide on rules",
            "Book auditorium",
            "Invite judges"
        ]
    }
    return subtasks_map.get(query.lower(), ["Research about task", "Plan subtasks", "Execute steps"])
    

def subtask(subtask: str):
    logs = [
        f"Agent started working on: {subtask}",
        f"Gathering resources for {subtask}...",
        f"Executing {subtask}...",
        f"Completed {subtask}"
    ]
    return logs