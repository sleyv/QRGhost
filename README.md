<div align="center">
  <h1>QRGhost 👻</h1>
  <p><strong>Hidden 3 Volumes → QR</strong></p>

  [HTML 📥](http://qrghost.sley.nl/download/) • [🌐 Live Demo](https://qrghost.sley.nl) • [🇷🇺 На русском](README_ru.md)

  <img src="https://img.shields.io/badge/Docker-Ready-blue?style=flat&logo=docker" alt="Docker Ready" />
  <img src="https://img.shields.io/badge/AI-Assisted-purple?style=flat" alt="AI Assisted" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat" alt="License" />
</div>

---

### 📖 Overview

**QRGhost** is a secure, plausible-deniability focused QR code generator and data encryption tool. Utilizing a TrueCrypt-style nested hidden volume architecture ("onion encryption"), it allows users to encrypt up to 3 layers of secrets within a single QR code. The application perfectly pads the innermost secrets with CSPRNG noise to the maximum capacity of the QR version, making it mathematically impossible to prove the existence of hidden inner layers without the exact passwords.

---

### ✨ Key Features

- 🔒 **Absolute Plausible Deniability:** Store a distress seed and a real seed. Giving up the outer password reveals the distress seed, while the real seed remains perfectly disguised as cryptographically secure random noise.
- 🧅 **Nested Hidden Volumes:** Encrypt data in up to 3 nested layers. You must decrypt the outer layer to access the ciphertext of the inner layer. It is mathematically impossible to skip or bypass an outer layer to reach an inner secret without providing the outer password.
- 📱 **Native Binary QR Codes:** Encodes data in raw 8-bit byte mode rather than Base64, maximizing the storage capacity of the QR code.
- 🌊 **Smart Capacity Allocation:** Automatically selects the best QR version and uses a "water-filling" algorithm to safely truncate over-sized text to exactly fit the remaining capacity.
- 📋 **Clipboard Integration:** Quickly decrypt by pasting (Ctrl+V) an image of a QR code directly into the Decrypt tab.
- 📥 **Self-Contained:** Download a single, portable `qrghost.html` file for easy, secure sharing and offline air-gapped use.
- 🖥️ **PWA Support:** Works offline after first site visit.
- 🚀 **Multiple deployment options:** standalone, Docker, or behind a reverse proxy.
- 🌐 **Flexible Hosting:** Can be hosted with any web server or library (Apache, Nginx, etc.).

---

### 🚀 Getting Started

#### 1. Clone & Prepare
```bash
git clone https://github.com/sleyv/QRGhost.git
cd QRGhost
```

#### 2. Choose Your Method

<details>
<summary><b>📥 Option 1: Run as a Local File (Easiest)</b></summary>

You can use QRGhost without any installation.
1. Download the `qrghost.html` file from the [Live Demo](https://qrghost.sley.nl) site by clicking the `📥 HTML` button.
2. Alternatively, use the `index.html` file from the `public` folder in this repository.
3. Open the file directly in your web browser.
</details>

<details>
<summary><b>💻 Option 2: Local Server</b></summary>

You can run a simple web server directly on your machine. No SSL certificates are needed for localhost.

1. **Start a local static server** (e.g. Python's built-in http.server):
   ```bash
   python3 -m http.server 8222
   ```
2. Access the app at [http://localhost:8222](http://localhost:8222).
</details>

<details>
<summary><b>🐳 Option 3: Docker (Standalone)</b></summary>

Docker does not require SSL certificates for local development. SSL is only needed when hosting on the internet.

1. **Build and run the container**:
   ```bash
   docker-compose up -d --build
   ```
2. Access the app at [http://localhost:8222](http://localhost:8222).
</details>

<details>
<summary><b>🌐 Option 4: Reverse Proxy (Recommended for Production)</b></summary>

This is the recommended method for hosting online. The reverse proxy (like Nginx or Traefik) will handle HTTPS.

The included `docker-compose-traefik.yml` is an **example** and must be adapted to your setup.

1. Rename `docker-compose-traefik.yml` to `docker-compose.yml` or use the `-f` flag.
2. Modify the file to match your Traefik configuration (e.g., the `Host` rule and external network name).
3. **Build and run the container**:
   ```bash
   docker-compose -f docker-compose-traefik.yml up -d --build
   ```
</details>

<details>
<summary><b>🌐 Option 5: Caddy (Automatic HTTPS)</b></summary>

Caddy is an excellent option for production as it automatically provisions and renews Let's Encrypt SSL certificates.

1. Open `docker-compose-caddy.yml` and change `--domain qrghost.your.domain` to your actual domain name.
2. **Start the container**:
   ```bash
   docker-compose -f docker-compose-caddy.yml up -d
   ```
</details>

<details>
<summary><b>🖥️ Option 6: Host with Any Web Server</b></summary>

The `index.html` file can be hosted with any web server or static file hosting service that supports HTTPS.

1. Upload the static files from the `public` folder (`index.html`, `manifest.json`, `sw.js`, icons) to your web server.
2. Configure HTTPS using your preferred method (Let's Encrypt, Cloudflare, etc.).
3. Access the app via your HTTPS domain.
</details>

---

### ⚠️ Important Notes

- **HTTPS is mandatory** for all browser features to work correctly when hosted online. The app will not function over HTTP. Localhost access is an exception.
- You can host the HTML file with any web hosting service or library that supports static files and HTTPS.
