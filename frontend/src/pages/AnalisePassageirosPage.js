import React, { useState, useEffect } from 'react';
import { fetchAnalisePassageirosPorBairro } from '../services/mobilidadeService';

const AnalisePassageirosPage = () => {
    const [analiseData, setAnaliseData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const carregarAnalise = async () => {
            setLoading(true);
            setError('');
            try {
                const data = await fetchAnalisePassageirosPorBairro();
                setAnaliseData(data);
            } catch (err) {
                setError(err.message || 'Falha ao carregar dados da análise.');
                console.error("Analysis fetch error:", err);
            }
            setLoading(false);
        };

        carregarAnalise();
    }, []);

    if (loading) {
        return <div className="loading-message container">Carregando análise... ⏳</div>;
    }

    if (error) {
        return <div className="error-message container">Erro: {error} 😔</div>;
    }

    if (!analiseData) {
        return <div className="container">Nenhum dado de análise disponível.</div>;
    }

    return (
        <div className="container analise-container">
            <h1>Análise de Passageiros por Bairro 📈</h1>
            <p>{analiseData.message}</p>

            {analiseData.plot_url && (
                <div>
                    <h3>Gráfico Gerado:</h3>
                    <img src={analiseData.plot_url} alt="Gráfico de Passageiros por Bairro" />
                    <p>
                        <a href={analiseData.plot_url} target="_blank" rel="noopener noreferrer">
                            Abrir gráfico em nova aba
                        </a>
                    </p>
                </div>
            )}

            {analiseData.data && analiseData.data.length > 0 && (
                <div>
                    <h3>Dados Tabulados:</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Bairro</th>
                                <th>Total de Passageiros</th>
                            </tr>
                        </thead>
                        <tbody>
                            {analiseData.data.map((item, index) => (
                                <tr key={index}>
                                    <td>{item.bairro}</td>
                                    <td>{item.passageiros}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
};

export default AnalisePassageirosPage;
