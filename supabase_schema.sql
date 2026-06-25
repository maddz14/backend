
-- ==================== USERS ====================
CREATE TABLE IF NOT EXISTS users (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email       TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    name        TEXT NOT NULL DEFAULT '',
    role        TEXT NOT NULL DEFAULT 'user',
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ==================== LOGIN ATTEMPTS ====================
CREATE TABLE IF NOT EXISTS login_attempts (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    identifier  TEXT UNIQUE NOT NULL,
    count       INT DEFAULT 0,
    locked_until TIMESTAMPTZ
);

-- ==================== SITE INFO ====================
CREATE TABLE IF NOT EXISTS site_info (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    _key            TEXT UNIQUE DEFAULT 'main',
    kabinet_name    TEXT DEFAULT 'Kabinet Samudera',
    tagline         TEXT DEFAULT '',
    description     TEXT DEFAULT '',
    visi            TEXT DEFAULT '',
    misi            JSONB DEFAULT '[]',
    periode         TEXT DEFAULT '2025/2026',
    contact_email   TEXT DEFAULT '',
    contact_instagram TEXT DEFAULT '',
    contact_address TEXT DEFAULT '',
    hero_image_url  TEXT
);

-- ==================== DEPARTEMEN ====================
CREATE TABLE IF NOT EXISTS departemen (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        TEXT NOT NULL,
    short_name  TEXT NOT NULL,
    description TEXT DEFAULT '',
    icon        TEXT DEFAULT 'waves',
    color       TEXT DEFAULT 'cyan',
    head        TEXT DEFAULT '',
    programs    JSONB DEFAULT '[]',
    "order"     INT DEFAULT 0
);

-- ==================== ANGGOTA ====================
CREATE TABLE IF NOT EXISTS anggota (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        TEXT NOT NULL,
    position    TEXT NOT NULL,
    department  TEXT DEFAULT '',
    photo_url   TEXT,
    bio         TEXT DEFAULT '',
    instagram   TEXT DEFAULT '',
    linkedin    TEXT DEFAULT '',
    "order"     INT DEFAULT 0
);

-- ==================== DOSEN ====================
CREATE TABLE IF NOT EXISTS dosen (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name            TEXT NOT NULL,
    gelar_depan     TEXT DEFAULT '',
    gelar_belakang  TEXT DEFAULT '',
    bidang_keahlian TEXT DEFAULT '',
    jabatan         TEXT DEFAULT '',
    photo_url       TEXT,
    email           TEXT DEFAULT '',
    linkedin        TEXT DEFAULT '',
    research_url    TEXT DEFAULT '',
    "order"         INT DEFAULT 0
);

-- ==================== BERITA ====================
CREATE TABLE IF NOT EXISTS berita (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title       TEXT NOT NULL,
    slug        TEXT UNIQUE NOT NULL,
    excerpt     TEXT DEFAULT '',
    content     TEXT DEFAULT '',
    image_url   TEXT,
    category    TEXT DEFAULT 'Umum',
    author      TEXT DEFAULT 'Admin',
    published_at TIMESTAMPTZ DEFAULT NOW()
);

-- ==================== PROGRAM KERJA ====================
CREATE TABLE IF NOT EXISTS program_kerja (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title       TEXT NOT NULL,
    department  TEXT NOT NULL,
    description TEXT DEFAULT '',
    schedule    TEXT DEFAULT '',
    status      TEXT DEFAULT 'planned',
    image_url   TEXT
);

-- ==================== GALERI ====================
CREATE TABLE IF NOT EXISTS galeri (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title       TEXT NOT NULL,
    image_url   TEXT NOT NULL,
    type        TEXT DEFAULT 'image',
    video_url   TEXT,
    category    TEXT DEFAULT 'Kegiatan',
    description TEXT DEFAULT '',
    span        TEXT DEFAULT '',
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ==================== PROJECT ====================
CREATE TABLE IF NOT EXISTS project (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title       TEXT NOT NULL,
    description TEXT DEFAULT '',
    category    TEXT DEFAULT 'Web App',
    image_url   TEXT,
    demo_url    TEXT,
    github_url  TEXT
);


-- ==================== KONTAK MESSAGES ====================
CREATE TABLE IF NOT EXISTS kontak_messages (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name        TEXT NOT NULL,
    email       TEXT NOT NULL,
    subject     TEXT NOT NULL,
    message     TEXT NOT NULL,
    read        BOOLEAN DEFAULT FALSE,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ==================== ROW LEVEL SECURITY (RLS) ====================
-- Aktifkan RLS untuk semua tabel (backend pakai service role key, jadi bisa bypass RLS)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE login_attempts ENABLE ROW LEVEL SECURITY;
ALTER TABLE site_info ENABLE ROW LEVEL SECURITY;
ALTER TABLE departemen ENABLE ROW LEVEL SECURITY;
ALTER TABLE anggota ENABLE ROW LEVEL SECURITY;
ALTER TABLE dosen ENABLE ROW LEVEL SECURITY;
ALTER TABLE berita ENABLE ROW LEVEL SECURITY;
ALTER TABLE program_kerja ENABLE ROW LEVEL SECURITY;
ALTER TABLE galeri ENABLE ROW LEVEL SECURITY;
ALTER TABLE project ENABLE ROW LEVEL SECURITY;
ALTER TABLE kontak_messages ENABLE ROW LEVEL SECURITY;

-- Allow public read untuk tabel publik
CREATE POLICY "Public read site_info" ON site_info FOR SELECT USING (true);
CREATE POLICY "Public read departemen" ON departemen FOR SELECT USING (true);
CREATE POLICY "Public read anggota" ON anggota FOR SELECT USING (true);
CREATE POLICY "Public read dosen" ON dosen FOR SELECT USING (true);
CREATE POLICY "Public read berita" ON berita FOR SELECT USING (true);
CREATE POLICY "Public read program_kerja" ON program_kerja FOR SELECT USING (true);
CREATE POLICY "Public read galeri" ON galeri FOR SELECT USING (true);
CREATE POLICY "Public read project" ON project FOR SELECT USING (true);
CREATE POLICY "Public insert kontak_messages" ON kontak_messages FOR INSERT WITH CHECK (true);

