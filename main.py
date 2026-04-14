import os
import re
from typing import Optional

from google import genai
import httpx
from bs4 import BeautifulSoup
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Troopod AI", version="1.0.0")

# ✅ CORS (important for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Gemini Client (HARDCODED → works guaranteed)
client = genai.Client(api_key="AIzaSyAURP7N2TYVrY5MIAfPjI90NlM2P3M1u_I")

MAX_HTML_LENGTH = 15000


# ── Helpers ─────────────────────────────

def inject_base_tag(html: str, base_url: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    if not soup.find("base"):
        base_tag = soup.new_tag("base", href=base_url)
        head = soup.find("head")
        if head:
            head.insert(0, base_tag)
        else:
            soup.insert(0, base_tag)
    return str(soup)


async def fetch_page_html(url: str) -> tuple[str, str]:
    try:
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as http:
            response = await http.get(url)
            response.raise_for_status()

        from urllib.parse import urlparse
        parsed = urlparse(str(response.url))
        base_url = f"{parsed.scheme}://{parsed.netloc}"

        html = inject_base_tag(response.text, base_url)
        return html, base_url

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fetch error: {str(e)}")


def clean_llm_html(text: str) -> str:
    text = re.sub(r"^```html\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^```\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text, flags=re.IGNORECASE)
    return text.strip()


def build_prompt(landing_url: str, landing_html: str, ad_context: str) -> str:
    truncated = (
        landing_html[:MAX_HTML_LENGTH] + "\n<!-- truncated -->"
        if len(landing_html) > MAX_HTML_LENGTH
        else landing_html
    )

    return f"""
You are a senior CRO expert and copywriter.

Ad Context:
{ad_context}

Landing Page:
{landing_url}

Task:
Improve this page to increase conversions, but make it feel NATURAL and HUMAN.

Guidelines:
- Do NOT sound robotic or generic
- Avoid buzzwords like "revolutionary", "unlock", "leverage"
- Write like a real marketer, not AI
- Keep tone consistent with brand
- Make copy concise and clear
- Improve CTA clarity and urgency
- Preserve structure (HTML must remain valid)

Focus on:
- Headline clarity
- Strong value proposition
- Trust signals
- CTA improvements

Return ONLY full HTML.
"""    


# ── Routes ─────────────────────────────

class FetchPageRequest(BaseModel):
    url: str


@app.get("/")
def root():
    return {"message": "Backend running 🚀"}


@app.post("/api/fetch-page")
async def fetch_page(req: FetchPageRequest):
    if not req.url.startswith("http"):
        raise HTTPException(status_code=400, detail="Invalid URL")

    html, base_url = await fetch_page_html(req.url)

    print("Fetched page successfully")

    return {"html": html, "baseUrl": base_url}


@app.post("/api/personalize")
async def personalize(
    landingPageHtml: str = Form(...),
    landingPageUrl: Optional[str] = Form(None),
    adUrl: Optional[str] = Form(None),
    adDescription: Optional[str] = Form(None),
    adImage: Optional[UploadFile] = File(None),
):
    if not landingPageHtml:
        raise HTTPException(status_code=400, detail="Landing page required")

    if not adImage and not adUrl and not adDescription:
        raise HTTPException(status_code=400, detail="Ad input required")

    # Build ad context
    if adImage and adImage.filename:
        ad_context = "Ad image provided"
    elif adUrl:
        ad_context = f"Ad URL: {adUrl}"
    else:
        ad_context = f"Ad description: {adDescription}"

    prompt = build_prompt(
        landingPageUrl or "",
        landingPageHtml,
        ad_context
    )

    try:
        print("→ Calling Gemini...")

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )

        output_text = response.text if hasattr(response, "text") else str(response)
        modified_html = clean_llm_html(output_text)

        print("← Gemini response received")

        return {
            "html": modified_html
        }

    except Exception as e:
        print("ERROR:", str(e))
        raise HTTPException(status_code=500, detail=f"Gemini error: {str(e)}")


@app.get("/api/health")
def health():
    return {"status": "ok"}