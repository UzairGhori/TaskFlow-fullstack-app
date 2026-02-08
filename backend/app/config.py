from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL: str = os.environ["DATABASE_URL"]
FRONTEND_URL: str = os.environ.get("FRONTEND_URL", "http://localhost:3000")
JWKS_URL: str = os.environ.get("JWKS_URL", FRONTEND_URL + "/api/auth/jwks")
