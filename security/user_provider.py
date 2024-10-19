from fastapi import Request, HTTPException

async def get_authenticated_user(request: Request) -> str:
    """
    Recupera o email do usuário autenticado a partir dos cabeçalhos da requisição.
    No caso de Google IAP, o email é passado no cabeçalho 'X-Goog-Authenticated-User-Email'.
    """
    user_email = request.headers.get('X-Goog-Authenticated-User-Email')

    if not user_email:
        raise HTTPException(status_code=401, detail="User not authenticated or missing headers")

    user_email = user_email.replace('accounts.google.com:', '')
    return user_email
