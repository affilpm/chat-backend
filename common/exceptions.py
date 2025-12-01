from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist, ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """
    Clean, consistent error formatting for all API exceptions.
    """

    # Let DRF handle known exceptions first
    response = exception_handler(exc, context)

    if response is not None:
        return Response(
            {
                "success": False,
                "error": {
                    "type": exc.__class__.__name__,
                    "message": response.data
                }
            },
            status=response.status_code
        )

    # Django ValidationError
    if isinstance(exc, DjangoValidationError):
        return Response(
            {
                "success": False,
                "error": {
                    "type": "ValidationError",
                    "message": exc.message_dict if hasattr(exc, "message_dict") else exc.messages
                }
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Missing object
    if isinstance(exc, ObjectDoesNotExist):
        return Response(
            {
                "success": False,
                "error": {
                    "type": "NotFound",
                    "message": "Requested object does not exist."
                }
            },
            status=status.HTTP_404_NOT_FOUND
        )

    # For ALL unhandled server errors
    logger.error(f"Unhandled exception: {exc}", exc_info=True)

    return Response(
        {
            "success": False,
            "error": {
                "type": "ServerError",
                "message": "An unexpected error occurred. Please try again later."
            }
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )