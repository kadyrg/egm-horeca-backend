def email_verification_body_text(verification_url: str) -> str:
    return f'{verification_url}'

def email_verification_body_html(verification_url: str) -> str:
    return \
    f"""
        <html>
            <body>
                <h1 style="font-size: 40px">Welcome to {verification_url}!</h1>
            </body>
        </html>
    """
