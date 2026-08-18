window.toast = function(message, type = 'success') {
        const el = document.createElement('div');
        el.className = `toast toast-${type}`;
        el.textContent = message;
        document.getElementById('toast-container').appendChild(el);
        requestAnimationFrame(() => el.classList.add('show'));
        setTimeout(() => {
            el.classList.remove('show');
            el.addEventListener('transitionend', () => el.remove());
        }, 3200);
    };

document.addEventListener('DOMContentLoaded', () => {
    console.log('%c Crafted by @tarihcituranx 🚀 ', 'background: #0d1117; color: #58a6ff; font-size: 14px; padding: 6px 12px; border-radius: 4px; font-family: monospace; border: 1px solid #30363d;');
    
    const dropZone = document.getElementById('upload-section');
    const fileInput = document.getElementById('file-input');
    const browseBtn = document.getElementById('browse-btn');
    const editorSection = document.getElementById('editor-section');
    const channelList = document.getElementById('channel-list');
    const saveBtn = document.getElementById('save-btn');
    const searchInput = document.getElementById('search-input');

    let selectedIndices = new Set();
    let channels = [];
    let currentFileName = "channel_list.scm";
    let currentSessionId = "";
    let frekansData = {};
    let isRestoringDraft = false;

    function saveDraftToLocal() {
        if (isRestoringDraft || channels.length === 0) return;
        const draft = {
            channels: channels,
            currentFileName: currentFileName,
            currentSessionId: currentSessionId,
            timestamp: new Date().getTime()
        };
        localStorage.setItem('channel_draft', JSON.stringify(draft));
    }

    function checkDraftOnLoad() {
        const draftStr = localStorage.getItem('channel_draft');
        if (draftStr) {
            try {
                const draft = JSON.parse(draftStr);
                if (draft.channels && draft.channels.length > 0) {
                    if (confirm('Kaydedilmemiş bir kanal düzenleme taslağınız var. Kaldığınız yerden devam etmek ister misiniz?')) {
                        isRestoringDraft = true;
                        channels = draft.channels;
                        currentFileName = draft.currentFileName;
                        currentSessionId = draft.currentSessionId;
                        
                        // Dosya yükleme ekranını gizle, editörü göster
                        dropZone.classList.add('hidden');
                        editorSection.classList.remove('hidden');
                        
                        renderChannels();
                        isRestoringDraft = false;
                    } else {
                        localStorage.removeItem('channel_draft');
                    }
                }
            } catch (e) {
                console.error("Draft restore error", e);
            }
        }
    }

    /**
     * LG/Sony/Hisense küçük harfli alanları (id, num, name, type, freq...)
     * Samsung/Tizen büyük harfli alanlara (Slot, No, Name, Type, Freq...) normalize et.
     * Samsung/Tizen zaten doğru formatta gelir, sadece eksik alanlar doldurulur.
     */
    function normalizeChannel(ch, index) {
        // Zaten büyük harfli (Samsung/Tizen) ise, eksikleri tamamla ve dön
        if ('Name' in ch) {
            if (!('Slot' in ch)) ch.Slot = ch.Slot ?? index;
            if (!('Freq' in ch)) ch.Freq = '';
            if (!('Pol'  in ch)) ch.Pol  = '';
            if (!('Sym'  in ch)) ch.Sym  = '';
            return ch;
        }
        // Küçük harfli (LG/Sony/Hisense) → büyük harfle eşle
        return {
            Slot:      ch.id      ?? index,
            No:        ch.num     ?? index + 1,
            Name:      ch.name    ?? '',
            Type:      ch.type    ?? '',
            Freq:      ch.freq    ?? '',
            Pol:       ch.pol     ?? '',
            Sym:       ch.sym     ?? '',
            Lock:      ch.lock    ?? false,
            Hide:      ch.hide    ?? false,
            Skip:      ch.skip    ?? false,
            Encrypted: ch.encrypted ?? 'No',
            Fav1:      ch.fav1   ?? false,
            Fav2:      ch.fav2   ?? false,
            Fav3:      ch.fav3   ?? false,
            Fav4:      ch.fav4   ?? false,
            Fav5:      ch.fav5   ?? false,
            SID:       ch.sid    ?? undefined,
            TSID:      ch.tsid   ?? undefined,
            ONID:      ch.onid   ?? undefined,
            VidPID:    ch.vidpid ?? undefined,
            PcrPID:    ch.pcrpid ?? undefined,
            // build sırasında backend küçük harfli alanları okuyabilsin diye orijinali sakla
            _brand_fields: ch,
        };
    }

    // Güncel frekansları yükle
    fetch('/static/data/frekanslar.json')
        .then(res => res.json())
        .then(data => {
            frekansData = data;
            checkDraftOnLoad();
        })
        .catch(err => {
            console.log('Frekans datası bulunamadı', err);
            checkDraftOnLoad();
        });

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

    if (browseBtn) {
        browseBtn.addEventListener('click', () => fileInput.click());
    }
    
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            handleFile(e.target.files[0]);
        }
    });

    function handleFile(file) {
        const nameLower = file.name.toLowerCase();
        if (!nameLower.endsWith('.scm') && !nameLower.endsWith('.zip') && !nameLower.endsWith('.tll') && !nameLower.endsWith('.xml') && !nameLower.endsWith('.db')) {
            toast('Lütfen desteklenen bir dosya formatı yükleyin (.scm, .zip, .tll, sdb.xml, servicelist.db).', 'danger');
            return;
        }
        
        currentFileName = file.name;

        const formData = new FormData();
        formData.append('file', file);

        browseBtn.classList.add('tv-scanning');

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                toast(data.error, 'danger');
                browseBtn.classList.remove('tv-scanning');
                return;
            }
            if (!data.channels || data.channels.length === 0) {
                toast('Geçersiz veya boş kanal listesi! Lütfen doğru formatta bir dosya yükleyin.', 'danger');
                browseBtn.classList.remove('tv-scanning');
                return;
            }
            channels = data.channels.map((ch, i) => normalizeChannel(ch, i));
            currentSessionId = data.session_id;
            showBrandBadge(data.brand, channels.length);
            renderChannels();
            dropZone.classList.add('hidden');
            editorSection.classList.remove('hidden');
        })
        .catch(err => {
            console.error(err);
            toast('An error occurred during upload.', 'danger');
            browseBtn.classList.remove('tv-scanning');
        });
    }

    function escapeHTML(str) {
        return str.replace(/[&<>'"]/g, 
            tag => ({
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                "'": '&#39;',
                '"': '&quot;'
            }[tag] || tag)
        );
    }

    const BRAND_INFO = {
        samsung: { emoji: '🔵', label: 'Samsung TV',  color: '#1428a0' },
        tizen:   { emoji: '🔵', label: 'Samsung Tizen TV', color: '#1428a0' },
        lg:      { emoji: '🔴', label: 'LG TV',       color: '#a50034' },
        sony:    { emoji: '⚫', label: 'Sony TV',     color: '#1a1a1a' },
        hisense: { emoji: '🟠', label: 'Hisense TV',  color: '#e85d00' },
    };

    function showBrandBadge(brand, count) {
        const badgeEl = document.getElementById('brand-badge');
        if (!badgeEl) return;
        const info = BRAND_INFO[brand] || { emoji: '📺', label: brand, color: '#555' };
        badgeEl.innerHTML = `
            <span class="brand-badge-icon">${info.emoji}</span>
            <span class="brand-badge-text">
                <strong>${info.label}</strong> formatı tespit edildi
                &nbsp;·&nbsp; <span class="brand-badge-count">${count} kanal</span>
            </span>
        `;
        badgeEl.style.borderLeftColor = info.color;
        badgeEl.classList.remove('hidden', 'badge-fadeout');
        // 6 saniye sonra fade-out
        clearTimeout(badgeEl._timer);
        badgeEl._timer = setTimeout(() => {
            badgeEl.classList.add('badge-fadeout');
        }, 6000);
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
            li.style.display = 'flex'; li.style.padding = '12px 15px'; li.style.borderBottom = '1px solid var(--border-color)'; li.style.background = 'var(--card-bg)';
            li.dataset.index = channels.indexOf(ch);
            
            let freqWarning = '';
            const chNameUp = ch.Name.toUpperCase();
            if (frekansData[chNameUp]) {
                let updatedFreq = frekansData[chNameUp];
                if (typeof updatedFreq === 'object') updatedFreq = updatedFreq.freq; // Handle advanced JSON format
                
                if (updatedFreq && parseInt(ch.Freq) !== parseInt(updatedFreq)) {
                    freqWarning = `<div style="font-size:10px; margin-top:4px; padding:2px 6px; background:var(--danger); color:white; border-radius:12px; display:inline-block; font-weight:600; line-height:1.2; opacity:0.9;" title="Doğru Frekans: ${updatedFreq}">⚠️ ${updatedFreq} olmalı</div>`;
                } else if (updatedFreq) {
                    freqWarning = `<div style="font-size:10px; margin-top:4px; padding:2px 6px; background:rgba(34,197,94,0.2); color:#22c55e; border-radius:12px; display:inline-block; font-weight:600; line-height:1.2; border:1px solid rgba(34,197,94,0.3);" title="Frekans Güncel">✅ Güncel</div>`;
                }
            }
            
            // Generate Avatar Logo
            let cleanName = ch.Name.replace(/[^a-zA-Z0-9ğüşıöçĞÜŞİÖÇ]/g, '').trim();
            let letters = cleanName.substring(0, 2).toUpperCase() || 'TV';
            let hash = 0;
            for (let i = 0; i < ch.Name.length; i++) hash = ch.Name.charCodeAt(i) + ((hash << 5) - hash);
            let hue = Math.abs(hash % 360);
            const avatarHtml = `<div class="channel-avatar" style="background: hsl(${hue}, 65%, 45%);" title="${escapeHTML(ch.Name)}">${letters}</div>`;

            // Format Polarization tooltip
            let polLabel = ch.Pol === 'V' ? 'Dikey (V)' : ch.Pol === 'H' ? 'Yatay (H)' : ch.Pol;
            let tooltipText = `Frekans: ${ch.Freq} MHz\nPolarizasyon: ${polLabel}\nSembol Oranı: ${ch.Sym}`;

            li.innerHTML = `
                <div class="col-drag drag-handle" role="button" tabindex="0" aria-label="Taşı" title="Sürükle" style="cursor:grab; color:var(--text-secondary); margin-left:-5px;">
                    <svg class="icon" width="18" height="18"><use href="#icon-grip"/></svg>
                </div>
                <div class="col-check" style="margin-right:10px;">
                    <input type="checkbox" class="row-checkbox" data-idx="${li.dataset.index}">
                </div>
                <div class="col-no" style="font-weight:bold;">${ch.No}</div>
                <div class="col-name" contenteditable="true" spellcheck="false" onblur="updateChannelName(${li.dataset.index}, this.innerText)" title="${escapeHTML(ch.Name)}">${escapeHTML(ch.Name)}</div>
                <div class="col-type">
                    <span style="background:var(--bg-color); padding:2px 6px; border-radius:4px; border:1px solid var(--border-color);">${ch.Type === 'HD' ? 'TV &middot; HD' : (ch.Type === 'SD' ? 'TV' : ch.Type)}</span>
                </div>
                <div class="col-freq" title="${tooltipText}">
                    ${ch.Freq} <span style="font-size:0.7rem; opacity:0.6;">${ch.Pol}/${ch.Sym}</span>
                </div>
                <div class="col-flags">
                    ${ch.Fav1 ? '<span title="Favori" style="color:var(--warning); font-size:14px;">⭐</span>' : ''}
                    ${ch.Encrypted === 'Yes' ? '<span title="Şifreli" style="color:var(--danger); display:flex; align-items:center;"><svg class="icon" width="14" height="14"><use href="#icon-lock"/></svg></span>' : ''}
                    ${ch.Lock === true ? '<span title="Çocuk Kilidi" style="color:var(--danger); display:flex; align-items:center;"><svg class="icon" width="14" height="14"><use href="#icon-lock"/></svg></span>' : ''}
                    ${freqWarning}
                </div>
                <div class="col-action" style="margin-left:auto; display:flex; gap:4px; justify-content:flex-end;">
                    <button class="icon-btn" title="Kilitle/Aç" onclick="toggleFlag(${li.dataset.index}, 'Lock')" style="border:none; background:transparent; color:${ch.Lock ? 'var(--danger)' : 'var(--text-secondary)'}; padding:4px;">
                        <svg class="icon" width="16" height="16"><use href="${ch.Lock ? '#icon-lock' : '#icon-unlock'}"/></svg>
                    </button>
                    <button class="icon-btn info-btn" title="Detaylar" onclick="showChannelInfo(${li.dataset.index})" style="border:none; background:transparent; padding:4px;">
                        <svg class="icon" width="16" height="16"><use href="#icon-info"/></svg>
                    </button>
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

            channelList.appendChild(li);
        });
        
        saveDraftToLocal();
    }

    // Initialize SortableJS
    new Sortable(channelList, {
        handle: '.col-drag', // handle's class
        animation: 150,
        ghostClass: 'sortable-ghost',
        dragClass: 'sortable-drag',
        onEnd: function (evt) {
            if (evt.oldIndex === evt.newIndex) return;
            const item = channels.splice(evt.oldIndex, 1)[0];
            channels.splice(evt.newIndex, 0, item);
            renderChannels(searchInput.value);
            saveDraftToLocal();
        }
    });

    // Custom Toast Notification System
    
    window.deleteChannel = function(index) {
        channels.splice(index, 1);
        renderChannels(searchInput.value);
    }

    window.toggleFlag = function(index, flagName) {
        channels[index][flagName] = !channels[index][flagName];
        renderChannels(searchInput.value);
    }

    window.updateChannelName = function(index, newName) {
        const trimmed = newName.trim();
        if (trimmed && channels[index].Name !== trimmed) {
            channels[index].Name = trimmed;
            // Render is not strictly necessary as DOM is already updated,
            // but doing it ensures consistency.
            renderChannels(searchInput.value);
        } else if (!trimmed) {
            // Restore original name if user empties the text
            renderChannels(searchInput.value);
        }
    }

    searchInput.addEventListener('input', (e) => {
        renderChannels(e.target.value);
    });

    // 1. Magic Wand & Custom Templates
    let TEMPLATES = {};

    // Asenkron olarak harici JSON dosyasından hazır şablonları yükle
    fetch('/static/data/templates.json')
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

    const selectAllCheckbox = document.getElementById('select-all');

    // Builder elements
    const builderModal = document.getElementById('builder-modal');
    const closeBuilderBtn = document.getElementById('close-builder-btn');
    const saveBuilderBtn = document.getElementById('save-builder-btn');
    const builderSourceList = document.getElementById('builder-source-list');
    const builderTargetList = document.getElementById('builder-target-list');
    let builderCart = [];

    // Checkbox state tracking

    function isEnglish() {
        return window.location.pathname.includes('/en') || document.documentElement.lang === 'en';
    }

    function updateSelectedCount() {
        const count = selectedIndices.size;
        const optDel = document.getElementById('opt-del-selected');
        const optLock = document.getElementById('opt-lock-selected');
        const optFav = document.getElementById('opt-fav-selected');
        
        if (optDel) {
            optDel.textContent = isEnglish() ? `🗑️ Delete Selected (${count})` : `🗑️ Seçilileri Sil (${count})`;
            optDel.disabled = count === 0;
        }
        if (optLock) optLock.disabled = count === 0;
        if (optFav) optFav.disabled = count === 0;
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



    saveTemplateBtn.addEventListener('click', () => {
        if (channels.length === 0) {
            toast('Please upload an SCM file first.', 'danger');
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
            li.textContent = `${idx + 1}. ${ch.Name} (${ch.Type})`;
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
            toast('Your cart is empty! Please add channels from left to right.', 'danger');
            return;
        }
        const tName = prompt('Bu mükemmel şablona ne isim vermek istersiniz?');
        if (!tName) return;

        const customList = builderCart.map(c => c.Name);
        localStorage.setItem('scm_custom_' + tName, JSON.stringify(customList));
        builderModal.classList.add('hidden');
        toast('Şablon başarıyla kaydedildi! ✨ Sihirli değnek menüsünden kullanabilirsiniz.', 'success');
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
        toast('Seçilen şablon başarıyla uygulandı! ✨', 'success');
    });

    // --- BULK ACTIONS ---
    const bulkActionsSelect = document.getElementById('bulk-actions-select');
    if (bulkActionsSelect) {
        bulkActionsSelect.addEventListener('change', (e) => {
            const action = e.target.value;
            if (!action) return;
            
            e.target.value = ''; // Reset select
            
            const msgConfirmDeleteSelected = isEnglish() ? `${selectedIndices.size} channels will be deleted. Are you sure?` : `${selectedIndices.size} adet kanal silinecek. Emin misiniz?`;
            const msgConfirmDeleteEncrypted = isEnglish() ? `All encrypted channels will be permanently deleted. Are you sure?` : `Tüm şifreli kanallar kalıcı olarak silinecek. Emin misiniz?`;
            const msgConfirmDeleteRadio = isEnglish() ? `All radio channels will be permanently deleted. Are you sure?` : `Tüm radyo kanalları kalıcı olarak silinecek. Emin misiniz?`;
            const msgDeletedEncrypted = isEnglish() ? ` encrypted channels deleted!` : ` adet şifreli kanal silindi!`;
            const msgDeletedRadio = isEnglish() ? ` radio channels deleted!` : ` adet radyo kanalı silindi!`;
            
            if (action === 'del_selected') {
                if (!confirm(msgConfirmDeleteSelected)) return;
                let indices = Array.from(selectedIndices).sort((a, b) => b - a);
                indices.forEach(idx => {
                    channels.splice(idx, 1);
                });
                selectedIndices.clear();
                selectAllCheckbox.checked = false;
                renderChannels(searchInput.value);
            } else if (action === 'lock_selected') {
                let anyUnlocked = Array.from(selectedIndices).some(idx => !channels[idx].Lock);
                let targetState = anyUnlocked ? true : false;
                selectedIndices.forEach(idx => {
                    channels[idx].Lock = targetState;
                });
                selectedIndices.clear();
                selectAllCheckbox.checked = false;
                renderChannels(searchInput.value);
            } else if (action === 'fav_selected') {
                let anyUnfaved = Array.from(selectedIndices).some(idx => !channels[idx].Fav1);
                let targetState = anyUnfaved ? true : false;
                selectedIndices.forEach(idx => {
                    channels[idx].Fav1 = targetState;
                });
                selectedIndices.clear();
                selectAllCheckbox.checked = false;
                renderChannels(searchInput.value);
            } else if (action === 'del_encrypted') {
                if (!confirm(msgConfirmDeleteEncrypted)) return;
                const initialCount = channels.length;
                channels = channels.filter(c => c.Encrypted === 'No');
                const deleted = initialCount - channels.length;
                renderChannels(searchInput.value);
                alert(`${deleted}${msgDeletedEncrypted}`);
            } else if (action === 'del_radio') {
                if (!confirm(msgConfirmDeleteRadio)) return;
                const initialCount = channels.length;
                channels = channels.filter(c => c.Type !== 'Radio');
                const deleted = initialCount - channels.length;
                renderChannels(searchInput.value);
                alert(`${deleted}${msgDeletedRadio}`);
            }
            updateSelectedCount();
        });
    }

    // --- END NEW FEATURES ---

    saveBtn.addEventListener('click', () => {
        saveBtn.textContent = 'Saving...';
        
        fetch('/build', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ session_id: currentSessionId, channels: channels, filename: currentFileName })
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                window.location.href = data.download_url;
                saveBtn.textContent = 'Save and Download';
                localStorage.removeItem('channel_draft');
            } else {
                toast('Generation error: ' + data.error, 'danger');
                saveBtn.textContent = 'Save and Download';
            }
        })
        .catch(err => {
            console.error(err);
            toast('An error occurred.', 'danger');
            saveBtn.textContent = 'Save and Download';
        });
    });

    // 4. Share Draft (Cross-Device)
    const exportShareBtn = document.getElementById('export-share-btn');
    const importShareBtn = document.getElementById('import-share-btn');

    if (exportShareBtn) {
        exportShareBtn.addEventListener('click', () => {
            exportShareBtn.textContent = '⏳';
            fetch('/api/share', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ draft: channels })
            })
            .then(res => res.json())
            .then(data => {
                exportShareBtn.textContent = '📱 Cihaza Aktar';
                if (data.success) {
                    prompt('Aşağıdaki kodu diğer cihazda "Kod ile İçe Aktar" bölümüne girin. (10 dakika geçerlidir)', data.code);
                } else {
                    toast('Hata: ' + data.error, 'danger');
                }
            }).catch(() => {
                exportShareBtn.textContent = '📱 Cihaza Aktar';
                toast('Bağlantı hatası.', 'danger');
            });
        });
    }

    if (importShareBtn) {
        importShareBtn.addEventListener('click', () => {
            const code = prompt('Diğer ekranda gördüğünüz 6 haneli kodu girin:');
            if (!code) return;
            
            importShareBtn.textContent = '⏳ Yükleniyor...';
            fetch(`/api/share?code=${code}`)
            .then(res => res.json())
            .then(data => {
                importShareBtn.textContent = '📱 Kod ile İçe Aktar';
                if (data.success) {
                    channels = data.draft;
                    dropZone.classList.add('hidden');
                    editorSection.classList.remove('hidden');
                    renderChannels();
                    saveDraftToLocal();
                    toast('Taslak başarıyla aktarıldı! ✨ Kaldığınız yerden devam edebilirsiniz.', 'success');
                } else {
                    toast('Hata: ' + data.error, 'danger');
                }
            }).catch(() => {
                importShareBtn.textContent = '📱 Kod ile İçe Aktar';
                toast('Bağlantı hatası.', 'danger');
            });
        });
    }

    // Modal elements
    const infoModal = document.getElementById('side-panel');
    const closeInfoBtn = document.getElementById('close-side-panel');

    closeInfoBtn.addEventListener('click', () => {
        infoModal.style.display = 'none';
    });

    window.showChannelInfo = function(idx) {
        const ch = channels[idx];
        if (!ch) return;

        // Generate Avatar again
        let cleanName = ch.Name.replace(/[^a-zA-Z0-9ğüşıöçĞÜŞİÖÇ]/g, '').trim();
        let letters = cleanName.substring(0, 2).toUpperCase() || 'TV';
        let hash = 0;
        for (let i = 0; i < ch.Name.length; i++) hash = ch.Name.charCodeAt(i) + ((hash << 5) - hash);
        let hue = Math.abs(hash % 360);

        document.getElementById('info-avatar').innerHTML = `<div class="channel-avatar" style="background: hsl(${hue}, 65%, 45%); width:40px; height:40px; font-size:16px;">${letters}</div>`;
        document.getElementById('info-name').textContent = ch.Name;
        document.getElementById('info-no').textContent = ch.No;
        document.getElementById('info-freq').innerHTML = `<span class="font-monospace">${ch.Freq} MHz</span>`;
        document.getElementById('info-pol').textContent = ch.Pol === 'V' ? 'Dikey (V)' : ch.Pol === 'H' ? 'Yatay (H)' : ch.Pol;
        document.getElementById('info-sym').innerHTML = `<span class="font-monospace">${ch.Sym} ksps</span>`;
        
        let typeHtml = ch.Type === 'HD' ? `<span class="badge" style="background:var(--accent); color:white; padding:4px 8px; border-radius:4px; font-size:12px;">TV HD</span>` : ch.Type;
        document.getElementById('info-type').innerHTML = typeHtml;
        
        document.getElementById('info-enc').innerHTML = ch.Encrypted === 'Yes' ? '<svg class="icon" width="14" height="14"><use href="#icon-lock"/></svg> Evet' : '<svg class="icon" width="14" height="14"><use href="#icon-unlock"/></svg> Hayır';
        
        // Advanced Tech details
        
        let advMod = ch.Type === 'HD' ? 'DVB-S2' : (ch.Type === 'SD' ? 'DVB-S' : '-');
        let advRollOff = '-';
        let advAudioPid = '-';
        
        // Eğer frekansData içinde bu kanal varsa ve gelişmiş nesne yapısındaysa (objeyse) gelişmiş verileri oradan al
        const chNameUp = ch.Name.toUpperCase();
        if (frekansData[chNameUp] && typeof frekansData[chNameUp] === 'object') {
            const extraData = frekansData[chNameUp];
            if (extraData.mod) advMod = extraData.mod;
            if (extraData.rolloff) advRollOff = extraData.rolloff;
            if (extraData.apid) advAudioPid = extraData.apid;
        }

        document.getElementById('info-mod').textContent = advMod;
        document.getElementById('info-rolloff').textContent = advRollOff;
        document.getElementById('info-nid').textContent = ch.ONID !== undefined ? ch.ONID : '-'; // NID is usually same as ONID
        document.getElementById('info-tsid').textContent = ch.TSID !== undefined ? ch.TSID : '-';
        document.getElementById('info-onid').textContent = ch.ONID !== undefined ? ch.ONID : '-';
        document.getElementById('info-sid').textContent = ch.SID !== undefined ? ch.SID : '-';
        document.getElementById('info-vidpid').textContent = ch.VidPID !== undefined ? ch.VidPID : '-';
        document.getElementById('info-audpid').textContent = advAudioPid;
        document.getElementById('info-pcrpid').textContent = ch.PcrPID !== undefined ? ch.PcrPID : '-';

        infoModal.style.display = 'flex';
    };

    // A11y: Esc key to close all modals
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            document.querySelectorAll('.modal').forEach(modal => {
                if (!modal.classList.contains('hidden')) {
                    modal.classList.add('hidden');
                }
            });
            // Also close template builder modal if exists
            if (templateModal && !templateModal.classList.contains('hidden')) {
                templateModal.classList.add('hidden');
            }
        }
    });
    // Keyboard support for moving selected channels (Alt + ArrowUp/ArrowDown)
    document.addEventListener('keydown', (e) => {
        const editorSection = document.getElementById('editor-section');
        if (!editorSection || editorSection.classList.contains('hidden')) return;
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

        if (e.altKey && (e.key === 'ArrowUp' || e.key === 'ArrowDown')) {
            e.preventDefault();
            const selected = document.querySelectorAll('.channel-select:checked');
            if (selected.length === 0) return;
            
            let indices = Array.from(selected).map(cb => parseInt(cb.dataset.index)).sort((a, b) => a - b);
            
            if (e.key === 'ArrowUp') {
                if (indices[0] > 0) {
                    for (let i of indices) {
                        let temp = currentChannels[i-1];
                        currentChannels[i-1] = currentChannels[i];
                        currentChannels[i] = temp;
                    }
                    renderChannels(document.getElementById('search-input').value);
                    indices.forEach(i => {
                        const cb = document.querySelector(`.channel-select[data-index="${i-1}"]`);
                        if (cb) cb.checked = true;
                    });
                }
            } else if (e.key === 'ArrowDown') {
                if (indices[indices.length-1] < currentChannels.length - 1) {
                    for (let i of [...indices].reverse()) {
                        let temp = currentChannels[i+1];
                        currentChannels[i+1] = currentChannels[i];
                        currentChannels[i] = temp;
                    }
                    renderChannels(document.getElementById('search-input').value);
                    indices.forEach(i => {
                        const cb = document.querySelector(`.channel-select[data-index="${i+1}"]`);
                        if (cb) cb.checked = true;
                    });
                }
            }
        }
    });

});
