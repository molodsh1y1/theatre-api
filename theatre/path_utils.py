import os
import uuid

from django.db.models import Model


def create_custom_path(instance: Model, filename: str) -> str:
    """
    Generate a custom path for uploaded
    images based on the model class name and
    a random UUID.
    """
    _, extension = os.path.splitext(filename)
    class_name = f"{instance.__class__.__name__.lower()}s"

    return os.path.join(
        f"uploads/images/{class_name}",
        f"{instance.id}-{uuid.uuid4()}{extension}"
    )
