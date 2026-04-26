<div align="center">
  <h1>Nara Backend Engine</h1>
  <p><em>Mesin backend untuk otomatisasi kampanye pemasaran yang didorong oleh AI, menggunakan arsitektur asinkron untuk skalabilitas tinggi.</em></p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.12.0-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
    <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
    <img src="https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white" alt="Google Cloud" />
    <img src="https://img.shields.io/badge/Mixpanel-7856FF?style=for-the-badge&logo=mixpanel&logoColor=white" alt="Mixpanel" />
    <img src="https://img.shields.io/badge/OneSignal-E54B4D?style=for-the-badge&logo=onesignal&logoColor=white" alt="OneSignal" />
    <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white" alt="GitHub Actions" />
  </p>
</div>

<br/>

## 1. Profil Proyek & Tech Stack

Proyek ini adalah mesin backend untuk otomatisasi kampanye pemasaran yang didorong oleh AI, menggunakan arsitektur asinkron untuk skalabilitas tinggi.

<details open>
<summary><b>Detail Teknologi yang Digunakan</b></summary>
<br/>

| Kategori | Teknologi | Deskripsi |
| :--- | :--- | :--- |
| **Bahasa Pemrograman** | Python 3.12.0 | Core logic aplikasi |
| **Framework API** | FastAPI | Asynchronous Server Gateway Interface untuk performa tinggi |
| **Runtime/Container** | Docker | Multi-stage build ready |
| **Database** | Google Cloud Firestore | Database NoSQL |
| **AI Engine** | Groq Cloud | Model: `llama-3.3-70b-versatile` |
| **Task Queue** | Google Cloud Tasks | Manajemen antrean tugas asinkron |
| **Analytics** | Mixpanel | Pelacakan event & analytics |
| **Messaging** | OneSignal | Push notification |
| **CI/CD** | GitHub Actions | Otomatisasi deployment |
| **Cloud Provider** | Google Cloud Platform | Cloud Run, Artifact Registry |

</details>

---

## 2. Arsitektur Kode (Clean Architecture)

Aplikasi ini menerapkan pemisahan tanggung jawab yang ketat (*Separation of Concerns*) untuk memastikan kode mudah di-maintenance, di-test, dan berskala besar.

- **Controller (API Layer):** Menangani HTTP Request dan validasi input menggunakan Pydantic DTOs.
- **Service Layer:** Jantung logika bisnis, mengorkestrasi AI, Analytics, dan Task Dispatcher.
- **Repository Layer:** Abstraksi akses data Firestore untuk memastikan kode mudah di-test.
- **Infrastructure Adapter:** Wrapper khusus untuk layanan pihak ketiga (Mixpanel, OneSignal, Groq).

<details>
<summary><b>Struktur Direktori Proyek</b></summary>
<br/>

```text
nara-backend/
├── .github/                  # CI/CD Workflows (GitHub Actions)
├── app/
│   ├── api/                  # Controller / API Routes Layer
│   ├── core/                 # Config & Third-party Adapters (Groq, Mixpanel)
│   ├── db/                   # Firestore Connection Setup
│   ├── models/               # Pydantic Schemas & DTOs
│   ├── repositories/         # Database Access Layer
│   ├── services/             # Business Logic Layer
│   ├── tests/                # Unit & Integration Tests
│   └── main.py               # FastAPI Application Entrypoint
├── .env.example              # Template Environment Variables
├── Dockerfile                # Docker Image Configuration
├── requirements.txt          # Python Dependencies
└── README.md                 # Project Documentation
```
</details>

---

## 3. Persiapan Lingkungan & Kredensial (GCP)

Untuk menjalankan aplikasi ini, diperlukan akses ke Google Cloud Console:

### Aktivasi API:
Pastikan API berikut sudah berstatus **Enabled** di GCP Console:
- Artifact Registry API
- Cloud Run API
- Cloud Tasks API
- Firestore API

### Membuat Service Account:
1. Buka **GCP Console** > **IAM & Admin** > **Service Accounts**.
2. Buat akun baru dengan role berikut:
   - `Cloud Datastore User`
   - `Cloud Tasks Enqueuer`
   - `Service Account User`
   - `Cloud Run Admin`
   - `Artifact Registry Administrator`
   - `Storage Admin` (untuk menyimpan build logs)

### Mengambil Kunci (JSON):
1. Klik pada Service Account yang dibuat > Tab **Keys** > **Add Key** > **Create New Key** (JSON).
2. Unduh file tersebut, masukkan ke *root folder* proyek, dan **RENAME** menjadi `gcp-key.json`.

### Setup Database:
- Aktifkan Firestore dan buat database dengan ID `nara` di region `us-central1`.

---

## 4. CI/CD & GitHub Secrets

Karena proyek ini menggunakan GitHub Actions, Anda wajib mencantumkan daftar rahasia (*secrets*) berikut di tab **Settings** > **Secrets and variables** > **Actions** pada repository Anda untuk *deployment* otomatis ke Cloud Run:

- `GCP_PROJECT_ID`: ID Project GCP Anda.
- `GCP_CREDENTIALS_JSON`: Seluruh isi file `gcp-key.json`.
- `MIXPANEL_TOKEN` & `MIXPANEL_API_SECRET`
- `ONESIGNAL_APP_ID` & `ONESIGNAL_API_KEY`
- `GROQ_API_KEY`
- `NARA_ADMIN_API_KEY`

---

## 5. Konfigurasi Environment (`.env`)

Buat file `.env` di root direktori dengan struktur berikut (🚨 **JANGAN di-commit ke Git**):

```env
# GCP Configurations
GOOGLE_CLOUD_PROJECT=nara-project-494421
GOOGLE_APPLICATION_CREDENTIALS=gcp-key.json
GCP_LOCATION=us-central1
GCP_QUEUE_NAME=nara-campaign-queue

# AI & Third Party Services
GROQ_API_KEY=your_groq_api_key
MIXPANEL_TOKEN=your_mixpanel_token
MIXPANEL_API_SECRET=your_mixpanel_api_secret
ONESIGNAL_APP_ID=your_onesignal_app_id
ONESIGNAL_API_KEY=your_onesignal_api_key

# Security
NARA_ADMIN_API_KEY=default_dev_key_123
```

---

## 6. Instruksi Menjalankan Aplikasi

<details>
<summary><b>Menjalankan secara Lokal</b></summary>
<br/>

Pastikan *virtual environment* aktif, lalu instal dependensi:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Akses Swagger UI di: [http://localhost:8000/docs](http://localhost:8000/docs)
</details>

<details>
<summary><b>🐳 Menjalankan dengan Docker</b></summary>
<br/>

Gunakan perintah ini untuk membangun *image* dan menjalankan kontainer dengan menyuntikkan file kredensial secara aman:

**Build Image:**
```bash
docker build -t nara-backend .
```

**Run Container:**
```bash
# Windows (CMD)
docker run -d --name nara-api -p 8000:8000 --env-file .env -v "%cd%\gcp-key.json:/app/gcp-key.json" nara-backend

# PowerShell
docker run -d --name nara-api -p 8000:8000 --env-file .env -v "${PWD}\gcp-key.json:/app/gcp-key.json" nara-backend

# Linux/macOS
docker run -d --name nara-api -p 8000:8000 --env-file .env -v "$(pwd)/gcp-key.json:/app/gcp-key.json" nara-backend
```
</details>

---

## 7. Detail Endpoint & Autentikasi

| Endpoint | Method | Security / Headers | Deskripsi |
| :--- | :---: | :--- | :--- |
| `/health` | `GET` | *Tanpa Auth* | Pengecekan status server |
| `/v1/campaigns/` | `POST` | `X-API-Key: <your_admin_api_key>` | Endpoint pembuatan kampanye |

---

## 8. Alur Kerja Asinkron (The Bumbu)

Sistem ini dirancang untuk memproses kampanye tanpa memblokir request pengguna utama.

1. **Request:** User mengirim konten mentah kampanye.
2. **AI Optimization:** `GroqAdapter` mengirim teks ke Llama 3.3 untuk dioptimasi secara asinkron menggunakan `httpx`.
3. **Persistence:** Data disimpan ke Firestore dengan status `queued`.
4. **Task Dispatch:** `CloudTasksDispatcher` mengirim *payload* ke antrean GCP untuk diproses lebih lanjut oleh *worker*. (Internal *endpoint worker* `/api/v1/internal/tasks/process-campaign` akan dipicu secara otomatis oleh Google Cloud Tasks setelah masuk antrean).
5. **Analytics:** `MixpanelAdapter` mencatat event pembuatan kampanye secara *non-blocking*.

<br/>
<div align="center">
  <sub>Nara Project</sub>
</div>