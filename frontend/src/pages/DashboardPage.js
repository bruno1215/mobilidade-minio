import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Link } from 'react-router-dom';

const DashboardPage = () => {
    const { currentUser, isAdmin } = useAuth();

    return (
        <div className="container">
            <h1>Dashboard 📊</h1>
            {currentUser && (
                <p>Bem-vindo de volta, <strong>{currentUser.username}</strong>!</p>
            )}
            <p>A partir daqui você pode navegar para as principais funcionalidades do sistema.</p>
            <ul>
                <li><Link to="/analise/passageiros">Ver Análise de Passageiros por Bairro</Link></li>
                {/* Adicionar links para outras seções, como CRUD de viagens */}
                {isAdmin && (
                    <li><Link to="/admin">Acessar Painel Administrativo</Link></li>
                )}
            </ul>
        </div>
    );
};

export default DashboardPage;
