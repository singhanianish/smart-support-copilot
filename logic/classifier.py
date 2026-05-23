from utils.helpers import (
    client,
    DEPLOYMENT_NAME
)


def classify_query(query):

    system_prompt = """
    You are a query classification system.

    Classify the user query into ONLY one category:

    1. troubleshooting
    2. comparison
    3. general

    Rules:
    - troubleshooting:
      issues, errors, fixes, overheating,
      battery drain, connectivity problems

    - comparison:
      compare products/models/features

    - general:
      informational questions,
      how-to, explanations

    Return ONLY the category name.
    """

    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": query
            }
        ],
        temperature=0
    )

    classification = (
        response.choices[0]
        .message.content
        .strip()
        .lower()
    )

    return classification