def create_indexes(database):

    database["conversations"].create_index(
        "conversation_id",
        unique=True
    )

    database["conversations"].create_index(
        "patient_id"
    )

    database["messages"].create_index(
        "message_id",
        unique=True
    )

    database["messages"].create_index(
        "conversation_id"
    )

    database["messages"].create_index(
        [
            ("conversation_id", 1),
            ("created_at", 1)
        ]
    )