def validate_user_message(message):
    if not isinstance(message, str) or len(message) > 5000: raise ValueError("Message must be text up to 5,000 characters.")
    return message.strip()


def validate_provider_response(response):
    if not isinstance(response, str):
        raise ValueError("AURA returned an invalid response.")
    response = response.strip()
    if not response or len(response) > 10000:
        raise ValueError("AURA returned an invalid response.")
    return response
