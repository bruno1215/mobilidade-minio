import { getToken } from './authService'; // Para pegar o token JWT

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api/mobilidade';

const getAuthHeaders = () => {
    const token = getToken();
    return {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
    };
};
export const fetchAnalisePassageirosPorBairro = async () => {
    const response = await fetch(`${API_BASE_URL}/analysis/passengers_by_neighborhood`, {
        method: 'GET',
        headers: getAuthHeaders(),
    });
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.msg || 'Falha ao buscar análise');
    }
    return response.json();
};
// CRUD para Viagens
export const fetchViagens = async (params = {}) => {
    const queryParams = new URLSearchParams(params).toString();
    const response = await fetch(`${API_BASE_URL}/viagens?${queryParams}`, {
        method: 'GET',
        headers: getAuthHeaders(),
    });
    // ... tratamento de erro e retorno
    if (!response.ok) throw new Error('Falha ao buscar viagens');
    return response.json();
};
// Adicionar createViagem, updateViagem, deleteViagem aqui...