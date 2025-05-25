import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Navbar from './components/layout/Navbar';
import PrivateRoute from './components/layout/PrivateRoute';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import AdminPage from './pages/AdminPage';
import AnalisePassageirosPage from './pages/AnalisePassageirosPage';

function AppContent() {
    return (
        <Router>
            <Navbar /> {/* Navbar is now a standalone component */}
            <main> {/* Optional: wrap routes in a main tag for semantics */}
                <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/register" element={<RegisterPage />} />

                    {/* Rotas Protegidas */}
                    <Route element={<PrivateRoute />}>
                        <Route path="/dashboard" element={<DashboardPage />} />
                        <Route path="/analise/passageiros" element={<AnalisePassageirosPage />} />
                    </Route>

                    {/* Rota Protegida para Admin */}
                    <Route element={<PrivateRoute adminOnly={true} />}>
                        <Route path="/admin" element={<AdminPage />} />
                    </Route>

                    <Route path="*" element={<div className="container"><h2>404 - Página Não Encontrada</h2></div>} />
                </Routes>
            </main>
        </Router>
    );
}

function App() {
    return (
        <AuthProvider>
            <AppContent />
        </AuthProvider>
    );
}

export default App;