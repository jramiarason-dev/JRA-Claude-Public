(() => {
  const dropZone     = document.getElementById('dropZone');
  const fileInput    = document.getElementById('fileInput');
  const dropContent  = document.getElementById('dropContent');
  const previewWrapper = document.getElementById('previewWrapper');
  const previewImg   = document.getElementById('previewImg');
  const removeBtn    = document.getElementById('removeBtn');
  const generateBtn  = document.getElementById('generateBtn');
  const resultCard   = document.getElementById('resultCard');
  const resultBody   = document.getElementById('resultBody');
  const resultMeta   = document.getElementById('resultMeta');
  const errorCard    = document.getElementById('errorCard');
  const errorMsg     = document.getElementById('errorMsg');
  const copyBtn      = document.getElementById('copyBtn');
  const newBtn       = document.getElementById('newBtn');
  const loader       = document.getElementById('loader');

  let selectedFile = null;

  // ── Helpers ──────────────────────────────────────────────────────────────

  function getSelectedPlatform() {
    const radio = document.querySelector('input[name="platform"]:checked');
    return radio ? radio.value : null;
  }

  function updateGenerateBtn() {
    generateBtn.disabled = !(selectedFile && getSelectedPlatform());
  }

  function showPreview(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      previewImg.src = e.target.result;
      dropContent.classList.add('hidden');
      previewWrapper.classList.remove('hidden');
    };
    reader.readAsDataURL(file);
  }

  function clearPreview() {
    selectedFile = null;
    fileInput.value = '';
    previewImg.src = '';
    previewWrapper.classList.add('hidden');
    dropContent.classList.remove('hidden');
    updateGenerateBtn();
  }

  function showError(msg) {
    errorCard.classList.remove('hidden');
    errorMsg.textContent = msg;
  }

  function hideError() {
    errorCard.classList.add('hidden');
    errorMsg.textContent = '';
  }

  function setLoading(on) {
    if (on) {
      loader.classList.remove('hidden');
      generateBtn.classList.add('loading');
      generateBtn.disabled = true;
      resultCard.classList.add('hidden');
      hideError();
    } else {
      loader.classList.add('hidden');
      generateBtn.classList.remove('loading');
      updateGenerateBtn();
    }
  }

  // ── File handling ─────────────────────────────────────────────────────────

  function handleFile(file) {
    if (!file) return;
    const allowed = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
    if (!allowed.includes(file.type)) {
      showError('Format non supporté. Utilisez JPEG, PNG, WebP ou GIF.');
      return;
    }
    if (file.size > 16 * 1024 * 1024) {
      showError('Le fichier est trop lourd (max 16 Mo).');
      return;
    }
    hideError();
    selectedFile = file;
    showPreview(file);
    updateGenerateBtn();
  }

  fileInput.addEventListener('change', () => {
    if (fileInput.files[0]) handleFile(fileInput.files[0]);
  });

  dropZone.addEventListener('click', (e) => {
    if (e.target === removeBtn || removeBtn.contains(e.target)) return;
    if (selectedFile) return;
    fileInput.click();
  });

  dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('drag-over');
  });
  dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));
  dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  });

  removeBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    clearPreview();
    resultCard.classList.add('hidden');
  });

  // ── Platform selection ────────────────────────────────────────────────────

  document.querySelectorAll('input[name="platform"]').forEach((radio) => {
    radio.addEventListener('change', updateGenerateBtn);
  });

  // ── Generate ──────────────────────────────────────────────────────────────

  generateBtn.addEventListener('click', async () => {
    if (!selectedFile || !getSelectedPlatform()) return;

    const platform = getSelectedPlatform();
    setLoading(true);

    const formData = new FormData();
    formData.append('image', selectedFile);
    formData.append('platform', platform);

    try {
      const response = await fetch('/generate', { method: 'POST', body: formData });
      const data = await response.json();

      if (!response.ok || data.error) {
        showError(data.error || 'Une erreur est survenue.');
      } else {
        resultBody.textContent = data.result;
        resultMeta.textContent = data.platform;
        resultCard.classList.remove('hidden');
        resultCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    } catch (err) {
      showError('Impossible de contacter le serveur. Vérifiez votre connexion.');
    } finally {
      setLoading(false);
    }
  });

  // ── Copy ─────────────────────────────────────────────────────────────────

  copyBtn.addEventListener('click', async () => {
    const text = resultBody.textContent;
    try {
      await navigator.clipboard.writeText(text);
      copyBtn.querySelector('.copy-label').textContent = 'Copié !';
      copyBtn.classList.add('copied');
      setTimeout(() => {
        copyBtn.querySelector('.copy-label').textContent = 'Copier tout';
        copyBtn.classList.remove('copied');
      }, 2000);
    } catch {
      // fallback for older browsers
      const ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
      copyBtn.querySelector('.copy-label').textContent = 'Copié !';
      setTimeout(() => (copyBtn.querySelector('.copy-label').textContent = 'Copier tout'), 2000);
    }
  });

  // ── New generation ────────────────────────────────────────────────────────

  newBtn.addEventListener('click', () => {
    resultCard.classList.add('hidden');
    resultBody.textContent = '';
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
})();
