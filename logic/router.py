from utils.helpers import (
    client,
    DEPLOYMENT_NAME
)

from logic.prompts import (
    TROUBLESHOOTING_PROMPT,
    COMPARISON_PROMPT,
    GENERAL_PROMPT
)


def generate_response(
    query,
    query_type,
    context,
    chat_history=""
):

    context_text = "\n".join(context)

    if query_type == "troubleshooting":
        prompt = TROUBLESHOOTING_PROMPT

    elif query_type == "comparison":
        prompt = COMPARISON_PROMPT

    else:
        prompt = GENERAL_PROMPT

    final_prompt = prompt.format(
        context=context_text,
        query=query,
        history=chat_history
    )

    response = client.chat.completions.create(
        model=DEPLOYMENT_NAME,
        messages=[
            {
                "role": "user",
                "content": final_prompt
            }
        ],
        temperature=0.3
    )

    return (
        response
        .choices[0]
        .message.content
    )