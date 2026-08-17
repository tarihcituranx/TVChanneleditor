document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('upload-section');
    const fileInput = document.getElementById('file-input');
    const browseBtn = document.getElementById('browse-btn');
    const editorSection = document.getElementById('editor-section');
    const channelList = document.getElementById('channel-list');
    const saveBtn = document.getElementById('save-btn');
    const searchInput = document.getElementById('search-input');

    let channels = [];
    let currentFileName = "channel_list.scm";
    let frekansData = {};

    // Güncel frekansları yükle
    fetch('/static/data/frekanslar.json')
        .then(res => res.json())
        .then(data => {
            frekansData = data;
        })
        .catch(err => console.log('Frekans datası bulunamadı', err));

    // Drag & Drop Upload
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        if (e.dataTransfer.files.length) {
            handleFile(e.dataTransfer.files[0]);
        }
    });

    browseBtn.addEventListener('click', () => fileInput.click());
    
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            handleFile(e.target.files[0]);
        }
    });

    function handleFile(file) {
        if (!file.name.endsWith('.scm')) {
            alert('Lütfen geçerli bir .scm dosyası yükleyin.');
            return;
        }
        
        currentFileName = file.name;

        const formData = new FormData();
        formData.append('file', file);

        browseBtn.textContent = 'Yükleniyor...';

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                browseBtn.textContent = 'Dosya Seç';
                return;
            }
            channels = data.channels;
            renderChannels();
            dropZone.classList.add('hidden');
            editorSection.classList.remove('hidden');
        })
        .catch(err => {
            console.error(err);
            alert('Yükleme sırasında hata oluştu.');
            browseBtn.textContent = 'Dosya Seç';
        });
    }

    function renderChannels(filter = '') {
        channelList.innerHTML = '';
        
        let filtered = channels;
        if (filter) {
            filtered = channels.filter(c => c.Name.toLowerCase().includes(filter.toLowerCase()));
        }

        filtered.forEach((ch, index) => {
            const li = document.createElement('li');
            li.draggable = true;
            li.dataset.index = channels.indexOf(ch);
            
            let freqWarning = '';
            let freqColor = '';
            const chNameUp = ch.Name.toUpperCase();
            if (frekansData[chNameUp]) {
                const updatedFreq = frekansData[chNameUp];
                if (parseInt(ch.Freq) !== parseInt(updatedFreq)) {
                    freqWarning = ` <span title="Doğru Frekans: ${updatedFreq}" style="color:red; font-size:12px;">⚠️ Eski Frekans (${updatedFreq} olmalı)</span>`;
                    freqColor = 'color: #ff4d4d;';
                } else {
                    freqWarning = ` <span title="Frekans Güncel" style="color:#00ff00; font-size:12px;">✅</span>`;
                }
            }
            
            li.innerHTML = `
                <div class="col-drag">⋮⋮</div>
                <div class="col-check"><input type="checkbox" class="row-checkbox" data-idx="${li.dataset.index}"></div>
                <div class="col-no">${index + 1}</div>
                <div class="col-name">${ch.Name}</div>
                <div class="col-type">${ch.Type}</div>
                <div class="col-freq" style="${freqColor}">${ch.Freq} ${ch.Pol} ${ch.Sym}${freqWarning}</div>
                <div class="col-action">
                    <button class="delete-btn" onclick="deleteChannel(${li.dataset.index})">✕</button>
                </div>
            `;
            
            // Checkbox tracking logic
            const cb = li.querySelector('.row-checkbox');
            if (selectedIndices.has(parseInt(li.dataset.index))) {
                cb.checked = true;
            }
            cb.addEventListener('change', (e) => {
                const globalIdx = parseInt(e.target.dataset.idx);
                if (e.target.checked) selectedIndices.add(globalIdx);
                else selectedIndices.delete(globalIdx);
                updateSelectedCount();
            });

            // Drag and Drop ordering
            li.addEventListener('dragstart', handleDragStart);
            li.addEventListener('dragover', handleDragOver);
            li.addEventListener('drop', handleDrop);
            li.addEventListener('dragend', handleDragEnd);

            channelList.appendChild(li);
        });
    }

    let dragSrcEl = null;

    function handleDragStart(e) {
        dragSrcEl = this;
        e.dataTransfer.effectAllowed = 'move';
        e.dataTransfer.setData('text/html', this.innerHTML);
        this.classList.add('dragging');
    }

    function handleDragOver(e) {
        if (e.preventDefault) { e.preventDefault(); }
        e.dataTransfer.dropEffect = 'move';
        return false;
    }

    function handleDrop(e) {
        if (e.stopPropagation) { e.stopPropagation(); }
        if (dragSrcEl !== this) {
            const srcIndex = parseInt(dragSrcEl.dataset.index);
            const tgtIndex = parseInt(this.dataset.index);
            
            // Reorder array
            const item = channels.splice(srcIndex, 1)[0];
            channels.splice(tgtIndex, 0, item);
            
            renderChannels(searchInput.value);
        }
        return false;
    }

    function handleDragEnd(e) {
        this.classList.remove('dragging');
    }

    window.deleteChannel = function(index) {
        channels.splice(index, 1);
        renderChannels(searchInput.value);
    }

    searchInput.addEventListener('input', (e) => {
        renderChannels(e.target.value);
    });

    // 1. Magic Wand & Custom Templates
    let TEMPLATES = {};

    // Asenkron olarak harici JSON dosyasından hazır şablonları yükle
    fetch('static/data/templates.json')
        .then(res => res.json())
        .then(data => {
            TEMPLATES = data;
        })
        .catch(err => console.error("Şablonlar yüklenirken hata oluştu:", err));

    const magicBtn = document.getElementById('magic-wand-btn');
    const modal = document.getElementById('magic-modal');
    const closeBtn = document.getElementById('close-modal-btn');
    const applyBtn = document.getElementById('apply-template-btn');
    const saveTemplateBtn = document.getElementById('save-template-btn');
    const customContainer = document.getElementById('custom-templates-container');
    const customCardsContainer = document.getElementById('custom-cards-container');
    
    let selectedTemplate = 'general';

    function loadCustomTemplates() {
        customCardsContainer.innerHTML = '';
        let hasCustom = false;
        
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key.startsWith('scm_custom_')) {
                hasCustom = true;
                const templateName = key.replace('scm_custom_', '');
                const list = JSON.parse(localStorage.getItem(key));
                TEMPLATES[key] = list;

                const previewText = list.slice(0, 5).map((name, idx) => `${idx+1}. ${name}`).join(' | ') + '...';

                const card = document.createElement('div');
                card.className = 'template-card';
                card.dataset.template = key;
                card.innerHTML = `
                    <h3>💾 ${templateName} (Kendi Şablonum)</h3>
                    <p>${list.length} kanallık özel diziliminiz.</p>
                    <div class="preview">${previewText}</div>
                `;
                
                card.addEventListener('click', () => {
                    document.querySelectorAll('.template-card').forEach(c => c.classList.remove('selected'));
                    card.classList.add('selected');
                    selectedTemplate = key;
                });

                customCardsContainer.appendChild(card);
            }
        }
        
        customContainer.style.display = hasCustom ? 'block' : 'none';
    }

    // Modal açılırken listeleri güncelle
    magicBtn.addEventListener('click', () => {
        loadCustomTemplates();
        
        // Yeniden event listener ekle (hazır şablonlar için)
        document.querySelectorAll('#template-cards-container > .template-card').forEach(card => {
            // Remove existing listener to prevent duplicates if possible, or just re-assign onclick
            card.onclick = () => {
                document.querySelectorAll('.template-card').forEach(c => c.classList.remove('selected'));
                card.classList.add('selected');
                selectedTemplate = card.dataset.template;
            };
        });
        
        modal.classList.remove('hidden');
    });

    closeBtn.addEventListener('click', () => {
        modal.classList.add('hidden');
    });

    const delSelectedBtn = document.getElementById('delete-selected-btn');
    const selectAllCheckbox = document.getElementById('select-all');
    const selCountSpan = document.getElementById('sel-count');

    // Builder elements
    const builderModal = document.getElementById('builder-modal');
    const closeBuilderBtn = document.getElementById('close-builder-btn');
    const saveBuilderBtn = document.getElementById('save-builder-btn');
    const builderSourceList = document.getElementById('builder-source-list');
    const builderTargetList = document.getElementById('builder-target-list');
    let builderCart = [];

    // Checkbox state tracking
    let selectedIndices = new Set();

    function updateSelectedCount() {
        selCountSpan.textContent = selectedIndices.size;
        delSelectedBtn.style.display = selectedIndices.size > 0 ? 'inline-block' : 'none';
    }

    selectAllCheckbox.addEventListener('change', (e) => {
        const isChecked = e.target.checked;
        selectedIndices.clear();
        if (isChecked) {
            channels.forEach((_, i) => selectedIndices.add(i));
        }
        document.querySelectorAll('.row-checkbox').forEach(cb => cb.checked = isChecked);
        updateSelectedCount();
    });

    delSelectedBtn.addEventListener('click', () => {
        if (!confirm(`${selectedIndices.size} adet kanalı silmek istediğinize emin misiniz?`)) return;
        
        // Remove from highest index to lowest to avoid shifting issues
        let indices = Array.from(selectedIndices).sort((a, b) => b - a);
        indices.forEach(idx => {
            channels.splice(idx, 1);
        });
        
        selectedIndices.clear();
        selectAllCheckbox.checked = false;
        renderChannels(searchInput.value);
        updateSelectedCount();
    });

    saveTemplateBtn.addEventListener('click', () => {
        if (channels.length === 0) {
            alert('Lütfen önce bir SCM dosyası yükleyin.');
            return;
        }
        builderCart = [];
        renderBuilderLists();
        builderModal.classList.remove('hidden');
    });

    closeBuilderBtn.addEventListener('click', () => {
        builderModal.classList.add('hidden');
    });

    function renderBuilderLists() {
        builderSourceList.innerHTML = '';
        builderTargetList.innerHTML = '';

        channels.forEach((ch, idx) => {
            const li = document.createElement('li');
            li.textContent = `${ch.No}. ${ch.Name} (${ch.Type})`;
            li.onclick = () => {
                builderCart.push(ch);
                renderBuilderLists();
            };
            builderSourceList.appendChild(li);
        });

        builderCart.forEach((ch, idx) => {
            const li = document.createElement('li');
            li.innerHTML = `<b>${idx + 1}.</b> ${ch.Name}`;
            li.onclick = () => {
                builderCart.splice(idx, 1);
                renderBuilderLists();
            };
            builderTargetList.appendChild(li);
        });
    }

    saveBuilderBtn.addEventListener('click', () => {
        if (builderCart.length === 0) {
            alert('Sepetiniz boş! Lütfen soldan sağa kanal ekleyin.');
            return;
        }
        const tName = prompt('Bu mükemmel şablona ne isim vermek istersiniz?');
        if (!tName) return;

        const customList = builderCart.map(c => c.Name);
        localStorage.setItem('scm_custom_' + tName, JSON.stringify(customList));
        builderModal.classList.add('hidden');
        alert('Şablon başarıyla tarayıcınıza kaydedildi! Sihirli Değnek menüsünden tek tıkla çağırabilirsiniz.');
    });

    applyBtn.addEventListener('click', () => {
        const refList = TEMPLATES[selectedTemplate];
        if (!refList) return;
        
        let newOrder = [];
        let remaining = [...channels];

        refList.forEach(refName => {
            const idx = remaining.findIndex(c => c.Name.toUpperCase() === refName.toUpperCase());
            if (idx !== -1) {
                newOrder.push(remaining[idx]);
                remaining.splice(idx, 1);
            }
        });

        channels = [...newOrder, ...remaining];
        renderChannels(searchInput.value);
        modal.classList.add('hidden');
        alert('Seçtiğiniz şablon başarıyla uygulandı! ✨');
    });

    // 2. Delete Encrypted
    document.getElementById('del-encrypted-btn').addEventListener('click', () => {
        if (!confirm('Tüm şifreli kanallar kalıcı olarak silinecek. Emin misiniz?')) return;
        const initialCount = channels.length;
        channels = channels.filter(c => c.Encrypted === 'No');
        const deleted = initialCount - channels.length;
        renderChannels(searchInput.value);
        alert(`${deleted} adet şifreli kanal silindi!`);
    });

    // 3. Delete Radios
    document.getElementById('del-radio-btn').addEventListener('click', () => {
        if (!confirm('Tüm radyo kanalları kalıcı olarak silinecek. Emin misiniz?')) return;
        const initialCount = channels.length;
        channels = channels.filter(c => c.Type !== 'Radio');
        const deleted = initialCount - channels.length;
        renderChannels(searchInput.value);
        alert(`${deleted} adet radyo kanalı silindi!`);
    });

    // --- END NEW FEATURES ---

    saveBtn.addEventListener('click', () => {
        saveBtn.textContent = 'Kaydediliyor...';
        
        fetch('/build', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ channels: channels, filename: currentFileName })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                window.location.href = data.download_url;
                saveBtn.textContent = 'Kaydet ve İndir';
            } else {
                alert('Oluşturma hatası: ' + data.error);
                saveBtn.textContent = 'Kaydet ve İndir';
            }
        })
        .catch(err => {
            console.error(err);
            alert('Bir hata oluştu.');
            saveBtn.textContent = 'Kaydet ve İndir';
        });
    });
});
