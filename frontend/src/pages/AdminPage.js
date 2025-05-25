import React, { useState } from 'react';
import { getToken } from '../services/authService'; // Assumindo que getToken está em authService
const AdminPage = () => {
    const [file, setFile] = useState(null);
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');
    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };
    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!file) {
            setError('Por favor, selecione um arquivo CSV.');
            return;
        }
        const formData = new FormData();
        formData.append('file', file);
        setMessage('');
        setError('');
        try {
            const token = getToken();
            const response = await fetch('http://localhost:5000/api/admin/load_csv_data', { // Ajuste a URL conforme necessário
                method: 'POST',
                headers: {
                    ...(token && { 'Authorization': `Bearer ${token}` }),
                    // 'Content-Type': 'multipart/form-data' // O browser define automaticamente com FormData
                },
                body: formData,
            });
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.msg || data.error || 'Erro ao carregar CSV.');
            }
            setMessage(data.msg);
            setFile(null); // Limpar o input
            event.target.reset(); // Resetar o formulário
        } catch (err) {
            setError(err.message);
            console.error("Erro no upload:", err);
        }
    };
    return (
        <div>
            <h1>Painel Administrativo</h1>
            <h2>Carregar Dados de Mobilidade (CSV)</h2>
            <form onSubmit={handleSubmit}>
                <input type="file" accept=".csv" onChange={handleFileChange} required />
                <button type="submit">Carregar CSV</button>
            </form>
            {message && <p style={{ color: 'green' }}>{message}</p>}
            {error && <p style={{ color: 'red' }}>{error}</p>}
            {/* Outras funcionalidades de admin aqui */}
        </div>
    );
};
export default AdminPage;