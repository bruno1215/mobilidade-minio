import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const HomePage = () => {
    const { isAuthenticated } = useAuth();
    return (
        <div className="container">
            <h1>Bem-vindo ao Sistema de Análise de Mobilidade Urbana! 🚦🚌</h1>
            <p>Este sistema permite analisar dados de mobilidade, visualizar informações e gerenciar dados de viagens.</p>
            {isAuthenticated ? (
                <div>
                    <p>Você está logado. Explore o <Link to="/dashboard">Dashboard</Link> ou a <Link to="/analise/passageiros">Análise de Passageiros</Link>.</p>
                </div>
            ) : (
                <div>
                    <p>Faça <Link to="/login">login</Link> para acessar todas as funcionalidades ou <Link to="/register">registre-se</Link> se você não tem uma conta.</p>
                </div>
            )}
             <p>Desenvolvido como um projeto full-stack integrando React, Flask, PostgreSQL, MinIO e Docker.</p>
        </div>
    );
};

export default HomePage;
