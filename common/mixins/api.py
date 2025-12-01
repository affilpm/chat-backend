from ..response import success_response

class BaseAPIMixin:
    """
    Reusable success helpers for API views.
    """

    def success(self, data=None, message="Success", status_code=200):
        return success_response(data, message, status_code)

    def created(self, data=None, message="Created successfully"):
        return self.success(data, message, 201)

    def updated(self, data=None, message="Updated successfully"):
        return self.success(data, message, 200)

    def deleted(self, message="Deleted successfully"):
        return self.success(None, message, 200)