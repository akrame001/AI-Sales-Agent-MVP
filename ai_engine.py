import openai,json

import os
openai.api_key = os.environ.get("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")

MASTER_PROMPT="""
You are an AI Sales Agent for appointment-based businesses.
Follow language -> service -> timing -> booking choice -> objections -> human takeover.
Respond in JSON:
{"ai_message":"...","updated_info":{}}
"""

def ai_respond(business,lead,conv_id,user_message):
    prompt=f"""
Business Info:{business}
Lead Info:{lead}
User message:{user_message}
"""
    res=openai.ChatCompletion.create(
        model="gpt-5-mini",
        messages=[{"role":"system","content":MASTER_PROMPT},{"role":"user","content":prompt}],
        temperature=0.7
    )
    text=res.choices[0].message.content
    try:
        data=json.loads(text)
        return data["ai_message"],data["updated_info"]
    except:
        return text,{}
