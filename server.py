"""Kabinet Samudera — Himaprodi TRPL Backend (Supabase Edition)."""
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / ".env")

import os
import re
import logging
import uuid
from datetime import datetime, timezone
from typing import Optional

# pyrefly: ignore [missing-import]
from fastapi import FastAPI, APIRouter, HTTPException, Request, Response, Depends
# pyrefly: ignore [missing-import]
from starlette.middleware.cors import CORSMiddleware
# pyrefly: ignore [missing-import]
from supabase import create_client, Client

from auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    set_auth_cookies,
    clear_auth_cookies,
    get_current_user,
)
from models import (
    LoginRequest,
    BeritaCreate,
    DepartemenCreate,
    AnggotaCreate,
    DosenCreate,
    GaleriCreate,
    KontakMessage,
    SiteInfo,
    ProjectCreate,
    ProgramKerjaCreate,
)
from seed_data import seed_all

# ---------- Supabase ----------
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]  # use service role for backend
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------- App ----------
app = FastAPI(title="Kabinet Samudera API")

# Setup CORS
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000").rstrip("/")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix="/api")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


# ---------- Helpers ----------
def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text).strip("-")
    return text[:80]


def sb_get(table: str, filters: dict = None, order: str = None, limit: int = 500):
    """Run a SELECT on a Supabase table, returning list of dicts."""
    q = supabase.table(table).select("*")
    if filters:
        for k, v in filters.items():
            q = q.eq(k, v)
    if order:
        q = q.order(order)
    q = q.limit(limit)
    return q.execute().data


def sb_get_one(table: str, filters: dict):
    rows = sb_get(table, filters, limit=1)
    return rows[0] if rows else None


async def _current_user(request: Request) -> dict:
    return await get_current_user(request, supabase)


async def _admin_user(request: Request) -> dict:
    user = await get_current_user(request, supabase)
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


# ---------- Health ----------
@api_router.get("/")
async def root():
    return {"message": "Kabinet Samudera API", "status": "ok"}


@api_router.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}


@api_router.get("/public-stats")
async def public_stats():
    def count(table):
        return supabase.table(table).select("id", count="exact").execute().count or 0
    
    return {
        "berita": count("berita"),
        "anggota": count("anggota"),
        "program_kerja": count("program_kerja"),
    }


# ==================== AUTH ====================
@api_router.post("/auth/login")
async def login(payload: LoginRequest, request: Request, response: Response):
    email = payload.email.lower()
    xff = request.headers.get("x-forwarded-for", "")
    client_ip = xff.split(",")[0].strip() if xff else (request.client.host if request.client else "unknown")
    identifier = f"{client_ip}:{email}"

    # Brute force check
    attempt = sb_get_one("login_attempts", {"identifier": identifier})
    if attempt and attempt.get("count", 0) >= 5:
        locked_until = attempt.get("locked_until")
        if locked_until:
            locked_dt = datetime.fromisoformat(locked_until.replace("Z", "+00:00"))
            if datetime.now(timezone.utc) < locked_dt:
                raise HTTPException(status_code=429, detail="Terlalu banyak percobaan. Coba lagi dalam 15 menit.")

    user = sb_get_one("users", {"email": email})
    if not user or not verify_password(payload.password, user["password_hash"]):
        from datetime import timedelta
        locked_until = (datetime.now(timezone.utc) + timedelta(minutes=15)).isoformat()
        if attempt:
            supabase.table("login_attempts").update({
                "count": attempt.get("count", 0) + 1,
                "locked_until": locked_until
            }).eq("identifier", identifier).execute()
        else:
            supabase.table("login_attempts").insert({
                "identifier": identifier,
                "count": 1,
                "locked_until": locked_until
            }).execute()
        raise HTTPException(status_code=401, detail="Email atau password salah")

    # Clear failed attempts
    supabase.table("login_attempts").delete().eq("identifier", identifier).execute()

    user_id = str(user["id"])
    access = create_access_token(user_id, email)
    refresh = create_refresh_token(user_id)
    set_auth_cookies(response, access, refresh)

    return {
        "id": user_id,
        "email": user["email"],
        "name": user.get("name", ""),
        "role": user.get("role", "user"),
        "access_token": access,
    }


@api_router.post("/auth/logout")
async def logout(response: Response, user: dict = Depends(_current_user)):
    clear_auth_cookies(response)
    return {"message": "Logged out"}


@api_router.get("/auth/me")
async def me(user: dict = Depends(_current_user)):
    return {
        "id": str(user["id"]),
        "email": user["email"],
        "name": user.get("name", ""),
        "role": user.get("role", "user"),
    }


# ==================== SITE INFO ====================
@api_router.get("/site-info")
async def get_site_info():
    doc = sb_get_one("site_info", {"_key": "main"})
    if not doc:
        return {}
    doc.pop("id", None)
    doc.pop("_key", None)
    return doc


@api_router.put("/site-info")
async def update_site_info(payload: SiteInfo, user: dict = Depends(_admin_user)):
    data = payload.model_dump()
    existing = sb_get_one("site_info", {"_key": "main"})
    if existing:
        supabase.table("site_info").update(data).eq("_key", "main").execute()
    else:
        supabase.table("site_info").insert({"_key": "main", **data}).execute()
    return data


# ==================== BERITA ====================
@api_router.get("/berita")
async def list_berita(limit: int = 100, skip: int = 0, category: Optional[str] = None):
    q = supabase.table("berita").select("*").order("published_at", desc=True).range(skip, skip + limit - 1)
    if category:
        q = q.eq("category", category)
    return q.execute().data


@api_router.get("/berita/{slug}")
async def get_berita(slug: str):
    doc = sb_get_one("berita", {"slug": slug})
    if not doc:
        raise HTTPException(status_code=404, detail="Berita tidak ditemukan")
    return doc


@api_router.post("/berita")
async def create_berita(payload: BeritaCreate, user: dict = Depends(_admin_user)):
    doc = payload.model_dump()
    slug_base = slugify(doc["title"])
    slug = slug_base
    idx = 1
    while sb_get_one("berita", {"slug": slug}):
        slug = f"{slug_base}-{idx}"
        idx += 1
    doc.update({
        "id": str(uuid.uuid4()),
        "slug": slug,
        "published_at": datetime.now(timezone.utc).isoformat(),
    })
    supabase.table("berita").insert(doc).execute()
    return doc


@api_router.put("/berita/{berita_id}")
async def update_berita(berita_id: str, payload: BeritaCreate, user: dict = Depends(_admin_user)):
    data = payload.model_dump()
    result = supabase.table("berita").update(data).eq("id", berita_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Berita tidak ditemukan")
    return result.data[0]


@api_router.delete("/berita/{berita_id}")
async def delete_berita(berita_id: str, user: dict = Depends(_admin_user)):
    result = supabase.table("berita").delete().eq("id", berita_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Berita tidak ditemukan")
    return {"message": "Deleted"}


# ==================== DEPARTEMEN ====================
@api_router.get("/departemen")
async def list_departemen():
    return supabase.table("departemen").select("*").order("order").execute().data


@api_router.post("/departemen")
async def create_departemen(payload: DepartemenCreate, user: dict = Depends(_admin_user)):
    doc = payload.model_dump()
    count = len(supabase.table("departemen").select("id").execute().data)
    doc["id"] = str(uuid.uuid4())
    doc["order"] = count + 1
    supabase.table("departemen").insert(doc).execute()
    return doc


@api_router.put("/departemen/{dept_id}")
async def update_departemen(dept_id: str, payload: DepartemenCreate, user: dict = Depends(_admin_user)):
    data = payload.model_dump()
    result = supabase.table("departemen").update(data).eq("id", dept_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Departemen tidak ditemukan")
    return result.data[0]


@api_router.delete("/departemen/{dept_id}")
async def delete_departemen(dept_id: str, user: dict = Depends(_admin_user)):
    result = supabase.table("departemen").delete().eq("id", dept_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Departemen tidak ditemukan")
    return {"message": "Deleted"}


# ==================== ANGGOTA ====================
@api_router.get("/anggota")
async def list_anggota(department: Optional[str] = None):
    q = supabase.table("anggota").select("*").order("order")
    if department:
        q = q.eq("department", department)
    return q.execute().data


@api_router.post("/anggota")
async def create_anggota(payload: AnggotaCreate, user: dict = Depends(_admin_user)):
    doc = payload.model_dump()
    count = len(supabase.table("anggota").select("id").execute().data)
    doc["id"] = str(uuid.uuid4())
    doc["order"] = count + 1
    supabase.table("anggota").insert(doc).execute()
    return doc


@api_router.put("/anggota/{anggota_id}")
async def update_anggota(anggota_id: str, payload: AnggotaCreate, user: dict = Depends(_admin_user)):
    data = payload.model_dump()
    result = supabase.table("anggota").update(data).eq("id", anggota_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Anggota tidak ditemukan")
    return result.data[0]


@api_router.delete("/anggota/{anggota_id}")
async def delete_anggota(anggota_id: str, user: dict = Depends(_admin_user)):
    result = supabase.table("anggota").delete().eq("id", anggota_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Anggota tidak ditemukan")
    return {"message": "Deleted"}


# ==================== DOSEN ====================
@api_router.get("/dosen")
async def list_dosen():
    return supabase.table("dosen").select("*").order("order").execute().data


@api_router.post("/dosen")
async def create_dosen(payload: DosenCreate, user: dict = Depends(_admin_user)):
    doc = payload.model_dump()
    count = len(supabase.table("dosen").select("id").execute().data)
    doc["id"] = str(uuid.uuid4())
    doc["order"] = count + 1
    supabase.table("dosen").insert(doc).execute()
    return doc


@api_router.put("/dosen/{dosen_id}")
async def update_dosen(dosen_id: str, payload: DosenCreate, user: dict = Depends(_admin_user)):
    data = payload.model_dump()
    result = supabase.table("dosen").update(data).eq("id", dosen_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Dosen tidak ditemukan")
    return result.data[0]


@api_router.delete("/dosen/{dosen_id}")
async def delete_dosen(dosen_id: str, user: dict = Depends(_admin_user)):
    result = supabase.table("dosen").delete().eq("id", dosen_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Dosen tidak ditemukan")
    return {"message": "Deleted"}


# ==================== PROGRAM KERJA ====================
@api_router.get("/program-kerja")
async def list_program_kerja(status: Optional[str] = None, department: Optional[str] = None):
    q = supabase.table("program_kerja").select("*")
    if status:
        q = q.eq("status", status)
    if department:
        q = q.eq("department", department)
    return q.execute().data


@api_router.post("/program-kerja")
async def create_program_kerja(payload: ProgramKerjaCreate, user: dict = Depends(_admin_user)):
    doc = payload.model_dump()
    doc["id"] = str(uuid.uuid4())
    supabase.table("program_kerja").insert(doc).execute()
    return doc


@api_router.put("/program-kerja/{prog_id}")
async def update_program_kerja(prog_id: str, payload: ProgramKerjaCreate, user: dict = Depends(_admin_user)):
    data = payload.model_dump()
    result = supabase.table("program_kerja").update(data).eq("id", prog_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Program kerja tidak ditemukan")
    return result.data[0]


@api_router.delete("/program-kerja/{prog_id}")
async def delete_program_kerja(prog_id: str, user: dict = Depends(_admin_user)):
    result = supabase.table("program_kerja").delete().eq("id", prog_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Program kerja tidak ditemukan")
    return {"message": "Deleted"}


# ==================== GALERI ====================
@api_router.get("/galeri")
async def list_galeri(category: Optional[str] = None):
    q = supabase.table("galeri").select("*").order("created_at", desc=True)
    if category:
        q = q.eq("category", category)
    return q.execute().data


@api_router.post("/galeri")
async def create_galeri(payload: GaleriCreate, user: dict = Depends(_admin_user)):
    doc = payload.model_dump()
    doc["id"] = str(uuid.uuid4())
    doc["created_at"] = datetime.now(timezone.utc).isoformat()
    supabase.table("galeri").insert(doc).execute()
    return doc


@api_router.put("/galeri/{item_id}")
async def update_galeri(item_id: str, payload: GaleriCreate, user: dict = Depends(_admin_user)):
    data = payload.model_dump()
    result = supabase.table("galeri").update(data).eq("id", item_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Galeri tidak ditemukan")
    return result.data[0]


@api_router.delete("/galeri/{item_id}")
async def delete_galeri(item_id: str, user: dict = Depends(_admin_user)):
    result = supabase.table("galeri").delete().eq("id", item_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Galeri tidak ditemukan")
    return {"message": "Deleted"}


# ==================== PROJECT ====================
@api_router.get("/project")
async def list_project(category: Optional[str] = None):
    q = supabase.table("project").select("*")
    if category:
        q = q.eq("category", category)
    return q.execute().data


@api_router.post("/project")
async def create_project(payload: ProjectCreate, user: dict = Depends(_admin_user)):
    doc = payload.model_dump()
    doc["id"] = str(uuid.uuid4())
    supabase.table("project").insert(doc).execute()
    return doc


@api_router.put("/project/{proj_id}")
async def update_project(proj_id: str, payload: ProjectCreate, user: dict = Depends(_admin_user)):
    data = payload.model_dump()
    result = supabase.table("project").update(data).eq("id", proj_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Project tidak ditemukan")
    return result.data[0]


@api_router.delete("/project/{proj_id}")
async def delete_project(proj_id: str, user: dict = Depends(_admin_user)):
    result = supabase.table("project").delete().eq("id", proj_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Project tidak ditemukan")
    return {"message": "Deleted"}


# ==================== KONTAK ====================
@api_router.post("/kontak")
async def create_kontak(payload: KontakMessage):
    doc = payload.model_dump()
    doc["id"] = str(uuid.uuid4())
    doc["created_at"] = datetime.now(timezone.utc).isoformat()
    doc["read"] = False
    supabase.table("kontak_messages").insert(doc).execute()
    return {"message": "Pesan berhasil dikirim. Terima kasih!"}


@api_router.get("/kontak")
async def list_kontak(user: dict = Depends(_admin_user)):
    return supabase.table("kontak_messages").select("*").order("created_at", desc=True).execute().data


@api_router.patch("/kontak/{msg_id}/read")
async def mark_kontak_read(msg_id: str, user: dict = Depends(_admin_user)):
    supabase.table("kontak_messages").update({"read": True}).eq("id", msg_id).execute()
    return {"message": "Updated"}


@api_router.delete("/kontak/{msg_id}")
async def delete_kontak(msg_id: str, user: dict = Depends(_admin_user)):
    supabase.table("kontak_messages").delete().eq("id", msg_id).execute()
    return {"message": "Deleted"}


# ==================== STATS (admin dashboard) ====================
@api_router.get("/admin/stats")
async def admin_stats(user: dict = Depends(_admin_user)):
    def count(table, filters=None):
        q = supabase.table(table).select("id", count="exact")
        if filters:
            for k, v in filters.items():
                q = q.eq(k, v)
        return q.execute().count or 0

    return {
        "berita": count("berita"),
        "anggota": count("anggota"),
        "departemen": count("departemen"),
        "program_kerja": count("program_kerja"),
        "galeri": count("galeri"),
        "project": count("project"),
        "pesan_baru": count("kontak_messages", {"read": False}),
    }


# ---------- Mount router + middleware ----------
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=[url.strip() for url in os.environ.get("FRONTEND_URL", "http://localhost:3000").split(",")],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- Startup: seed admin + dummy data ----------
async def seed_admin():
    admin_email = os.environ["ADMIN_EMAIL"].lower()
    admin_password = os.environ["ADMIN_PASSWORD"]
    existing_rows = supabase.table("users").select("*").eq("email", admin_email).execute().data
    existing = existing_rows[0] if existing_rows else None

    if existing is None:
        supabase.table("users").insert({
            "id": str(uuid.uuid4()),
            "email": admin_email,
            "password_hash": hash_password(admin_password),
            "name": "Admin Kabinet Samudera",
            "role": "admin",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }).execute()
        logger.info(f"Admin seeded: {admin_email}")
    elif not verify_password(admin_password, existing["password_hash"]):
        supabase.table("users").update({
            "password_hash": hash_password(admin_password)
        }).eq("email", admin_email).execute()
        logger.info(f"Admin password updated: {admin_email}")


@app.on_event("startup")
async def on_startup():
    try:
        await seed_admin()
        await seed_all(supabase)
        logger.info("Startup complete: admin and seed data ready.")
    except Exception as e:
        logger.warning(f"Startup seeding failed (Supabase may be unreachable): {e}")
        logger.info("Server will continue running. Database features may not work until Supabase is reachable.")
