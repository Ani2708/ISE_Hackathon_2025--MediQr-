import axios from 'axios';


const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:4000/api';


export const api = axios.create({ baseURL: API_BASE, timeout: 15000 });


export function authHeader(token){
return { headers: { Authorization: Bearer ${token} } };
}