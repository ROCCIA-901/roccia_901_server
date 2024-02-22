from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None and "message" not in response.data:
        error_messages = []

        for field, messages in response.data.items():
            if isinstance(messages, list):
                error_messages.extend(messages)
            else:
                error_messages.append(messages)

        combined_message = " ".join(error_messages)

        response.data = {"message": combined_message}

    return response
