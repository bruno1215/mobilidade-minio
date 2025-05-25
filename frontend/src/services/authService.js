const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/auth'; // Configure no .env do React
export const login = async (username_or_email, password) => {
    const response = await fetch(`${API_URL}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username_or_email, password }),
    });
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.msg || 'Falha no login');
    }
    const data = await response.json();
    if (data.access_token) {
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('user', JSON.stringify(data.user)); // Armazena dados do usuário
    }
    return data;
};
export const register = async (username, email, password) => {
    const response = await fetch(`${API_URL}/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password }),
    });
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.msg || 'Falha no registro');
    }
    return response.json();
};
export const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
};
export const getCurrentUser = () => {
    const token = localStorage.getItem('token');
    const user = localStorage.getItem('user');
    return token ? JSON.parse(user) : null;
};
export const getToken = () => {
    return localStorage.getItem('token');
};
// Para buscar dados do usuário logado (ex: /auth/me)
export const fetchCurrentUserDetails = async () => {
    const token = getToken();
    if (!token) return null;

    const response = await fetch(`${API_URL}/me`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    if (!response.ok) {
        // Token pode ter expirado, fazer logout
        if (response.status === 401 || response.status === 422) { // 422 Unprocessable Entity se o token for inválido
            logout();
        }
        throw new Error('Falha ao buscar dados do usuário');
    }
    return response.json();
};