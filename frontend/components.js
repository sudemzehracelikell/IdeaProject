// ============================================
// Reusable UI Components
// ============================================

// Toast Notification System
class ToastManager {
    constructor() {
        this.container = document.getElementById('toastContainer');
        if (!this.container) {
            this.container = document.createElement('div');
            this.container.id = 'toastContainer';
            this.container.className = 'toast-container';
            document.body.appendChild(this.container);
        }
    }

    show(message, type = 'info', duration = 3000) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;

        const icon = this.getIcon(type);
        toast.innerHTML = `
            <div class="flex gap-md items-center">
                <span style="font-size: 1.5rem;">${icon}</span>
                <div>
                    <strong>${this.getTitle(type)}</strong>
                    <p style="margin: 0; color: var(--color-text-secondary);">${message}</p>
                </div>
            </div>
        `;

        this.container.appendChild(toast);

        setTimeout(() => {
            toast.style.animation = 'toastSlideIn var(--transition-base) reverse';
            setTimeout(() => toast.remove(), 250);
        }, duration);
    }

    getIcon(type) {
        const icons = {
            success: '✓',
            error: '✕',
            warning: '⚠',
            info: 'ℹ'
        };
        return icons[type] || icons.info;
    }

    getTitle(type) {
        const titles = {
            success: 'Başarılı',
            error: 'Hata',
            warning: 'Uyarı',
            info: 'Bilgi'
        };
        return titles[type] || titles.info;
    }
}

const toastManager = new ToastManager();

// Global toast function
function showToast(message, type = 'info', duration = 3000) {
    toastManager.show(message, type, duration);
}

// ============================================
// Modal Component
// ============================================

class Modal {
    constructor(id, title, content) {
        this.id = id;
        this.title = title;
        this.content = content;
        this.element = null;
        this.create();
    }

    create() {
        this.element = document.createElement('div');
        this.element.id = this.id;
        this.element.className = 'modal';
        this.element.innerHTML = `
            <div class="modal-backdrop" onclick="closeModal('${this.id}')"></div>
            <div class="modal-content">
                <div class="modal-header">
                    <h3>${this.title}</h3>
                    <button class="modal-close" onclick="closeModal('${this.id}')">&times;</button>
                </div>
                <div class="modal-body">
                    ${this.content}
                </div>
            </div>
        `;
        document.body.appendChild(this.element);
    }

    show() {
        this.element.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    hide() {
        this.element.classList.remove('active');
        document.body.style.overflow = '';
    }
}

// Global modal functions
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }
}

// ============================================
// Idea Card Component
// ============================================

function createIdeaCard(idea) {
    const card = document.createElement('div');
    card.className = 'glass-card idea-card';
    card.onclick = () => window.location.href = `idea-detail.html?id=${idea.IdeaID}`;

    const statusClass = getStatusBadgeClass(idea.StatusID?.name || 'Draft');

    card.innerHTML = `
        <div class="card-header">
            <div class="flex justify-between items-center">
                <span class="badge ${statusClass}">${idea.StatusID?.name || 'Draft'}</span>
                <span class="badge badge-primary">${idea.CategoryID?.name || 'Genel'}</span>
            </div>
        </div>
        <div class="card-body">
            <h3 class="card-title">${idea.Title}</h3>
            <p>${truncateText(idea.ShortDescription || idea.Description, 150)}</p>
            ${idea.Tags && idea.Tags.length > 0 ? `
                <div class="flex gap-sm" style="flex-wrap: wrap; margin-top: var(--space-md);">
                    ${idea.Tags.map(tag => `<span class="badge">#${tag.TagName}</span>`).join('')}
                </div>
            ` : ''}
        </div>
        <div class="card-footer">
            <div class="flex items-center gap-md">
                <span class="flex items-center gap-sm">
                    <span style="font-size: 1.2rem;">⭐</span>
                    <span>${idea.VotesCount || 0}</span>
                </span>
                <span class="flex items-center gap-sm">
                    <span style="font-size: 1.2rem;">💬</span>
                    <span>${idea.CommentsCount || 0}</span>
                </span>
            </div>
            <span class="text-muted" style="font-size: var(--font-size-sm);">
                ${formatDate(idea.CreateDate)}
            </span>
        </div>
    `;

    return card;
}

// ============================================
// Comment Component
// ============================================

function createCommentElement(comment) {
    const commentEl = document.createElement('div');
    commentEl.className = 'comment glass-card';
    commentEl.style.marginBottom = 'var(--space-md)';

    commentEl.innerHTML = `
        <div class="flex gap-md">
            <div class="comment-avatar" style="
                width: 40px;
                height: 40px;
                border-radius: 50%;
                background: var(--gradient-primary);
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: 700;
                flex-shrink: 0;
            ">
                ${comment.user?.userName ? comment.user.userName.charAt(0).toUpperCase() : 'U'}
            </div>
            <div style="flex: 1;">
                <div class="flex justify-between items-center" style="margin-bottom: var(--space-sm);">
                    <strong>${comment.user?.userName || 'Anonim'}</strong>
                    <span class="text-muted" style="font-size: var(--font-size-sm);">
                        ${formatDate(comment.comment_date)}
                    </span>
                </div>
                <p style="margin: 0; color: var(--color-text-secondary);">${comment.text}</p>
            </div>
        </div>
    `;

    return commentEl;
}

// ============================================
// Update Timeline Component
// ============================================

function createUpdateElement(update) {
    const updateEl = document.createElement('div');
    updateEl.className = 'update-item glass-card';
    updateEl.style.marginBottom = 'var(--space-md)';
    updateEl.style.borderLeft = '4px solid var(--color-primary)';

    const stateClass = getUpdateStateBadgeClass(update.state);
    const stateText = getUpdateStateText(update.state);

    updateEl.innerHTML = `
        <div class="flex justify-between items-start" style="margin-bottom: var(--space-sm);">
            <span class="badge ${stateClass}">${stateText}</span>
            <span class="text-muted" style="font-size: var(--font-size-sm);">
                ${formatDate(update.created_at)}
            </span>
        </div>
        <p style="margin: 0; color: var(--color-text-secondary);">${update.description}</p>
        <div style="margin-top: var(--space-sm);">
            <span class="text-muted" style="font-size: var(--font-size-sm);">
                ${update.user?.userName || 'Bilinmeyen Kullanıcı'}
            </span>
        </div>
    `;

    return updateEl;
}

// ============================================
// Team Card Component
// ============================================

function createTeamCard(team) {
    const card = document.createElement('div');
    card.className = 'glass-card team-card';
    card.onclick = () => window.location.href = `team-detail.html?id=${team.id}`;

    const memberCount = team.teamMember?.length || 0;

    card.innerHTML = `
        <div class="card-body">
            <div style="
                width: 60px;
                height: 60px;
                border-radius: var(--radius-xl);
                background: var(--gradient-accent);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 2rem;
                margin-bottom: var(--space-lg);
            ">
                👥
            </div>
            <h3 class="card-title">${team.teamName}</h3>
            <p class="text-muted">${memberCount} üye</p>
        </div>
        <div class="card-footer">
            <button class="btn btn-outline btn-sm" onclick="event.stopPropagation(); viewTeam(${team.id})">
                Detayları Gör
            </button>
        </div>
    `;

    return card;
}

// ============================================
// User Card Component
// ============================================

function createUserCard(user) {
    const card = document.createElement('div');
    card.className = 'glass-card user-card';

    const roleName = getRoleName(user.role);
    const roleClass = user.role === 1 ? 'badge-error' :
        user.role === 3 ? 'badge-primary' :
            user.role === 4 ? 'badge-warning' : 'badge';

    card.innerHTML = `
        <div class="flex items-center gap-md">
            <div style="
                width: 50px;
                height: 50px;
                border-radius: 50%;
                background: var(--gradient-primary);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.5rem;
                font-weight: 700;
            ">
                ${user.userName.charAt(0).toUpperCase()}
            </div>
            <div style="flex: 1;">
                <h4 style="margin-bottom: var(--space-xs);">${user.userName}</h4>
                <p class="text-muted" style="margin: 0; font-size: var(--font-size-sm);">${user.email}</p>
            </div>
            <span class="badge ${roleClass}">${roleName}</span>
        </div>
    `;

    return card;
}

// ============================================
// Empty State Component
// ============================================

function createEmptyState(message, icon = '📭') {
    const emptyState = document.createElement('div');
    emptyState.className = 'empty-state';
    emptyState.style.cssText = `
        text-align: center;
        padding: var(--space-3xl);
        color: var(--color-text-muted);
    `;

    emptyState.innerHTML = `
        <div style="font-size: 4rem; margin-bottom: var(--space-lg);">${icon}</div>
        <p style="font-size: var(--font-size-lg);">${message}</p>
    `;

    return emptyState;
}

// ============================================
// Pagination Component
// ============================================

function createPagination(currentPage, totalPages, onPageChange) {
    const pagination = document.createElement('div');
    pagination.className = 'pagination';
    pagination.style.cssText = `
        display: flex;
        justify-content: center;
        gap: var(--space-sm);
        margin-top: var(--space-2xl);
    `;

    // Previous button
    const prevBtn = document.createElement('button');
    prevBtn.className = 'btn btn-ghost btn-sm';
    prevBtn.textContent = '← Önceki';
    prevBtn.disabled = currentPage === 1;
    prevBtn.onclick = () => onPageChange(currentPage - 1);
    pagination.appendChild(prevBtn);

    // Page numbers
    for (let i = 1; i <= totalPages; i++) {
        if (i === 1 || i === totalPages || (i >= currentPage - 1 && i <= currentPage + 1)) {
            const pageBtn = document.createElement('button');
            pageBtn.className = i === currentPage ? 'btn btn-primary btn-sm' : 'btn btn-ghost btn-sm';
            pageBtn.textContent = i;
            pageBtn.onclick = () => onPageChange(i);
            pagination.appendChild(pageBtn);
        } else if (i === currentPage - 2 || i === currentPage + 2) {
            const dots = document.createElement('span');
            dots.textContent = '...';
            dots.style.padding = 'var(--space-sm)';
            pagination.appendChild(dots);
        }
    }

    // Next button
    const nextBtn = document.createElement('button');
    nextBtn.className = 'btn btn-ghost btn-sm';
    nextBtn.textContent = 'Sonraki →';
    nextBtn.disabled = currentPage === totalPages;
    nextBtn.onclick = () => onPageChange(currentPage + 1);
    pagination.appendChild(nextBtn);

    return pagination;
}

// ============================================
// Search Bar Component
// ============================================

function createSearchBar(placeholder, onSearch) {
    const searchBar = document.createElement('div');
    searchBar.className = 'search-bar';
    searchBar.style.cssText = `
        position: relative;
        max-width: 500px;
        margin-bottom: var(--space-xl);
    `;

    searchBar.innerHTML = `
        <input 
            type="text" 
            class="form-input" 
            placeholder="${placeholder}"
            style="padding-left: var(--space-3xl);"
        >
        <span style="
            position: absolute;
            left: var(--space-md);
            top: 50%;
            transform: translateY(-50%);
            font-size: 1.2rem;
        ">🔍</span>
    `;

    const input = searchBar.querySelector('input');
    input.addEventListener('input', debounce((e) => onSearch(e.target.value), 300));

    return searchBar;
}
