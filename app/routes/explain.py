from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from app.config import OPENAI_API_KEY
from fastapi import Request, Depends
from app.rate_limiter import check_rate_limit

router = APIRouter(prefix="/explain", tags=["Explain"])

client = OpenAI(api_key=OPENAI_API_KEY)

class ExplainRequest(BaseModel):
    sql: str
    dialect: str
    persona: str

@router.post("")
def explain_sql(req: ExplainRequest,request: Request,_: None = Depends(check_rate_limit)
):
    print("REQ:", req)
    if not req.sql.strip():
        raise HTTPException(400, "SQL cannot be empty")

    with open("app/prompts/system.txt") as f:
        system_prompt = f.read()

    with open("app/prompts/explain.txt") as f:
        user_prompt = f.read()

    user_prompt = (
        user_prompt
        .replace("{{dialect}}", req.dialect)
        .replace("{{persona}}", req.persona)
        .replace("{{sql}}", req.sql)
    )

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0.2,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    return {
        "explanation": response.choices[0].message.content
    }
