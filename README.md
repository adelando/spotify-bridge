# 🎵 Spotify Universal Bridge for Home Assistant

Connect your Spotify account to **any** `media_player` in Home Assistant, regardless of whether it supports Spotify Connect. Cast to AirPlay, Chromecast, DLNA, and more—all from one unified dashboard card.

## ✨ Features
- **Universal Casting:** Stream Spotify to devices that don't natively support it.
- **Multi-Speaker Sync:** Select multiple speakers from a grid and play to them simultaneously.
- **Custom Lovelace Card:** A sleek, dedicated UI for managing your "Bridge" sessions.
- **Local Audio Stream:** Uses an internal HTTP bridge to pipe audio directly to your hardware.

## 🛠 Spotify Developer Setup (Required)
Before installing, you must register an application with Spotify to get your credentials:
1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).
2. Click **Create app**.
3. **App name:** `Home Assistant Bridge` (or similar).
4. **Redirect URI:** You **MUST** add `https://my.home-assistant.io/redirect/oauth`.
5. Check the box for the **Developer Agreement** and click **Save**.
6. Once created, go to **Settings** to find your **Client ID** and **Client Secret**.

## 🚀 Installation

### Via HACS (Recommended)
1. Open **HACS** in Home Assistant.
2. Click the three dots in the top right and select **Custom repositories**.
3. Paste the URL of this repository and select **Integration** as the category.
4. Click **Install**.
5. Restart Home Assistant.

### Manual Installation
1. Copy the `spotify_bridge` folder from `custom_components/` into your HA `/config/custom_components/` directory.
2. Go to **Settings > Dashboards > Resources**.
3. Add `/local/custom_components/spotify_bridge/dist/spotify-bridge-card.js` as a **JavaScript Module**.
4. Restart Home Assistant.

## 🚀 Setup
1. Go to **Settings > Integrations > Add Integration**.
2. Search for **Spotify Universal Bridge**.
3. Enter your **Client ID** and **Client Secret** when prompted.
4. Complete the Spotify login via the popup window.
5. Add the `custom:spotify-bridge-card` to your dashboard.

## 🎛 Dashboard Card Configuration
Example basic setup:
type: custom:spotify-bridge-card

## 📜 Requirements & Limitations
- **Spotify Premium:** Required for the streaming API and librespot functionality.
- **Network:** Your Home Assistant instance must be reachable by your speakers on port 8081.
- **Sync:** While the integration attempts to sync players, slight latency may occur between different protocols (e.g., AirPlay vs Chromecast).

## 🤝 Contributing
If you find a bug or have a feature request, feel free to open an issue or submit a Pull Request on GitHub.

## ⚖️ License
MIT License - See [LICENSE](LICENSE) for details.
