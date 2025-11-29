import React, { useState } from 'react';
import { api } from '../api';
import { useNavigate } from 'react-router-dom';


export default function Login(){
const [email, setEmail] = useState('');
const [password, setPassword] = useState('');
const nav = useNavigate();


async function submit(e){
e.preventDefault();
try{
const r = await api.post('/auth/login', { email, password });
localStorage.setItem('token', r.data.token);
nav('/admin/queue/General');
}catch(err){
alert('Login failed');
}
}


return (
<div className="container">
<h2>Login (Doctor/Admin)</h2>
<form onSubmit={submit} className="card">
<label>Email<input value={email} onChange={e=>setEmail(e.target.value)} /></label>
<label>Password<input type="password" value={password} onChange={e=>setPassword(e.target.value)} /></label>
<button type="submit">Login</button>
</form>
</div>
);
}