/* ========================================================
   NETSHIELD AI - MAIN JS
   Network Intrusion Detection with Live Geo-Tracking
   ======================================================== */
(function () {
  "use strict";

  let framesLoaded = false;
  let cyberLoaderFinishedSequence = false;

  function checkLoaderCompletion() {
    if (framesLoaded && cyberLoaderFinishedSequence) {
      document.body.classList.add("is-loaded");
      const loader = document.getElementById("loader");
      if (loader) loader.setAttribute("aria-hidden", "true");
    }
  }

  /* --- Federated AI Loader Logic: AutoEncoder Flow --- */
  function initCyberLoader() {
    const canvas = document.getElementById('matrix-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    function resize() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize);

    // --- AutoEncoder Bottleneck Animation ---
    const particles = [];
    const particleCount = 400; // Optimal count for smooth loading
    const baseSpeed = 5;
    const bottleneckWidth = 60;

    class Particle {
      constructor() {
        this.reset(true);
      }

      reset(randomX = false) {
        this.x = randomX ? Math.random() * canvas.width : 0;
        this.y = Math.random() * canvas.height;
        this.originalY = this.y;
        this.speedOffset = Math.random() * 0.5 + 0.5;
        this.isThreat = Math.random() > 0.95; // 5% chance to be an anomaly
      }

      update() {
        this.x += baseSpeed * this.speedOffset;

        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;

        const distanceToCenter = Math.abs(this.x - centerX);
        let compression = distanceToCenter / (canvas.width / 2);
        let currentSpread = (canvas.height / 2) * Math.max(compression, bottleneckWidth / canvas.height);

        const targetY = centerY + ((this.originalY - centerY) / (canvas.height / 2)) * currentSpread;
        this.y += (targetY - this.y) * 0.1;

        if (this.x > canvas.width) {
          this.reset();
        }
      }

      draw() {
        const isCompressed = Math.abs(this.x - canvas.width / 2) < 50;

        if (isCompressed) {
          ctx.fillStyle = '#ffffff'; // Flash white in latent space
        } else if (this.isThreat) {
          ctx.fillStyle = '#f59e0b'; // Amber for anomalies
        } else {
          ctx.fillStyle = '#38bdf8'; // Cyan/Blue for normal data
        }

        ctx.beginPath();
        ctx.arc(this.x, this.y, 2, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    function initParticles() {
      particles.length = 0;
      for (let i = 0; i < particleCount; i++) {
        particles.push(new Particle());
      }
    }
    initParticles();

    // --- Cleaned up drawing function ---
    function drawAutoEncoder() {
      ctx.fillStyle = 'rgba(15, 23, 42, 0.3)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
      ctx.font = 'bold 36px monospace';
      ctx.textAlign = 'center';
      ctx.fillText('AUTOENCODERS', canvas.width / 2, 80);

      ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
      ctx.font = '25px monospace';
      ctx.textAlign = 'center';
      ctx.fillText('ENCODER - INPUT DATA', canvas.width * 0.15, canvas.height / 2 - 100);
      ctx.fillText('LATENT SPACE', canvas.width / 2, canvas.height / 2 - bottleneckWidth / 2 - 30);
      ctx.fillText('DECODER - RECONSTRUCTED DATA', canvas.width * 0.85, canvas.height / 2 - 100);

      ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
      ctx.setLineDash([5, 5]);
      ctx.strokeRect(canvas.width / 2 - 30, canvas.height / 2 - bottleneckWidth / 2 - 20, 60, bottleneckWidth + 40);
      ctx.setLineDash([]);

      for (let i = 0; i < particles.length; i++) {
        particles[i].update();
        particles[i].draw();
      }

      requestAnimationFrame(drawAutoEncoder);
    }

    // Start animation loop
    requestAnimationFrame(drawAutoEncoder);

    // --- Terminal logic ---
    const container = document.getElementById('terminal-lines-container');
    if (!container) return;

    const lines = [
      "U R Being HACKED :)",
      "HACKING AND STEALING YOUR DATA ;)",
      "PLZ WAIT...",
      "DON'T PANIC IT WAS A JOKE... HEHE",
      "BUT IT COULD HAPPEN IF THERE WAS NO AUTOENCODER BASED NETWORK INTRUSION DETECTION SYSTEM...",
      "Starting the Autoencoder system...",
      "Compressing data to find the most important patterns...",
      "Passing information through the narrow bottleneck layer...",
      "Reconstructing data back to its original size...",
      "Comparing the original data with the reconstructed data...",
      "System ready. Monitoring for unusual activity..."
    ];

    let currentLineIdx = 0;
    const promptPrefix = "PS C:\\Windows\\system32> ";

    function typeLine(text, cb) {
      const lineDiv = document.createElement('div');
      lineDiv.className = 'terminal-line';

      // --- NEW: Font fix and Color update ---
      lineDiv.style.fontFamily = "'Courier New', Courier, monospace"; // Prevents random font changes
      lineDiv.style.color = '#00ffff';
      lineDiv.style.fontSize = '20px';
      lineDiv.style.marginBottom = '10px';

      const textSpan = document.createElement('span');
      const cursorSpan = document.createElement('span');
      cursorSpan.className = 'terminal-cursor';
      cursorSpan.textContent = '_';

      textSpan.textContent = promptPrefix;
      lineDiv.appendChild(textSpan);
      lineDiv.appendChild(cursorSpan);
      container.appendChild(lineDiv);

      let charIdx = 0;
      const typeInterval = setInterval(() => {
        if (charIdx < text.length) {
          textSpan.textContent = promptPrefix + text.substring(0, charIdx + 1);
          charIdx++;
        } else {
          clearInterval(typeInterval);
          cursorSpan.remove();
          if (cb) setTimeout(cb, 150);
        }
      }, 45);
    }

    function typeNextLine() {
      if (currentLineIdx < lines.length) {
        typeLine(lines[currentLineIdx], typeNextLine);
        currentLineIdx++;
      } else {
        cyberLoaderFinishedSequence = true;
        if (!framesLoaded) {
          setTimeout(() => {
            container.innerHTML = '';
            currentLineIdx = 0;
            cyberLoaderFinishedSequence = false;
            typeNextLine();
          }, 1000);
        } else {
          checkLoaderCompletion();
        }
      }
    }

    typeNextLine();
  }

  initCyberLoader();

  const FRAME_PATH = "/static/frames/ezgif-frame-";
  const FRAME_COUNT = 240;

  const canvas = document.getElementById("sequence");
  const ctx = canvas.getContext("2d");
  const scrolly = document.getElementById("scrolly");
  const nav = document.getElementById("nav");
  const loader = document.getElementById("loader");
  const loaderProgress = document.getElementById("loader-progress");
  const panels = Array.from(document.querySelectorAll(".panel"));

  const images = new Array(FRAME_COUNT);
  let loadedCount = 0;
  let latestProgress = -1;
  let ticking = false;
  let lastScrollY = 0;
  let scrollDirection = 'up';

  function clamp(v, min, max) { return Math.min(Math.max(v, min), max); }
  function easeOutCubic(t) { return 1 - Math.pow(1 - t, 3); }
  function easeInCubic(t) { return t * t * t; }

  /* --- Canvas sizing --- */
  function setCanvasSize() {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.floor(canvas.clientWidth * dpr);
    canvas.height = Math.floor(canvas.clientHeight * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  /* --- Preload frames --- */
  function preloadFrames() {
    for (let i = 0; i < FRAME_COUNT; i++) {
      const img = new Image();
      const num = String(i + 1).padStart(3, "0");
      img.src = `${FRAME_PATH}${num}.webp`;
      img.onload = () => {
        loadedCount++;
        if (loaderProgress) {
          loaderProgress.textContent = `${Math.round((loadedCount / FRAME_COUNT) * 100)}%`;
        }
        if (loadedCount === 1) drawFrame(0);
        if (loadedCount === FRAME_COUNT) {
          framesLoaded = true;
          checkLoaderCompletion();
        }
      };
      images[i] = img;
    }
  }

  /* --- Draw frame --- */
  function drawFrame(index) {
    const img = images[index];
    if (!img || !img.complete) return;
    const cw = canvas.clientWidth, ch = canvas.clientHeight;
    const ir = img.width / img.height, cr = cw / ch;
    let dw = cw, dh = ch;
    if (cr > ir) dh = cw / ir; else dw = ch * ir;
    const dx = (cw - dw) / 2, dy = (ch - dh) / 2;
    ctx.clearRect(0, 0, cw, ch);
    ctx.drawImage(img, dx, dy, dw, dh);
  }

  /* --- Panel fade with easing --- */
  function updatePanels(progress) {
    panels.forEach((panel, idx) => {
      const start = parseFloat(panel.dataset.start);
      const end = parseFloat(panel.dataset.end);
      const isLast = idx === panels.length - 1;
      if (idx === 0 && progress <= 0.06) {
        panel.style.opacity = "1";
        panel.style.transform = "translateY(0px)";
        return;
      }
      if (isLast && progress >= start) {
        const local = clamp((progress - start) / (end - start), 0, 1);
        const fadeIn = easeOutCubic(clamp(local / 0.3, 0, 1));
        const drift = (1 - fadeIn) * 28;
        panel.style.opacity = fadeIn.toFixed(3);
        panel.style.transform = `translateY(${drift.toFixed(2)}px)`;
        return;
      }
      const local = clamp((progress - start) / (end - start), 0, 1);
      const fadeIn = easeOutCubic(clamp(local / 0.3, 0, 1));
      const fadeOut = 1 - easeInCubic(clamp((local - 0.7) / 0.3, 0, 1));
      const opacity = Math.min(fadeIn, fadeOut);
      const drift = (1 - opacity) * 28 * (progress < (start + end) / 2 ? 1 : -1);
      panel.style.opacity = opacity.toFixed(3);
      panel.style.transform = `translateY(${drift.toFixed(2)}px)`;
    });
  }

  /* --- Scroll progress --- */
  function getScrollProgress() {
    const top = scrolly.offsetTop;
    const h = scrolly.offsetHeight - window.innerHeight;
    return clamp((window.scrollY - top) / h, 0, 1);
  }

  function updateScene() {
    const progress = getScrollProgress();
    if (progress === latestProgress) { ticking = false; return; }
    const fi = Math.min(FRAME_COUNT - 1, Math.round(progress * (FRAME_COUNT - 1)));
    drawFrame(fi);
    updatePanels(progress);

    const currentScrollY = window.scrollY;
    scrollDirection = currentScrollY > lastScrollY ? 'down' : 'up';
    lastScrollY = currentScrollY;

    if (currentScrollY < 60) {
      nav.classList.add("nav--visible");
      nav.classList.remove("nav--hidden");
    } else if (scrollDirection === 'down') {
      nav.classList.add("nav--hidden");
      nav.classList.remove("nav--visible");
    } else {
      nav.classList.remove("nav--hidden");
      nav.classList.add("nav--visible");
    }

    latestProgress = progress;
    ticking = false;
  }

  function onScroll() {
    if (!ticking) { window.requestAnimationFrame(updateScene); ticking = true; }
  }

  /* --- Init canvas --- */
  setCanvasSize();
  preloadFrames();
  updateScene();
  function onResize() {
  setCanvasSize();
  latestProgress = -1; // Force redraw even if scroll progress hasn't changed
  updateScene();
}

window.addEventListener("resize", onResize);

// Fix for F11 fullscreen: browser fires fullscreenchange separately from resize
document.addEventListener("fullscreenchange", () => {
  setTimeout(() => { onResize(); }, 50); // Small delay lets browser finish layout
});

// Also handle visibility restore (tab switching, etc.)
document.addEventListener("visibilitychange", () => {
  if (!document.hidden) { latestProgress = -1; updateScene(); }
});
  window.addEventListener("scroll", onScroll, { passive: true });

  /* --- Smooth nav links --- */
  document.querySelectorAll('.nav__links a[href^="#"]').forEach(a => {
    a.addEventListener("click", e => {
      e.preventDefault();
      const t = document.querySelector(a.getAttribute("href"));
      if (t) t.scrollIntoView({ behavior: "smooth" });
    });
  });

  /* === NETWORK INTRUSION DETECTION === */

  // Initialize map
  let map = null;
  let markers = [];
  let detectionInterval = null;
  let isDetecting = false;
  let currentIndex = 0;
  let totalRecords = 0;
  let predictionResults = [];
  let stats = {
    total: 0,
    benign: 0,
    attacks: 0,
    correct: 0
  };

  function initMap() {
    if (map) return;

    map = L.map('map', {
      center: [20, 0],
      zoom: 2,
      minZoom: 1.5,
      zoomSnap: 0.5,
      maxZoom: 10,
      maxBounds: [[-90, -180], [90, 180]],
      maxBoundsViscosity: 1.0
    });

    L.tileLayer('https://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
      maxZoom: 20,
      subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
      attribution: '© Google Maps',
      noWrap: true
    }).addTo(map);
  }

  function addMarker(result) {
    const color = result.predicted_label === 0 ? '#4ade80' : '#ef4444';
    const icon = L.divIcon({
      className: 'custom-marker',
      html: `<div style="background-color: ${color}; width: 12px; height: 12px; border-radius: 50%; border: 2px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3);"></div>`,
      iconSize: [12, 12],
      iconAnchor: [6, 6]
    });

    const marker = L.marker([result.src_lat, result.src_lon], { icon }).addTo(map);

    const statusText = result.predicted_label === 0 ? 'Benign' : 'Attack';
    const actualText = result.actual_label === 0 ? 'Benign' : 'Attack';
    const match = result.predicted_label === result.actual_label ? '' : '';

    marker.bindPopup(`
      <div style="font-family: 'Jost', sans-serif; min-width: 200px;">
        <strong style="color: ${color};">${statusText} Traffic ${match}</strong><br>
        <hr style="margin: 8px 0; border: none; border-top: 1px solid #e5e7eb;">
        <strong>Source:</strong> ${result.src_city}<br>
        <strong>IP:</strong> ${result.src_ip}<br>
        <strong>Destination:</strong> ${result.dst_city}<br>
        <strong>IP:</strong> ${result.dst_ip}<br>
        <hr style="margin: 8px 0; border: none; border-top: 1px solid #e5e7eb;">
        <strong>Predicted:</strong> ${statusText}<br>
        <strong>Actual:</strong> ${actualText}<br>
        <strong>Error:</strong> ${result.reconstruction_error.toFixed(6)}<br>
        <strong>Threshold:</strong> ${result.threshold}<br>
        <small style="color: #6b7280;">${result.timestamp}</small>
      </div>
    `);

    markers.push(marker);

    // Animate marker
    setTimeout(() => {
      marker.openPopup();
      setTimeout(() => marker.closePopup(), 2000);
    }, 100);
  }

  function updateStats() {
    document.getElementById('stat-total').textContent = stats.total;
    document.getElementById('stat-benign').textContent = stats.benign;
    document.getElementById('stat-attacks').textContent = stats.attacks;

    const accuracy = stats.total > 0 ? ((stats.correct / stats.total) * 100).toFixed(2) : 0;
    document.getElementById('stat-accuracy').textContent = accuracy + '%';
  }

  async function startDetection() {
    const modelType = document.getElementById('model-select').value;
    const testSizeSelect = document.getElementById('test-size-select');
    const testSize = testSizeSelect ? parseInt(testSizeSelect.value, 10) : 100;

    // Reset
    stats = { total: 0, benign: 0, attacks: 0, correct: 0 };
    currentIndex = 0;
    predictionResults = [];
    markers.forEach(m => map.removeLayer(m));
    markers = [];

    // Clear recent detections
    const detectionsList = document.getElementById('detections-list');
    detectionsList.innerHTML = '<div class="no-detections">Monitoring network traffic...</div>';

    // Initialize map if needed
    initMap();

    // Show monitoring layout
    document.getElementById('monitoring-layout').style.display = 'grid';

    // Fix map rendering by invalidating size after it becomes visible
    setTimeout(() => {
      if (map) map.invalidateSize();
    }, 100);

    // Disable/enable buttons
    document.getElementById('start-btn').disabled = true;
    document.getElementById('stop-btn').disabled = false;
    document.getElementById('compare-btn').disabled = true;
    document.getElementById('model-select').disabled = true;
    if (testSizeSelect) testSizeSelect.disabled = true;

    isDetecting = true;

    try {
      // Start detection
      const startResp = await fetch('/api/start_detection', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ model_type: modelType, test_size: testSize })
      });

      const startData = await startResp.json();

      if (startData.status === 'started') {
        totalRecords = startData.total_records;

        Swal.fire({
          icon: 'success',
          title: 'Detection Started',
          text: `Monitoring ${totalRecords} network connections with ${modelType.toUpperCase()} model`,
          timer: 2000,
          showConfirmButton: false,
          background: '#111',
          color: '#eee'
        });

        // Start polling for predictions
        detectionInterval = setInterval(getNextPrediction, 500);
      }
    } catch (error) {
      console.error('Error starting detection:', error);
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: 'Failed to start detection: ' + error.message,
        background: '#111',
        color: '#eee'
      });
      stopDetection();
    }
  }

  function addRecentDetection(result) {
    const detectionsList = document.getElementById('detections-list');

    // Remove "no detections" message
    const noDetections = detectionsList.querySelector('.no-detections');
    if (noDetections) {
      noDetections.remove();
    }

    const statusText = result.predicted_label === 0 ? 'Benign' : 'Attack';
    const actualText = result.actual_label === 0 ? 'Benign' : 'Attack';
    const isCorrect = result.predicted_label === result.actual_label;
    const matchClass = isCorrect ? 'detection-match--correct' : 'detection-match--incorrect';
    const matchSymbol = isCorrect ? '✓' : '✗';
    const itemClass = result.predicted_label === 0 ? 'detection-item--benign' : 'detection-item--attack';
    const statusClass = result.predicted_label === 0 ? 'detection-status--benign' : 'detection-status--attack';

    const detectionItem = document.createElement('div');
    detectionItem.className = `detection-item ${itemClass}`;
    detectionItem.innerHTML = `
      <div class="detection-header">
        <span class="detection-status ${statusClass}">${statusText}</span>
        <span class="detection-time">${new Date().toLocaleTimeString()}</span>
      </div>
      <div class="detection-details">
        <strong>${result.src_city}</strong> &rarr; <strong>${result.dst_city}</strong>
        <span class="detection-match ${matchClass}">${matchSymbol}</span>
        <br>
        <small>${result.src_ip} &rarr; ${result.dst_ip}</small>
      </div>
    `;

    // Add to top of list
    detectionsList.insertBefore(detectionItem, detectionsList.firstChild);

    // Keep only last 10 detections
    while (detectionsList.children.length > 10) {
      detectionsList.removeChild(detectionsList.lastChild);
    }
  }

  async function getNextPrediction() {
    if (!isDetecting) return;

    if (currentIndex >= totalRecords && totalRecords > 0) {
      stopDetection();
      document.getElementById('compare-btn').disabled = false;
      Swal.fire({
        icon: 'success',
        title: 'Detection Complete',
        text: `Processed ${currentIndex} connections`,
        background: '#111',
        color: '#eee'
      });
      return;
    }

    const modelType = document.getElementById('model-select').value;

    try {
      const resp = await fetch('/api/get_next_prediction', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ model_type: modelType, index: currentIndex })
      });

      const data = await resp.json();

      if (data.status === 'completed') {
        stopDetection();
        document.getElementById('compare-btn').disabled = false;

        Swal.fire({
          icon: 'success',
          title: 'Detection Complete',
          text: `Processed ${data.total_processed} connections`,
          background: '#111',
          color: '#eee'
        });
        return;
      }

      if (data.status === 'success') {
        const result = data.result;
        predictionResults.push(result);
        currentIndex++;

        // Update stats
        stats.total++;
        if (result.predicted_label === 0) stats.benign++;
        else stats.attacks++;
        if (result.predicted_label === result.actual_label) stats.correct++;

        updateStats();

        // Update progress
        const percentage = totalRecords > 0 ? Math.round((currentIndex / totalRecords) * 100 * 100) / 100 : 0;
        document.getElementById('progress-fill').style.width = percentage + '%';
        document.getElementById('progress-text').textContent =
          `${currentIndex} / ${totalRecords} (${percentage}%)`;

        // Add marker
        addMarker(result);

        // Add to recent detections
        addRecentDetection(result);
      }
    } catch (error) {
      console.error('Error getting prediction:', error);
    }
  }

  async function stopDetection() {
    isDetecting = false;

    if (detectionInterval) {
      clearInterval(detectionInterval);
      detectionInterval = null;
    }

    document.getElementById('start-btn').disabled = false;
    document.getElementById('stop-btn').disabled = true;
    document.getElementById('model-select').disabled = false;
    const testSizeSelect = document.getElementById('test-size-select');
    if (testSizeSelect) testSizeSelect.disabled = false;
  }

  async function showComparison() {
    if (predictionResults.length === 0) {
      Swal.fire({
        icon: 'error',
        title: 'Error',
        text: 'No predictions available',
        background: '#111',
        color: '#eee'
      });
      return;
    }

    const total = predictionResults.length;
    let tp = 0, tn = 0, fp = 0, fn = 0;

    predictionResults.forEach(r => {
      if (r.actual_label === 1 && r.predicted_label === 1) tp++;
      else if (r.actual_label === 0 && r.predicted_label === 0) tn++;
      else if (r.actual_label === 0 && r.predicted_label === 1) fp++;
      else if (r.actual_label === 1 && r.predicted_label === 0) fn++;
    });

    const correct = tp + tn;
    const accuracy = total > 0 ? ((correct / total) * 100).toFixed(2) : 0;
    const precision = (tp + fp) > 0 ? ((tp / (tp + fp)) * 100).toFixed(2) : 0;
    const recall = (tp + fn) > 0 ? ((tp / (tp + fn)) * 100).toFixed(2) : 0;
    const f1_score = (parseFloat(precision) + parseFloat(recall)) > 0
      ? ((2 * parseFloat(precision) * parseFloat(recall)) / (parseFloat(precision) + parseFloat(recall))).toFixed(2)
      : 0;

    const html = `
      <div class="metrics-grid">
        <div class="metric-card">
          <div class="metric-label">Total Predictions</div>
          <div class="metric-value">${total}</div>
        </div>
        <div class="metric-card">
          <div class="metric-label">Accuracy</div>
          <div class="metric-value metric-value--success">${accuracy}%</div>
        </div>
        <div class="metric-card">
          <div class="metric-label">Precision</div>
          <div class="metric-value">${precision}%</div>
        </div>
        <div class="metric-card">
          <div class="metric-label">Recall</div>
          <div class="metric-value">${recall}%</div>
        </div>
        <div class="metric-card">
          <div class="metric-label">F1 Score</div>
          <div class="metric-value">${f1_score}%</div>
        </div>
      </div>
      
      <h3 style="margin-top: 2rem; margin-bottom: 1rem;">Confusion Matrix</h3>
      <div class="confusion-matrix">
        <div class="cm-row">
          <div class="cm-cell cm-header"></div>
          <div class="cm-cell cm-header">Predicted Benign</div>
          <div class="cm-cell cm-header">Predicted Attack</div>
        </div>
        <div class="cm-row">
          <div class="cm-cell cm-header">Actual Benign</div>
          <div class="cm-cell cm-value cm-tn">${tn}</div>
          <div class="cm-cell cm-value cm-fp">${fp}</div>
        </div>
        <div class="cm-row">
          <div class="cm-cell cm-header">Actual Attack</div>
          <div class="cm-cell cm-value cm-fn">${fn}</div>
          <div class="cm-cell cm-value cm-tp">${tp}</div>
        </div>
      </div>
    `;

    document.getElementById('comparison-metrics').innerHTML = html;
    document.getElementById('comparison-modal').classList.add('active');
  }

  async function resetDetection() {
    stopDetection();

    stats = { total: 0, benign: 0, attacks: 0, correct: 0 };
    currentIndex = 0;
    totalRecords = 0;
    predictionResults = [];
    markers.forEach(m => map.removeLayer(m));
    markers = [];

    updateStats();

    document.getElementById('progress-fill').style.width = '0%';
    document.getElementById('progress-text').textContent = '0 / 0 (0%)';
    document.getElementById('monitoring-layout').style.display = 'none';
    document.getElementById('compare-btn').disabled = true;

    // Reset recent detections
    const detectionsList = document.getElementById('detections-list');
    detectionsList.innerHTML = '<div class="no-detections">No detections yet. Start monitoring to see live results.</div>';

    Swal.fire({
      icon: 'info',
      title: 'Reset Complete',
      text: 'Detection system has been reset',
      timer: 1500,
      showConfirmButton: false,
      background: '#111',
      color: '#eee'
    });
  }

  // Event listeners
  document.getElementById('start-btn').addEventListener('click', startDetection);
  document.getElementById('stop-btn').addEventListener('click', stopDetection);
  document.getElementById('compare-btn').addEventListener('click', showComparison);
  document.getElementById('reset-btn').addEventListener('click', resetDetection);

  document.getElementById('comparison-close').addEventListener('click', () => {
    document.getElementById('comparison-modal').classList.remove('active');
  });

  document.getElementById('comparison-modal').addEventListener('click', (e) => {
    if (e.target.id === 'comparison-modal') {
      document.getElementById('comparison-modal').classList.remove('active');
    }
  });

  // Initialize map on page load
  setTimeout(initMap, 1000);

})();