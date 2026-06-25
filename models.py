"""Pydantic models for API request/response validation."""
# pyrefly: ignore [missing-import]
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime, timezone
import uuid


# ---------- AUTH ----------
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    email: EmailStr
    name: str
    role: str


# ---------- BERITA ----------
class BeritaBase(BaseModel):
    title: str
    excerpt: str
    content: str
    image_url: Optional[str] = None
    category: str = "Umum"
    author: str = "Admin"


class BeritaCreate(BeritaBase):
    pass


class Berita(BeritaBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    slug: str
    published_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# ---------- DEPARTEMEN ----------
class DepartemenBase(BaseModel):
    name: str
    short_name: str
    description: str
    icon: str = "waves"  # lucide icon name
    color: str = "cyan"
    head: str = ""
    programs: List[str] = []


class DepartemenCreate(DepartemenBase):
    pass


class Departemen(DepartemenBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    order: int = 0


# ---------- ANGGOTA ----------
class AnggotaBase(BaseModel):
    name: str
    position: str
    department: str = ""
    photo_url: Optional[str] = None
    bio: Optional[str] = ""
    instagram: Optional[str] = ""
    linkedin: Optional[str] = ""


class AnggotaCreate(AnggotaBase):
    pass


class Anggota(AnggotaBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    order: int = 0


# ---------- DOSEN ----------
class DosenBase(BaseModel):
    name: str
    gelar_depan: Optional[str] = ""        # e.g. "Dr.", "Prof."
    gelar_belakang: Optional[str] = ""     # e.g. "M.Kom.", "Ph.D."
    bidang_keahlian: Optional[str] = ""
    jabatan: Optional[str] = ""            # e.g. "Dosen Tetap", "Ketua Prodi"
    photo_url: Optional[str] = None
    email: Optional[str] = ""
    linkedin: Optional[str] = ""
    research_url: Optional[str] = ""


class DosenCreate(DosenBase):
    pass


class Dosen(DosenBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    order: int = 0


# ---------- PROGRAM KERJA ----------
class ProgramKerjaBase(BaseModel):
    title: str
    department: str
    description: str
    schedule: str = ""  # e.g., "Maret 2026"
    status: str = "planned"  # planned, ongoing, completed
    image_url: Optional[str] = None


class ProgramKerjaCreate(ProgramKerjaBase):
    pass


class ProgramKerja(ProgramKerjaBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))


# ---------- PROJECT ----------
class ProjectBase(BaseModel):
    title: str
    description: str
    category: str = "Web App"
    image_url: Optional[str] = None
    demo_url: Optional[str] = None
    github_url: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))


# ---------- GALERI ----------
class GaleriBase(BaseModel):
    title: str
    image_url: str
    type: str = "image"            # "image" or "video"
    video_url: Optional[str] = None  # used when type == "video"
    category: str = "Kegiatan"
    description: Optional[str] = ""
    span: Optional[str] = ""       # tailwind col/row span hint, e.g. "md:col-span-2 md:row-span-2"


class GaleriCreate(GaleriBase):
    pass


class Galeri(GaleriBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# ---------- KONTAK ----------
class KontakMessage(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str


class KontakMessageStored(KontakMessage):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    read: bool = False


# ---------- SITE INFO ----------
class SiteInfo(BaseModel):
    kabinet_name: str = "Kabinet Samudera"
    tagline: str = "Himaprodi Teknologi Rekayasa Perangkat Lunak"
    description: str = ""
    visi: str = ""
    misi: List[str] = []
    periode: str = "2025/2026"
    contact_email: str = "himaproditrpl@gmail.com"
    contact_instagram: str = "@himaproditrpl"
    contact_address: str = ""
    hero_image_url: Optional[str] = None
