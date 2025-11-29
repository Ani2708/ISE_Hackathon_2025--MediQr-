import React from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import App from './App';
import PatientPage from './pages/PatientPage';
import Login from './pages/Login';
import AdminQueue from './pages/AdminQueue';
import './styles.css';


createRoot(document.getElementById('root')).render(
<BrowserRouter>
<Routes>
<Route path="/" element={<App/>} />
<Route path="/login" element={<Login/>} />
<Route path="/patient/:qrId" element={<PatientPage/>} />
<Route path="/admin/queue/:dept" element={<AdminQueue/>} />
</Routes>
</BrowserRouter>
);