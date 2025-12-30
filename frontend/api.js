// ============================================
// API Service Layer
// ============================================

const API_BASE_URL = 'http://localhost:8000';

class APIService {
    constructor(baseURL = API_BASE_URL) {
        this.baseURL = baseURL;
        this.token = localStorage.getItem('authToken');
    }

    // Helper method for making requests
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }

        const config = {
            ...options,
            headers
        };

        try {
            const response = await fetch(url, config);

            if (response.status === 204) {
                return null;
            }

            if (!response.ok) {
                const error = await response.json().catch(() => ({ message: 'Request failed' }));
                throw new Error(error.message || `HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API Request Error:', error);
            throw error;
        }
    }

    // User endpoints
    async getUsers() {
        return this.request('/UserApp/users/');
    }

    async searchUsers(query) {
        return this.request(`/UserApp/users/?search=${encodeURIComponent(query)}`);
    }

    async getUser(id) {
        return this.request(`/UserApp/users/${id}`);
    }

    async updateUser(id, userData) {
        return this.request(`/UserApp/users/${id}`, {
            method: 'PUT',
            body: JSON.stringify(userData)
        });
    }

    async createUser(userData) {
        return this.request('/UserApp/users/', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    }

    async updateUserRole(id, newRole, adminEmail) {
        return this.request(`/UserApp/users/${id}`, {
            method: 'PUT',
            body: JSON.stringify({
                role: newRole,
                requesting_user_email: adminEmail
            })
        });
    }

    async deleteUser(id) {
        return this.request(`/UserApp/users/${id}`, {
            method: 'DELETE'
        });
    }

    // Idea endpoints
    async getIdeas() {
        return this.request('/IdeaApp/ideas/');
    }

    async getIdea(id) {
        return this.request(`/IdeaApp/ideas/${id}`);
    }

    async createIdea(ideaData) {
        return this.request('/IdeaApp/ideas/', {
            method: 'POST',
            body: JSON.stringify(ideaData)
        });
    }

    async updateIdea(id, ideaData) {
        return this.request(`/IdeaApp/ideas/${id}`, {
            method: 'PUT',
            body: JSON.stringify(ideaData)
        });
    }

    async deleteIdea(id) {
        return this.request(`/IdeaApp/ideas/${id}`, {
            method: 'DELETE'
        });
    }

    // Category endpoints
    async getCategories() {
        return this.request('/IdeaApp/categories/');
    }

    async createCategory(categoryData) {
        return this.request('/IdeaApp/categories/', {
            method: 'POST',
            body: JSON.stringify(categoryData)
        });
    }

    async deleteCategory(id) {
        return this.request(`/IdeaApp/categories/${id}`, {
            method: 'DELETE'
        });
    }

    // Tag endpoints
    async getTags() {
        return this.request('/IdeaApp/tags/');
    }

    // Status endpoints
    async getStatuses() {
        return this.request('/IdeaApp/status/');
    }

    async createStatus(statusData) {
        return this.request('/IdeaApp/status/', {
            method: 'POST',
            body: JSON.stringify(statusData)
        });
    }

    async deleteStatus(id) {
        return this.request(`/IdeaApp/status/${id}`, {
            method: 'DELETE'
        });
    }

    // Team endpoints
    async getTeams(userId = null) {
        const url = userId ? `/TeamApp/teams/?user_id=${userId}` : '/TeamApp/teams/';
        return this.request(url);
    }

    async getTeam(id) {
        return this.request(`/TeamApp/team/${id}`);
    }

    async createTeam(teamData) {
        return this.request('/TeamApp/teams/', {
            method: 'POST',
            body: JSON.stringify(teamData)
        });
    }

    async addTeamMember(teamId, userId) {
        return this.request('/TeamApp/teamMembers/', {
            method: 'POST',
            body: JSON.stringify({
                team: teamId,
                user: userId
            })
        });
    }

    async getTeamMember(id) {
        return this.request(`/TeamApp/teamMember/${id}`);
    }

    async updateTeam(id, teamData) {
        return this.request(`/TeamApp/team/${id}`, {
            method: 'PUT',
            body: JSON.stringify(teamData)
        });
    }

    async deleteTeam(id) {
        return this.request(`/TeamApp/team/${id}`, {
            method: 'DELETE'
        });
    }

    // Team Member endpoints
    async getTeamMembers() {
        return this.request('/TeamApp/teamMembers/');
    }

    async createTeamMember(memberData) {
        return this.request('/TeamApp/teamMembers/', {
            method: 'POST',
            body: JSON.stringify(memberData)
        });
    }

    async deleteTeamMember(id) {
        return this.request(`/TeamApp/teamMember/${id}`, {
            method: 'DELETE'
        });
    }

    // Comment endpoints
    async getComments(ideaId) {
        return this.request(`/InteractionApp/ideas/${ideaId}/comments/`);
    }

    async createComment(ideaId, commentData) {
        return this.request(`/InteractionApp/ideas/${ideaId}/comments/`, {
            method: 'POST',
            body: JSON.stringify(commentData)
        });
    }

    // Vote endpoints
    async voteIdea(ideaId, voteData) {
        return this.request(`/InteractionApp/ideas/${ideaId}/vote/`, {
            method: 'POST',
            body: JSON.stringify(voteData)
        });
    }

    // Update endpoints
    async getUpdates(ideaId) {
        return this.request(`/IdeaApp/ideas/${ideaId}/updates/`);
    }

    async createUpdate(ideaId, updateData) {
        return this.request(`/IdeaApp/ideas/${ideaId}/updates/`, {
            method: 'POST',
            body: JSON.stringify(updateData)
        });
    }

    // Media upload
    async uploadMedia(formData) {
        const url = `${this.baseURL}/IdeaApp/media/`;
        const headers = {};

        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers,
                body: formData // Don't set Content-Type for FormData
            });

            if (!response.ok) {
                throw new Error(`Upload failed! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Media Upload Error:', error);
            throw error;
        }
    }
}

// Create a global instance
const api = new APIService();
