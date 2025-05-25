import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const Navbar = () => {
    const { isAuthenticated, currentUser, logout, isAdmin } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login'); // Redirect to login after logout
    };

    return (
        <nav>
            <Link to="/">App Mobilidade</Link>
            {isAuthenticated ? (
                <>
                    <Link to="/dashboard">Dashboard</Link>
                    <Link to="/analise/passageiros">Análise de Passageiros</Link>
                    {isAdmin && <Link to="/admin">Painel Admin</Link>}
                    <span>Olá, {currentUser?.username}!</span>
                    <button onClick={handleLogout}>Sair</button>
                </>
            ) : (
                <>
                    <Link to="/login">Login</Link>
                    <Link to="/register">Registrar</Link>
                </>
            )}
        </nav>
    );
};

export default Navbar;
