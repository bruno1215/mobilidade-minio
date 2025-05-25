import React from 'react';
import LoginForm from '../components/auth/LoginForm';
import { Link } from 'react-router-dom';

const LoginPage = () => {
    return (
        <div className="container">
            <LoginForm />
            <p style={{ textAlign: 'center', marginTop: '20px' }}>
                Não tem uma conta? <Link to="/register">Registre-se aqui</Link>
            </p>
        </div>
    );
};

export default LoginPage;
