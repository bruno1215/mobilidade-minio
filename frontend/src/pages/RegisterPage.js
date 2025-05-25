import React from 'react';
import RegisterForm from '../components/auth/RegisterForm';
import { Link } from 'react-router-dom';

const RegisterPage = () => {
    return (
        <div className="container">
            <RegisterForm />
            <p style={{ textAlign: 'center', marginTop: '20px' }}>
                Já tem uma conta? <Link to="/login">Faça login aqui</Link>
            </p>
        </div>
    );
};

export default RegisterPage;
