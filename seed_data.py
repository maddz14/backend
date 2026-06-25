"""Seed dummy data for Kabinet Samudera demonstration (Supabase edition)."""
from datetime import datetime, timezone, timedelta
import uuid


def slugify(text: str) -> str:
    import re
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text).strip("-")
    return text[:80]


SITE_INFO = {
    "_key": "main",
    "kabinet_name": "Kabinet Samudera",
    "tagline": "Himpunan Mahasiswa Prodi Teknologi Rekayasa Perangkat Lunak",
    "description": "Kabinet Samudera adalah organisasi kemahasiswaan Prodi Teknologi Rekayasa Perangkat Lunak yang berdedikasi untuk menciptakan ekosistem belajar, berkreasi, dan berkolaborasi bagi seluruh mahasiswa TRPL.",
    "visi": "Menjadikan Himaprodi TRPL sebagai wadah pengembangan potensi mahasiswa yang adaptif, inovatif, dan berdaya saing global layaknya samudera yang luas dan dalam.",
    "misi": [
        "Menyelenggarakan program kerja yang berbasis teknologi, kreativitas, dan kolaborasi.",
        "Membangun budaya organisasi yang inklusif, terbuka, dan saling mendukung.",
        "Mengembangkan kompetensi mahasiswa melalui pelatihan, workshop, dan sertifikasi.",
        "Mempererat sinergi antar civitas akademika dan mitra industri.",
        "Menjadi jembatan aspirasi dan pelayanan bagi seluruh anggota Himaprodi TRPL.",
    ],
    "periode": "2025/2026",
    "contact_email": "himaproditrpl@gmail.com",
    "contact_instagram": "@himaproditrpl",
    "contact_address": "Gedung TRPL, Kampus Politeknik, Indonesia",
    "hero_image_url": None,
}


DEPARTEMEN = [
    {"name": "Pengembangan Sumber Daya Manusia", "short_name": "PSDM", "description": "Mengembangkan potensi dan karakter anggota melalui pelatihan, mentoring, dan program kaderisasi yang terarah.", "icon": "users", "color": "cyan", "head": "Bintang Laut Pratama", "programs": ["Kaderisasi Anggota", "Leadership Training", "Mentoring Junior"], "order": 1},
    {"name": "Akademik dan Keilmuan", "short_name": "AKADEMIK", "description": "Mendorong budaya akademik melalui kompetisi, workshop teknologi, dan sharing session keilmuan TRPL.", "icon": "book-open", "color": "teal", "head": "Arkan Mahardika", "programs": ["Coding Bootcamp", "Workshop AI/ML", "Study Group", "Hackathon TRPL"], "order": 2},
    {"name": "Hubungan Masyarakat", "short_name": "HUMAS", "description": "Menjadi jembatan komunikasi antar mahasiswa, kampus, alumni, dan mitra eksternal.", "icon": "megaphone", "color": "blue", "head": "Nayla Oceania", "programs": ["Newsletter TRPL", "Alumni Gathering", "Campus Expo"], "order": 3},
    {"name": "Media dan Informasi", "short_name": "MEDINFO", "description": "Mengelola konten digital, sosial media, dan dokumentasi seluruh kegiatan Himaprodi.", "icon": "camera", "color": "cyan", "head": "Raka Samudera", "programs": ["Content Creator Hub", "Podcast TRPL", "Video Documentation"], "order": 4},
    {"name": "Minat dan Bakat", "short_name": "MIKAT", "description": "Menyalurkan minat mahasiswa di bidang olahraga, seni, dan pengembangan diri non-akademik.", "icon": "trophy", "color": "amber", "head": "Danendra Widya", "programs": ["TRPL Cup", "E-Sports League", "Art Festival"], "order": 5},
    {"name": "Kewirausahaan", "short_name": "KWU", "description": "Membangun jiwa wirausaha digital dan mengelola unit usaha mahasiswa berbasis teknologi.", "icon": "briefcase", "color": "teal", "head": "Saskia Anindya", "programs": ["Startup Weekend", "Merchandise TRPL", "Tech Business Bootcamp"], "order": 6},
]

ANGGOTA = [
    # INTI
    {"name": "Ahmad Ilyas Mu'alimin", "position": "Gubernur Himaprodi", "department": "Inti", "bio": "", "instagram": "", "linkedin": "", "photo_url": None, "order": 1},
    {"name": "M. Rafly Ardiyaksa", "position": "Wakil Gubernur Himaprodi", "department": "Inti", "bio": "", "instagram": "", "linkedin": "", "photo_url": None, "order": 2},
    {"name": "Adela Handira Syahputri", "position": "Sekretaris 1", "department": "Inti", "bio": "", "instagram": "", "linkedin": "", "photo_url": None, "order": 3},
    {"name": "Allika Aullia", "position": "Sekretaris 2", "department": "Inti", "bio": "", "instagram": "", "linkedin": "", "photo_url": None, "order": 4},
    {"name": "Nagita Rorencia Donan", "position": "Bendahara 1", "department": "Inti", "bio": "", "instagram": "", "linkedin": "", "photo_url": None, "order": 5},
    {"name": "Putri Abelia", "position": "Bendahara 2", "department": "Inti", "bio": "", "instagram": "", "linkedin": "", "photo_url": None, "order": 6},

    # ADVOKASI
    {"name": "Petrus Roliand Federico Girsang", "position": "Koordinator Div. Advokasi", "department": "Advokasi", "bio": "", "instagram": "", "linkedin": "", "photo_url": None, "order": 7},
    {"name": "Miftahul Nurul Qolbi", "position": "Anggota Div. Advokasi", "department": "Advokasi", "bio": "", "instagram": "", "linkedin": "", "photo_url": None, "order": 8},
    {"name": "Ratna Kurnia Wati", "position": "Anggota Div. Advokasi", "department": "Advokasi", "bio": "", "instagram": "", "linkedin": "", "photo_url": None, "order": 9},

    # PUBLIC RELATION
    {"name": "Mifta Salsabilah Lubis", "position": "Koordinator Div. Public Relation", "department": "Public Relation", "bio": "", "instagram": "", "linkedin": "", "photo_url": None, "order": 10},
    {"name": "Aliyya Raeni Chayara", "position": "Anggota Div. Public Relation", "department": "Public Relation", "bio": "", "instagram": "", "linkedin": "", "photo_url": None, "order": 11},
    {"name": "Asyifa Salsabila Al-Qodri", "position": "Anggota Div. Public Relation", "department": "Public Relation", "bio": "", "instagram": "", "linkedin": "", "photo_url": None, "order": 12},

    # KEWIRAUSAHAAN
    {"name": "Rizki Wahyu Saputra", "position": "Koordinator Div. Kewirausahaan", "department": "Kewirausahaan", "bio": "", "instagram": "", "linkedin": "", "photo_url": None, "order": 13},
    {"name": "Silva", "position": "Anggota Div. Kewirausahaan", "department": "Kewirausahaan", "bio": "", "instagram": "", "linkedin": "", "photo_url": None, "order": 14},
    {"name": "Dika Prasetyawan", "position": "Anggota Div. Kewirausahaan", "department": "Kewirausahaan", "bio": "", "instagram": "", "linkedin": "", "photo_url": None, "order": 15},
    {"name": "Nursheila Majid", "position": "Anggota Div. Kewirausahaan", "department": "Kewirausahaan", "bio": "", "instagram": "", "linkedin": "", "photo_url": None, "order": 16},
    {"name": "Sri Wahyuni", "position": "Anggota Div. Kewirausahaan", "department": "Kewirausahaan", "bio": "", "instagram": "", "linkedin": "", "photo_url": None, "order": 17},

    # WEB DEV
    {"name": "Rengga Bagus Kurniawan", "position": "Koordinator Div. Development Web & App", "department": "Web Dev", "bio": "", "instagram": "", "linkedin": "", "photo_url": None, "order": 18},
    {"name": "Ahmad Sukron Yusuf", "position": "Anggota Div. Development Web & App", "department": "Web Dev", "bio": "", "instagram": "", "linkedin": "", "photo_url": None, "order": 19},
    {"name": "Ahmad Zulkifli", "position": "Anggota Div. Development Web & App", "department": "Web Dev", "bio": "", "instagram": "", "linkedin": "", "photo_url": None, "order": 20},

    # PDD
    {"name": "Wira Mega Wijaya", "position": "Koordinator Div. Publication, Documentation, & Design", "department": "PDD", "bio": "", "instagram": "", "linkedin": "", "photo_url": None, "order": 21},
    {"name": "Albib Azrianda", "position": "Anggota Div. Publication, Documentation, & Design", "department": "PDD", "bio": "", "instagram": "", "linkedin": "", "photo_url": None, "order": 22},
    {"name": "Baiti Rahma", "position": "Anggota Div. Publication, Documentation, & Design", "department": "PDD", "bio": "", "instagram": "", "linkedin": "", "photo_url": None, "order": 23},

    # PENGEMBANGAN SDM
    {"name": "Lipi Enzelina Br.Sihite", "position": "Koordinator Div. Pengembangan SDM", "department": "Pengembangan SDM", "bio": "", "instagram": "", "linkedin": "", "photo_url": None, "order": 24},
    {"name": "Mya Aprilia Melani Putri", "position": "Anggota Div. Pengembangan SDM", "department": "Pengembangan SDM", "bio": "", "instagram": "", "linkedin": "", "photo_url": None, "order": 25},
    {"name": "Dendi Ramadhan", "position": "Anggota Div. Pengembangan SDM", "department": "Pengembangan SDM", "bio": "", "instagram": "", "linkedin": "", "photo_url": None, "order": 26},

    # MINAT BAKAT
    {"name": "Evanuel Syaputra Saragih", "position": "Koordinator Div. Minat dan Bakat", "department": "Minat Bakat", "bio": "", "instagram": "", "linkedin": "", "photo_url": None, "order": 27},
    {"name": "Rahmi Syafitri", "position": "Anggota Div. Minat dan Bakat", "department": "Minat Bakat", "bio": "", "instagram": "", "linkedin": "", "photo_url": None, "order": 28},
    {"name": "Fathi Nabill Raffa Ruza", "position": "Anggota Div. Minat dan Bakat", "department": "Minat Bakat", "bio": "", "instagram": "", "linkedin": "", "photo_url": None, "order": 29}
]


def _berita_seed():
    base_time = datetime.now(timezone.utc)
    items = [
        {"title": "Kabinet Samudera Resmi Dilantik, Siap Arungi Periode 2025/2026", "excerpt": "Pelantikan Kabinet Samudera berlangsung khidmat di Auditorium Kampus dengan dihadiri seluruh civitas akademika TRPL.", "content": "Pelantikan Kabinet Samudera periode 2025/2026 berlangsung khidmat pada hari Sabtu lalu di Auditorium Kampus.", "category": "Organisasi", "author": "Tim MEDINFO", "image_url": "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=1200", "days_ago": 2},
        {"title": "Workshop AI & Machine Learning: Mengenal GenAI di Era Modern", "excerpt": "Departemen Akademik sukses menggelar workshop GenAI dengan lebih dari 120 peserta antusias.", "content": "Workshop AI & Machine Learning bertajuk 'Mengenal GenAI di Era Modern' digelar oleh Departemen Akademik.", "category": "Akademik", "author": "Arkan Mahardika", "image_url": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1200", "days_ago": 7},
        {"title": "TRPL Cup 2026: Liga Futsal dan E-Sports Digelar Sebulan Penuh", "excerpt": "Departemen Mikat menghadirkan kompetisi olahraga dan e-sports terbesar di TRPL tahun ini.", "content": "TRPL Cup 2026 resmi dibuka dengan upacara pembukaan meriah.", "category": "Minat Bakat", "author": "Danendra Widya", "image_url": "https://images.unsplash.com/photo-1526232761682-d26e03ac148e?w=1200", "days_ago": 14},
        {"title": "Kolaborasi Himaprodi TRPL dengan Industri Lokal untuk Program Magang", "excerpt": "Humas menandatangani MoU dengan 5 perusahaan teknologi untuk program magang eksklusif mahasiswa TRPL.", "content": "Departemen Humas berhasil menjalin kerjasama dengan lima perusahaan teknologi lokal.", "category": "Kemitraan", "author": "Nayla Oceania", "image_url": "https://images.unsplash.com/photo-1521737604893-d14cc237f11d?w=1200", "days_ago": 21},
        {"title": "Startup Weekend TRPL: 48 Jam Melahirkan Ide Bisnis Digital", "excerpt": "Departemen Kewirausahaan menggelar kompetisi startup 48 jam non-stop untuk ide bisnis teknologi.", "content": "Startup Weekend TRPL sukses menjaring 40 peserta dari berbagai angkatan.", "category": "Kewirausahaan", "author": "Saskia Anindya", "image_url": "https://images.unsplash.com/photo-1559136555-9303baea8ebd?w=1200", "days_ago": 28},
        {"title": "Podcast TRPL Episode Perdana: Bincang Santai Soal Karir Tech", "excerpt": "Medinfo meluncurkan Podcast TRPL dengan episode perdana menghadirkan alumni yang bekerja di unicorn lokal.", "content": "Departemen Medinfo Kabinet Samudera resmi meluncurkan Podcast TRPL.", "category": "Media", "author": "Raka Samudera", "image_url": "https://images.unsplash.com/photo-1478737270239-2f02b77fc618?w=1200", "days_ago": 35},
    ]
    result = []
    for i, it in enumerate(items):
        published_at = base_time - timedelta(days=it["days_ago"])
        result.append({
            "id": str(uuid.uuid4()),
            "title": it["title"],
            "slug": slugify(it["title"]) + f"-{i}",
            "excerpt": it["excerpt"],
            "content": it["content"],
            "category": it["category"],
            "author": it["author"],
            "image_url": it["image_url"],
            "published_at": published_at.isoformat(),
        })
    return result


BERITA = _berita_seed()

PROGRAM_KERJA = [
    {"id": str(uuid.uuid4()), "title": "Kaderisasi Anggota Baru", "department": "PSDM", "description": "Program pengkaderan berjenjang untuk anggota baru Himaprodi TRPL.", "schedule": "Februari - April 2026", "status": "ongoing", "image_url": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=800"},
    {"id": str(uuid.uuid4()), "title": "Coding Bootcamp TRPL", "department": "AKADEMIK", "description": "Intensive bootcamp 4 minggu untuk fullstack web development.", "schedule": "Maret 2026", "status": "planned", "image_url": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800"},
    {"id": str(uuid.uuid4()), "title": "Hackathon TRPL 2026", "department": "AKADEMIK", "description": "Kompetisi hackathon tahunan dengan tema AI for Social Good.", "schedule": "Mei 2026", "status": "planned", "image_url": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=800"},
    {"id": str(uuid.uuid4()), "title": "Campus Expo & Open House", "department": "HUMAS", "description": "Pameran prodi TRPL untuk calon mahasiswa baru dan masyarakat umum.", "schedule": "Juni 2026", "status": "planned", "image_url": "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800"},
    {"id": str(uuid.uuid4()), "title": "TRPL Cup 2026", "department": "MIKAT", "description": "Liga olahraga dan e-sports antar angkatan.", "schedule": "Sedang Berlangsung", "status": "ongoing", "image_url": "https://images.unsplash.com/photo-1526232761682-d26e03ac148e?w=800"},
    {"id": str(uuid.uuid4()), "title": "Startup Weekend TRPL", "department": "KWU", "description": "Program inkubasi startup 48 jam untuk mahasiswa.", "schedule": "Selesai - Januari 2026", "status": "completed", "image_url": "https://images.unsplash.com/photo-1559136555-9303baea8ebd?w=800"},
    {"id": str(uuid.uuid4()), "title": "Podcast TRPL Season 1", "department": "MEDINFO", "description": "12 episode podcast membahas karir dan teknologi.", "schedule": "Maret - Agustus 2026", "status": "ongoing", "image_url": "https://images.unsplash.com/photo-1478737270239-2f02b77fc618?w=800"},
    {"id": str(uuid.uuid4()), "title": "Alumni Gathering", "department": "HUMAS", "description": "Reuni dan networking session bersama alumni TRPL.", "schedule": "September 2026", "status": "planned", "image_url": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=800"},
]

GALERI = [
    {"id": str(uuid.uuid4()), "title": "Pelantikan Kabinet Samudera", "category": "Organisasi", "description": "Momen pelantikan resmi pengurus Kabinet Samudera.", "image_url": "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=1000", "type": "image", "video_url": None, "span": "md:col-span-2 md:row-span-2"},
    {"id": str(uuid.uuid4()), "title": "Workshop GenAI", "category": "Akademik", "description": "Antusiasme peserta workshop AI & Machine Learning.", "image_url": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1000", "type": "image", "video_url": None, "span": ""},
    {"id": str(uuid.uuid4()), "title": "TRPL Cup Futsal", "category": "Mikat", "description": "Final futsal TRPL Cup 2026.", "image_url": "https://images.unsplash.com/photo-1526232761682-d26e03ac148e?w=1000", "type": "image", "video_url": None, "span": ""},
    {"id": str(uuid.uuid4()), "title": "Startup Weekend", "category": "Kewirausahaan", "description": "Pitching session Startup Weekend TRPL.", "image_url": "https://images.unsplash.com/photo-1559136555-9303baea8ebd?w=1000", "type": "image", "video_url": None, "span": "md:col-span-2"},
    {"id": str(uuid.uuid4()), "title": "Coding Bootcamp Day 1", "category": "Akademik", "description": "Peserta bootcamp fullstack development.", "image_url": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=1000", "type": "image", "video_url": None, "span": ""},
    {"id": str(uuid.uuid4()), "title": "Rapat Koordinasi Kabinet", "category": "Organisasi", "description": "Rakor bulanan seluruh departemen.", "image_url": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=1000", "type": "image", "video_url": None, "span": ""},
    {"id": str(uuid.uuid4()), "title": "Podcast Recording", "category": "Media", "description": "Behind the scene produksi Podcast TRPL.", "image_url": "https://images.unsplash.com/photo-1478737270239-2f02b77fc618?w=1000", "type": "image", "video_url": None, "span": ""},
    {"id": str(uuid.uuid4()), "title": "Alumni Gathering", "category": "Kemitraan", "description": "Reuni alumni TRPL lintas angkatan.", "image_url": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=1000", "type": "image", "video_url": None, "span": ""},
    {"id": str(uuid.uuid4()), "title": "Campus Expo", "category": "Kemitraan", "description": "Pameran Prodi TRPL di Campus Expo.", "image_url": "https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=1000", "type": "image", "video_url": None, "span": ""},
]

DOSEN = [
    {"id": str(uuid.uuid4()), "name": "Dr. Andi Firmansyah", "nip": "197803152005011002", "gelar_depan": "Dr.", "gelar_belakang": "M.Kom.", "bidang_keahlian": "Rekayasa Perangkat Lunak & Arsitektur Sistem", "jabatan": "Ketua Program Studi TRPL", "pendidikan": "S3 Ilmu Komputer, Universitas Indonesia", "photo_url": "https://images.unsplash.com/photo-1568602471122-7832951cc4c5?w=400&h=400&fit=crop&crop=face", "email": "andi.firmansyah@cwe.ac.id", "linkedin": "", "research_url": "", "order": 1},
    {"id": str(uuid.uuid4()), "name": "Siti Rahmawati", "nip": "198506202010012003", "gelar_depan": "", "gelar_belakang": "M.T.", "bidang_keahlian": "Artificial Intelligence & Machine Learning", "jabatan": "Dosen Tetap", "pendidikan": "S2 Teknik Informatika, Institut Teknologi Bandung", "photo_url": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400&h=400&fit=crop&crop=face", "email": "siti.rahmawati@cwe.ac.id", "linkedin": "", "research_url": "", "order": 2},
    {"id": str(uuid.uuid4()), "name": "Reza Kurniawan", "nip": "199001102018031001", "gelar_depan": "", "gelar_belakang": "M.Cs.", "bidang_keahlian": "DevOps & Cloud Engineering", "jabatan": "Dosen Tetap", "pendidikan": "S2 Computer Science, Universitas Gadjah Mada", "photo_url": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop&crop=face", "email": "reza.kurniawan@cwe.ac.id", "linkedin": "", "research_url": "", "order": 3},
    {"id": str(uuid.uuid4()), "name": "Dewi Puspitasari", "nip": "198712182014032002", "gelar_depan": "", "gelar_belakang": "M.Kom.", "bidang_keahlian": "Mobile & Web Development", "jabatan": "Dosen Tetap", "pendidikan": "S2 Teknik Informatika, Universitas Brawijaya", "photo_url": "https://images.unsplash.com/photo-1551836022-deb4988cc6c0?w=400&h=400&fit=crop&crop=face", "email": "dewi.puspitasari@cwe.ac.id", "linkedin": "", "research_url": "", "order": 4},
    {"id": str(uuid.uuid4()), "name": "Bayu Santoso", "nip": "198903252016031003", "gelar_depan": "", "gelar_belakang": "M.Eng.", "bidang_keahlian": "Data Engineering & Analytics", "jabatan": "Dosen Tetap", "pendidikan": "S2 Information Engineering, Universitas Diponegoro", "photo_url": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&h=400&fit=crop&crop=face", "email": "bayu.santoso@cwe.ac.id", "linkedin": "", "research_url": "", "order": 5},
    {"id": str(uuid.uuid4()), "name": "Mega Lestari", "nip": "199205142020032004", "gelar_depan": "", "gelar_belakang": "M.Kom.", "bidang_keahlian": "Quality Assurance & Testing", "jabatan": "Dosen Tidak Tetap", "pendidikan": "S2 Sistem Informasi, Universitas Bina Nusantara", "photo_url": "https://images.unsplash.com/photo-1580489944761-15a19d654956?w=400&h=400&fit=crop&crop=face", "email": "mega.lestari@cwe.ac.id", "linkedin": "", "research_url": "", "order": 6},
]

PROJECT = [
    {"id": str(uuid.uuid4()), "title": "Sistem Informasi Akademik Terpadu", "description": "Sistem terintegrasi untuk manajemen data akademik kampus, KRS, KHS, dan jadwal perkuliahan.", "category": "Web App", "image_url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=1000", "demo_url": "https://demo.siakad.com", "github_url": "https://github.com/trpl/siakad"},
    {"id": str(uuid.uuid4()), "title": "Aplikasi Pemantauan Cuaca Pertanian", "description": "Aplikasi IoT dan Mobile untuk memantau suhu, kelembaban tanah, dan cuaca bagi petani.", "category": "Mobile App", "image_url": "https://images.unsplash.com/photo-1592982537447-6f2334208f66?w=1000", "demo_url": "", "github_url": "https://github.com/trpl/agri-weather"},
    {"id": str(uuid.uuid4()), "title": "Platform E-Commerce UMKM Lokal", "description": "Marketplace yang didesain khusus untuk membantu UMKM lokal memasarkan produk kerajinan.", "category": "Web App", "image_url": "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=1000", "demo_url": "https://umkm-marketplace.id", "github_url": ""},
    {"id": str(uuid.uuid4()), "title": "Smart Home Automation System", "description": "Sistem kontrol perangkat rumah tangga menggunakan Raspberry Pi dan protokol MQTT.", "category": "IoT", "image_url": "https://images.unsplash.com/photo-1558002038-1055907df827?w=1000", "demo_url": "", "github_url": "https://github.com/trpl/smart-home"},
]



async def seed_all(supabase):
    """Idempotent: only seeds if table is empty."""
    # Site info
    if not supabase.table("site_info").select("id").execute().data:
        supabase.table("site_info").insert(SITE_INFO).execute()

    if not supabase.table("departemen").select("id").execute().data:
        docs = [{"id": str(uuid.uuid4()), **d} for d in DEPARTEMEN]
        supabase.table("departemen").insert(docs).execute()

    current_anggota = supabase.table("anggota").select("id").execute().data
    if len(current_anggota) != len(ANGGOTA):
        supabase.table("anggota").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
        docs = [{"id": str(uuid.uuid4()), **a} for a in ANGGOTA]
        supabase.table("anggota").insert(docs).execute()

    if not supabase.table("dosen").select("id").execute().data:
        supabase.table("dosen").insert(DOSEN).execute()

    if not supabase.table("berita").select("id").execute().data:
        supabase.table("berita").insert(BERITA).execute()

    if not supabase.table("program_kerja").select("id").execute().data:
        supabase.table("program_kerja").insert(PROGRAM_KERJA).execute()

    if not supabase.table("galeri").select("id").execute().data:
        now = datetime.now(timezone.utc).isoformat()
        docs = [{**g, "created_at": now} for g in GALERI]
        supabase.table("galeri").insert(docs).execute()

    if not supabase.table("project").select("id").execute().data:
        supabase.table("project").insert(PROJECT).execute()
