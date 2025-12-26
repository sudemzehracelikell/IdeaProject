// ============================================
// Core Application Logic
// ============================================

// Authentication Manager
class AuthManager {
    constructor() {
        this.currentUser = this.loadUser();
    }

    loadUser() {
        const userStr = localStorage.getItem('currentUser');
        return userStr ? JSON.parse(userStr) : null;
    }

    saveUser(user) {
        this.currentUser = user;
        localStorage.setItem('currentUser', JSON.stringify(user));
    }

    logout() {
        this.currentUser = null;
        localStorage.removeItem('currentUser');
        localStorage.removeItem('authToken');
        window.location.href = 'index.html';
    }

    isAuthenticated() {
        return this.currentUser !== null;
    }

    hasRole(role) {
        if (!this.currentUser) return false;
        return this.currentUser.role === role;
    }

    isAdmin() {
        return this.hasRole(1); // Admin role
    }

    isTeamLeader() {
        return this.hasRole(3); // Team Leader role
    }

    isJudge() {
        return this.hasRole(4); // Judge role
    }

    isParticipant() {
        return this.hasRole(2); // Participant role
    }

    requireAuth() {
        if (!this.isAuthenticated()) {
            window.location.href = 'auth.html';
            return false;
        }
        return true;
    }
}

// Global auth instance
const auth = new AuthManager();

// ============================================
// Utility Functions
// ============================================

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 0) {
        return 'Bugün';
    } else if (diffDays === 1) {
        return 'Dün';
    } else if (diffDays < 7) {
        return `${diffDays} gün önce`;
    } else {
        return date.toLocaleDateString('tr-TR');
    }
}

// Truncate text
function truncateText(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

// Get role name
function getRoleName(roleId) {
    const roles = {
        1: 'Admin',
        2: 'Katılımcı',
        3: 'Takım Lideri',
        4: 'Hakem'
    };
    return roles[roleId] || 'Bilinmeyen';
}

// Get status badge class
function getStatusBadgeClass(status) {
    const statusMap = {
        'Draft': 'badge-warning',
        'Public': 'badge-success',
        'Closed': 'badge-error'
    };
    return statusMap[status] || 'badge';
}

// Get update state badge class
function getUpdateStateBadgeClass(state) {
    const stateMap = {
        'IN_PROGRESS': 'badge-primary',
        'COMPLETED': 'badge-success',
        'WAITING': 'badge-warning',
        'CANCELLED': 'badge-error'
    };
    return stateMap[state] || 'badge';
}

// Get update state text
function getUpdateStateText(state) {
    const stateMap = {
        'IN_PROGRESS': 'Devam Ediyor',
        'COMPLETED': 'Tamamlandı',
        'WAITING': 'Beklemede',
        'CANCELLED': 'İptal Edildi'
    };
    return stateMap[state] || state;
}

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Show loading overlay
function showLoading() {
    const overlay = document.createElement('div');
    overlay.className = 'loading-overlay';
    overlay.id = 'loadingOverlay';
    overlay.innerHTML = '<div class="spinner"></div>';
    document.body.appendChild(overlay);
}

// Hide loading overlay
function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.remove();
    }
}

// ============================================
// Navigation Updates
// ============================================

function updateNavigation() {
    const navbarMenu = document.getElementById('navbarMenu');
    if (!navbarMenu) return;

    if (auth.isAuthenticated()) {
        navbarMenu.innerHTML = `
            <li><a href="index.html" class="navbar-link">Ana Sayfa</a></li>
            <li><a href="dashboard.html" class="navbar-link">Dashboard</a></li>
            <li><a href="ideas.html" class="navbar-link">Fikirler</a></li>
            <li><a href="teams.html" class="navbar-link">Takımlar</a></li>
            <li><a href="profile.html" class="navbar-link">Profil</a></li>
            <li><button onclick="auth.logout()" class="btn btn-ghost btn-sm">Çıkış Yap</button></li>
        `;
    } else {
        navbarMenu.innerHTML = `
            <li><a href="index.html" class="navbar-link">Ana Sayfa</a></li>
            <li><a href="ideas.html" class="navbar-link">Fikirler</a></li>
            <li><a href="teams.html" class="navbar-link">Takımlar</a></li>
            <li><a href="auth.html" class="btn btn-primary btn-sm">Giriş Yap</a></li>
        `;
    }

    // Set active link
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const links = navbarMenu.querySelectorAll('.navbar-link');
    links.forEach(link => {
        if (link.getAttribute('href') === currentPage) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

// ============================================
// Form Validation
// ============================================

function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validateForm(formElement) {
    const inputs = formElement.querySelectorAll('[required]');
    let isValid = true;

    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add('error');
        } else {
            input.classList.remove('error');
        }

        if (input.type === 'email' && input.value && !validateEmail(input.value)) {
            isValid = false;
            input.classList.add('error');
        }
    });

    return isValid;
}

// ============================================
// Initialize on page load
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    updateNavigation();
});

// ============================================
// Error Handler
// ============================================

window.addEventListener('unhandledrejection', event => {
    console.error('Unhandled promise rejection:', event.reason);
    showToast('Bir hata oluştu. Lütfen tekrar deneyin.', 'error');
    hideLoading();
});
