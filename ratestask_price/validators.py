from rest_framework.exceptions import ValidationError

from ratestask_port.models import Ports


def validate_origin_destination(value):
    """
    Validation function for the origin and destination field
    """

    ports = Ports.get_ports_by_code_or_slug(value=value)

    if len(ports) == 0:
        raise ValidationError("Invalid input symbol.")
    return ports
