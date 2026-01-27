def validate_rules(lead):
    errors = []

    if not lead.get("name"):
        errors.append("Missing name")

    if "@" not in lead.get("email", ""):
        errors.append("Invalid email")

    if len(lead.get("description", "")) < 10:
        errors.append("Description too short")

    return errors
