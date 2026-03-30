import { LitElement, html, css } from 'https://unpkg.com/lit-element@2.4.0/lit-element.js?module';

class SpotifyBridgeCard extends LitElement {
  static get properties() {
    return {
      hass: {},
      config: {}
    };
  }

  render() {
    const players = Object.keys(this.hass.states)
      .filter(eid => eid.startsWith('media_player.') && eid !== 'media_player.spotify_bridge');

    return html`
      <ha-card header="Spotify Universal Bridge">
        <div class="card-content">
          <p>Select target speakers:</p>
          <div class="speaker-list">
            ${players.map(eid => html`
              <div class="speaker-row">
                <input type="checkbox" id="${eid}" @change="${(e) => this._toggleSpeaker(e, eid)}">
                <label for="${eid}">${this.hass.states[eid].attributes.friendly_name || eid}</label>
              </div>
            `)}
          </div>
          <mwc-button raised @click="${this._startBridge}">Sync & Play</mwc-button>
        </div>
      </ha-card>
    `;
  }

  _toggleSpeaker(ev, entityId) {
    // Logic to add/remove entityId from a local "active_targets" array
  }

  _startBridge() {
    // Call your custom integration service
    this.hass.callService('spotify_bridge', 'sync_playback', {
      targets: this.active_targets
    });
  }

  static get styles() {
    return css`
      .speaker-list { max-height: 200px; overflow-y: auto; margin-bottom: 15px; }
      .speaker-row { display: flex; align-items: center; padding: 5px 0; }
      input { margin-right: 10px; width: 20px; height: 20px; }
    `;
  }
}
customElements.define('spotify-bridge-card', SpotifyBridgeCard);
