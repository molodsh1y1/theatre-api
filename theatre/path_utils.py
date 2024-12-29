import os
import uuid


def create_custom_path(instance, filename):
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
