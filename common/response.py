from rest_framework.response import Response

def success_response(data=None, message="Success", status=200):
    return Response(
        {
            "success": True,
            "data": data,
            "message": message
        },
        status=status
    )