import React, { createContext, useState, useEffect, useContext } from 'react';
import * as authService from '../services/authService';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [currentUser, setCurrentUser] = useState(authService.getCurrentUser());
    const [loading, setLoading] = useState(true); // Para verificar token na inicialização

    useEffect(() => {
        const verifyToken = async () => {
            const token = authService.getToken();
            if (token) {
                try {
                    // Tenta buscar os detalhes do usuário para validar o token
                    const userDetails = await authService.fetchCurrentUserDetails();
                    setCurrentUser(userDetails); // Atualiza com dados frescos do backend
                } catch (error) {
                    console.error("Erro ao verificar token:", error);
                    authService.logout(); // Token inválido ou expirado
                    setCurrentUser(null);
                }
            }
            setLoading(false);
        };
        verifyToken();
    }, []);

    const login = async (username_or_email, password) => {
        const data = await authService.login(username_or_email, password);
        setCurrentUser(data.user);
        return data;
    };

    const register = async (username, email, password) => {
        return authService.register(username, email, password);
    };

    const logout = () => {
        authService.logout();
        setCurrentUser(null);
    };

    const value = {
        currentUser,
        isAuthenticated: !!currentUser,
        isAdmin: currentUser?.is_admin || false,
        login,
        register,
        logout,
        loading // Para saber se a verificação inicial do token terminou
    };

    return <AuthContext.Provider value={value}>{!loading && children}</AuthContext.Provider>;
};

export const useAuth = () => useContext(AuthContext);
