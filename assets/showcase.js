(() => {
  'use strict';

  const THEMES = ['terminal-dark', 'light-pastel'];
  const THEME_NAMES = {'terminal-dark': '暖黑', 'light-pastel': '暖纸'};
  const THEME_KEY = 'live-panel-studio-showcase-theme';
  const $ = (id) => document.getElementById(id);
  let theme = 'terminal-dark';
  let demos = [];
  let exports = [];

  // Relative, same-origin assets continue to work under a GitHub Pages project path.
  function asset(path) {
    if (typeof path !== 'string' || !path.trim() || /[\\\u0000-\u001f]/.test(path)) throw new Error('无效媒体路径');
    const url = new URL(path, document.baseURI);
    const root = new URL('./', document.baseURI);
    if (url.origin !== root.origin || !url.pathname.startsWith(root.pathname)) throw new Error('媒体路径超出站点目录');
    return url.href;
  }

  function node(tag, className, text) {
    const el = document.createElement(tag);
    if (className) el.className = className;
    if (text !== undefined) el.textContent = text;
    return el;
  }

  function durationLabel(seconds) {
    return `${Math.round(Number(seconds || 12) * 10) / 10}s`;
  }

  function link(label, path, download = false) {
    const el = node('a', '', label);
    el.href = asset(path);
    if (download) el.setAttribute('download', '');
    return el;
  }

  function wireVideo(video, error) {
    video.controls = true;
    video.playsInline = true;
    video.preload = 'none';
    video.addEventListener('play', () => {
      document.querySelectorAll('video').forEach((other) => { if (other !== video) other.pause(); });
      if (error) error.hidden = true;
    });
    video.addEventListener('error', () => {
      if (!error) return;
      error.textContent = '视频暂时无法播放，可通过下载链接查看文件。';
      error.hidden = false;
    });
  }

  function setMedia(video, source, poster, error) {
    video.pause();
    if (error) error.hidden = true;
    const next = asset(source);
    if (video.getAttribute('src') !== next) {
      video.src = next;
      if (poster) video.poster = asset(poster);
      else video.removeAttribute('poster');
      video.load();
    }
  }

  function mediaCard(item, index, recreation = false) {
    const card = node('article', 'media-card');
    if (recreation) card.style.setProperty('--media-aspect', `${item.width || 1280}/${item.height || 800}`);
    const head = node('div', 'media-card-head');
    head.append(node('span', 'media-index', `${recreation ? 'REFERENCE' : 'SCENE'} / ${String(index + 1).padStart(2, '0')}`), node('span', 'media-category', item.category || (item.avatar === 'spider' ? '机械蜘蛛版本' : '机器人版本')));
    const frame = node('div', 'media-frame');
    const video = node('video');
    const error = node('p', 'media-error');
    error.hidden = true;
    error.setAttribute('role', 'status');
    video.setAttribute('aria-label', `${item.title}视频`);
    wireVideo(video, error);
    frame.append(video, error);
    const body = node('div', 'media-card-body');
    body.append(node('h3', '', item.title), node('p', '', item.summary || '由配置与时间线生成的动画。'));
    const meta = node('div', 'media-meta');
    meta.append(node('span', '', durationLabel(item.duration)), node('span', '', `${item.fps || 30}fps`), node('span', 'card-theme', THEME_NAMES[recreation ? item.theme : theme] || THEME_NAMES[theme]));
    const links = node('div', 'media-links');
    if (recreation) {
      setMedia(video, item.video, item.poster, error);
      links.append(link('下载 MP4 ↓', item.video, true), node('span', '', '参考画面重新实现'));
      if (item.provenance) card.title = item.provenance;
    } else {
      card.dataset.scene = item.id;
      links.append(link('交互体验 ↗', `examples/capability-demos/index.html#${encodeURIComponent(item.id)}`), link('下载 MP4 ↓', demoVideo(item), true));
      links.lastChild.classList.add('demo-download');
      setMedia(video, demoVideo(item), demoPoster(item), error);
    }
    body.append(meta, links);
    card.append(head, frame, body);
    return card;
  }

  function demoVideo(item) {
    const filename = item.videos?.[theme] || (theme === 'light-pastel' ? 'demo-light.mp4' : 'demo.mp4');
    return `examples/capability-demos/${item.id}/${filename}`;
  }

  function demoPoster(item) {
    return `examples/capability-demos/${item.id}/${theme === 'light-pastel' ? 'poster-light.png' : 'poster.png'}`;
  }

  function applyTheme(next, announce = true) {
    if (!THEMES.includes(next)) return;
    theme = next;
    document.documentElement.dataset.theme = theme;
    document.querySelector('meta[name="theme-color"]').content = theme === 'light-pastel' ? '#f2efe6' : '#11110f';
    document.querySelectorAll('[data-theme-choice]').forEach((button) => button.setAttribute('aria-pressed', String(button.dataset.themeChoice === theme)));
    try { localStorage.setItem(THEME_KEY, theme); } catch (_) { /* Private sessions can disable storage. */ }
    demos.forEach((item) => {
      const card = document.querySelector(`[data-scene="${item.id}"]`);
      if (!card) return;
      setMedia(card.querySelector('video'), demoVideo(item), demoPoster(item), card.querySelector('.media-error'));
      card.querySelector('.demo-download').href = asset(demoVideo(item));
      card.querySelector('.card-theme').textContent = THEME_NAMES[theme];
    });
    if (announce) $('page-status').textContent = `已切换为${THEME_NAMES[theme]}主题，八个 Demo 将播放对应主题的成片。`;
  }

  function rangeLabel(item) {
    if (item.view === 'full') return '整段 Demo';
    return (item.label || item.view).replace(/\s*·\s*(机器人|机械蜘蛛|蜘蛛)\s*$/, '');
  }

  function labelFor(item) {
    const role = item.avatar === 'drone' ? '机器人' : '蜘蛛';
    return `${rangeLabel(item)} · ${THEME_NAMES[item.theme] || item.theme} · ${role}`;
  }

  function selectExport(item) {
    if (!item) return;
    $('export-scene').value = item.scene;
    const cases = exports.filter((entry) => entry.scene === item.scene);
    $('export-case').replaceChildren(...cases.map((entry) => {
      const option = node('option', '', labelFor(entry));
      option.value = entry.id;
      return option;
    }));
    $('export-case').value = item.id;
    $('export-title').textContent = item.title;
    $('export-summary').textContent = item.summary || (item.method === 'crop' ? '由对应完整成片裁剪，保留功能块动画。' : '由当前配置逐帧渲染。');
    $('export-view').textContent = item.view === 'full' ? '整个 Demo' : rangeLabel(item);
    $('export-variant').textContent = `${THEME_NAMES[item.theme] || item.theme} / ${item.avatar === 'drone' ? '机器人' : '机械蜘蛛'}`;
    $('export-dimensions').textContent = `${item.width} × ${item.height}`;
    $('export-timing').textContent = `${durationLabel(item.duration)} / ${item.fps} fps`;
    $('export-stage-label').textContent = `${item.scene.toUpperCase()} / ${item.view.toUpperCase()}`;
    const video = $('export-video');
    video.style.setProperty('--media-aspect', `${item.width}/${item.height}`);
    video.setAttribute('aria-label', `${item.title}视频`);
    setMedia(video, item.video, item.poster, $('export-error'));
    $('export-download').href = asset(item.video);
    $('export-download').hidden = false;
  }

  function renderExports(items) {
    exports = items;
    if (!items.length) {
      $('export-count').textContent = '暂无案例';
      $('export-summary').textContent = '导出案例尚未发布。可以先观看上面的能力示例。';
      return;
    }
    $('export-count').textContent = `${items.length} 段成片`;
    const scenes = new Map(items.map((entry) => [entry.scene, entry.sceneTitle || entry.scene]));
    $('export-scene').replaceChildren(...Array.from(scenes, ([id, title]) => {
      const option = node('option', '', title);
      option.value = id;
      return option;
    }));
    $('export-scene').disabled = false;
    $('export-case').disabled = false;
    $('export-scene').addEventListener('change', () => selectExport(items.find((entry) => entry.scene === $('export-scene').value)));
    $('export-case').addEventListener('change', () => selectExport(items.find((entry) => entry.id === $('export-case').value)));
    const featured = [
      ['full', '整段 · 机器人'],
      ['rag-hero', '主流程 · 机器人'],
      ['rag-rerank', '重排 · 机器人'],
    ].map(([view, label]) => ({item: items.find((entry) => entry.scene === 'rag-explainer' && entry.view === view && entry.avatar === 'drone'), label})).filter((entry) => entry.item);
    $('export-quick-links').replaceChildren(...featured.map(({item, label}) => {
      const button = node('button', '', label);
      button.type = 'button';
      button.addEventListener('click', () => selectExport(item));
      return button;
    }));
    selectExport(featured.find((entry) => entry.item.view === 'rag-hero')?.item || featured[0]?.item || items[0]);
  }

  async function getJson(path) {
    const response = await fetch(asset(path), {credentials: 'same-origin'});
    if (!response.ok) throw new Error(`读取失败：${response.status}`);
    return response.json();
  }

  async function loadDemos() {
    try {
      demos = await getJson('examples/capability-demos/manifest.json');
      if (!Array.isArray(demos)) throw new Error('无效的示例清单');
      $('demo-grid').replaceChildren(...demos.map((item, index) => mediaCard(item, index)));
    } catch (_) {
      const message = node('p', 'loading-message', '示例清单暂时无法加载。');
      message.append(document.createTextNode(' '), link('打开交互体验馆 ↗', 'examples/capability-demos/index.html'));
      $('demo-grid').replaceChildren(message);
    }
  }

  async function loadCatalog() {
    try {
      const catalog = await getJson('media/catalog.json');
      if (!Array.isArray(catalog.recreations) || !Array.isArray(catalog.exports)) throw new Error('无效的媒体清单');
      $('recreation-grid').replaceChildren(...catalog.recreations.map((item, index) => mediaCard(item, index, true)));
      if (!catalog.recreations.length) $('recreation-grid').append(node('p', 'loading-message', '复刻成片尚未发布。'));
      renderExports(catalog.exports);
    } catch (_) {
      $('recreation-grid').replaceChildren(node('p', 'loading-message', '媒体清单暂时无法加载，请稍后刷新。'));
      $('export-count').textContent = '读取失败';
      $('export-summary').textContent = '导出案例暂时无法读取。上方的能力示例仍可播放。';
    }
  }

  wireVideo($('export-video'), $('export-error'));
  try { const saved = localStorage.getItem(THEME_KEY); if (THEMES.includes(saved)) theme = saved; } catch (_) { /* Use the default without storage. */ }
  applyTheme(theme, false);
  document.querySelectorAll('[data-theme-choice]').forEach((button) => button.addEventListener('click', () => applyTheme(button.dataset.themeChoice)));
  Promise.allSettled([loadDemos(), loadCatalog()]);
})();
