/* =====================================================================
   SON (synthétisé, aucun fichier)
   ===================================================================== */
const SFX = {
  ctx: null, muted: false,
  init() {
    if (this.ctx) return;
    try {
      const c = this.ctx = new (window.AudioContext || window.webkitAudioContext)();
      this.master = c.createGain(); this.master.gain.value = 0.45; this.master.connect(c.destination);
      this.noise = c.createBuffer(1, c.sampleRate * 1.5, c.sampleRate);
      const d = this.noise.getChannelData(0); for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
      this.eng = c.createOscillator(); this.eng.type = 'sawtooth';
      this.engF = c.createBiquadFilter(); this.engF.type = 'lowpass'; this.engF.frequency.value = 500;
      this.engG = c.createGain(); this.engG.gain.value = 0;
      this.eng.connect(this.engF).connect(this.engG).connect(this.master); this.eng.start();
      this.hornG = c.createGain(); this.hornG.gain.value = 0; this.hornG.connect(this.master);
      for (const f of [392, 494]) { const o = c.createOscillator(); o.type = 'square'; o.frequency.value = f; o.connect(this.hornG); o.start(); }
    } catch (e) { this.ctx = null; }
  },
  burst(dur, freq, vol) {
    if (!this.ctx || this.muted) return;
    const c = this.ctx, s = c.createBufferSource(); s.buffer = this.noise;
    const f = c.createBiquadFilter(); f.type = 'lowpass'; f.frequency.value = freq;
    const g = c.createGain(); g.gain.setValueAtTime(vol, c.currentTime); g.gain.exponentialRampToValueAtTime(0.001, c.currentTime + dur);
    s.connect(f).connect(g).connect(this.master); s.start(); s.stop(c.currentTime + dur);
  },
  engine(on, speed, kind) {
    if (!this.ctx) return; const t = this.ctx.currentTime;
    this.engG.gain.setTargetAtTime(this.muted || !on ? 0 : kind === 'heli' ? 0.09 : 0.05, t, 0.1);
    this.eng.frequency.setTargetAtTime(kind === 'heli' ? 28 + speed * 0.4 : 42 + Math.abs(speed) * 2.4, t, 0.08);
  },
  horn(on) { if (this.ctx) this.hornG.gain.setTargetAtTime(on && !this.muted ? 0.05 : 0, this.ctx.currentTime, 0.02); }
};
