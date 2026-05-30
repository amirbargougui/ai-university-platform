"""
agent/views.py
Endpoint unique : POST /api/agent/chat/
"""
import json
import requests

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings

from .context_builder import build_context
from .prompts import get_system_prompt


@csrf_exempt
@require_http_methods(["POST"])
def agent_chat(request):
    """
    Body JSON attendu : { "message": "...", "history": [...] }
    Retourne      : { "reply": "..." }
    """
    try:
        body = json.loads(request.body)
        user_message = body.get("message", "").strip()
        history = body.get("history", [])

        if not user_message:
            return JsonResponse({"error": "Message vide."}, status=400)

        # Récupère l'utilisateur (connecté ou anonyme)
        user = request.user

        # Contexte adapté selon l'utilisateur
        context = build_context(user=user)

        # Prompt adapté selon l'utilisateur
        system_content = get_system_prompt(context, user=user)

        # Historique (max 10 derniers tours)
        messages = [
            {"role": m["role"], "content": m["content"]}
            for m in history[-10:]
            if m.get("role") in ("user", "assistant")
        ]
        messages.append({"role": "user", "content": user_message})

        # Appel Groq
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "system", "content": system_content},
                    *messages,
                ],
                "max_tokens": 800,
                "temperature": 0.5,
            },
            timeout=30,
        )
        response.raise_for_status()

        reply = response.json()["choices"][0]["message"]["content"]
        return JsonResponse({"reply": reply})

    except requests.exceptions.Timeout:
        return JsonResponse(
            {"error": "Le service est temporairement indisponible (timeout)."},
            status=503,
        )
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": f"Erreur Groq : {e}"}, status=502)
    except Exception as e:
        return JsonResponse({"error": f"Erreur interne : {e}"}, status=500)
