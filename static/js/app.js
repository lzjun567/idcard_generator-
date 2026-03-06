'use strict';

/* ===== 页面初始化 ===== */
document.addEventListener('DOMContentLoaded', () => {
  setupUploadArea();
  setupForm();
  setupTabs();
  loadRandomData(); // 页面加载时自动填入随机数据
});

/* ===== 随机数据 ===== */
function loadRandomData() {
  const btn = document.getElementById('randomBtn');
  btn.disabled = true;
  btn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>生成中…';

  fetch('/api/random')
    .then(r => r.json())
    .then(data => fillForm(data))
    .catch(() => alert('获取随机数据失败，请刷新后重试'))
    .finally(() => {
      btn.disabled = false;
      btn.innerHTML = '<i class="fas fa-shuffle me-1"></i>随机填充';
    });
}

function fillForm(data) {
  setVal('name',  data.name  ?? '');
  setVal('nation', data.nation ?? '汉');
  setVal('year',  data.year  ?? '');
  setVal('month', data.month ?? '');
  setVal('day',   data.day   ?? '');
  setVal('addr',  data.addr  ?? '');
  setVal('idn',   data.idn   ?? '');
  setVal('org',   data.org   ?? '');
  setVal('life',  data.life  ?? '');

  const sexEl = document.getElementById('sex');
  if (data.sex === '女') {
    sexEl.value = '女';
  } else {
    sexEl.value = '男';
  }
}

function setVal(id, val) {
  const el = document.getElementById(id);
  if (el) el.value = val;
}

/* ===== 头像上传 ===== */
function setupUploadArea() {
  const uploadArea    = document.getElementById('uploadArea');
  const avatarInput   = document.getElementById('avatarInput');
  const avatarPreview = document.getElementById('avatarPreview');

  // 点击上传
  uploadArea.addEventListener('click', () => avatarInput.click());

  // 键盘无障碍
  uploadArea.addEventListener('keydown', e => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      avatarInput.click();
    }
  });

  // 拖拽
  uploadArea.addEventListener('dragover', e => {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
  });
  uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('drag-over');
  });
  uploadArea.addEventListener('drop', e => {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      setAvatarFile(file);
    } else {
      alert('请上传图片文件（JPG / PNG）');
    }
  });

  // 文件选择
  avatarInput.addEventListener('change', e => {
    const file = e.target.files[0];
    if (file) setAvatarFile(file);
  });

  function setAvatarFile(file) {
    // 更新 input files（拖拽时需要手动替换）
    const dt = new DataTransfer();
    dt.items.add(file);
    avatarInput.files = dt.files;

    // 预览
    const reader = new FileReader();
    reader.onload = ev => {
      avatarPreview.src = ev.target.result;
      avatarPreview.style.display = 'block';
      uploadArea.classList.add('has-image');
    };
    reader.readAsDataURL(file);
  }
}

/* ===== 表单提交 ===== */
function setupForm() {
  document.getElementById('randomBtn').addEventListener('click', loadRandomData);

  document.getElementById('generateForm').addEventListener('submit', e => {
    e.preventDefault();
    generateIdCard();
  });
}

function generateIdCard() {
  const avatarInput = document.getElementById('avatarInput');
  if (!avatarInput.files || avatarInput.files.length === 0) {
    alert('请先上传头像图片');
    return;
  }

  showState('loading');

  // 手动构建 FormData，避免 form 内无 name 属性的 file input 被漏掉
  const form = document.getElementById('generateForm');
  const formData = new FormData();
  formData.append('avatar', avatarInput.files[0]);
  formData.append('name',   form.name.value);
  formData.append('sex',    form.sex.value);
  formData.append('nation', form.nation.value);
  formData.append('year',   form.year.value);
  formData.append('month',  form.month.value);
  formData.append('day',    form.day.value);
  formData.append('addr',   form.addr.value);
  formData.append('idn',    form.idn.value);
  formData.append('org',    form.org.value);
  formData.append('life',   form.life.value);
  formData.append('use_matting', document.getElementById('useMatting').checked ? 'true' : 'false');

  fetch('/api/generate', { method: 'POST', body: formData })
    .then(r => r.json().then(data => ({ ok: r.ok, data })))
    .then(({ ok, data }) => {
      if (!ok || data.error) {
        alert('生成失败：' + (data.error || '未知错误'));
        showState('empty');
        return;
      }

      document.getElementById('colorResult').src = data.color;
      document.getElementById('bwResult').src    = data.bw;
      document.getElementById('downloadColor').href = data.color;
      document.getElementById('downloadBw').href    = data.bw;

      showState('result');
      showTab('color');
    })
    .catch(err => {
      alert('请求失败：' + err.message);
      showState('empty');
    });
}

/* ===== 状态切换 ===== */
function showState(state) {
  document.getElementById('emptyState').style.display   = state === 'empty'   ? '' : 'none';
  document.getElementById('loadingState').style.display = state === 'loading'  ? '' : 'none';
  document.getElementById('resultState').style.display  = state === 'result'   ? '' : 'none';
}

/* ===== Tab 切换 ===== */
function setupTabs() {
  document.querySelectorAll('[data-tab]').forEach(btn => {
    btn.addEventListener('click', () => showTab(btn.dataset.tab));
  });
}

function showTab(tab) {
  document.querySelectorAll('[data-tab]').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.tab === tab);
  });
  document.getElementById('colorResult').style.display = tab === 'color' ? '' : 'none';
  document.getElementById('bwResult').style.display    = tab === 'bw'    ? '' : 'none';
}
