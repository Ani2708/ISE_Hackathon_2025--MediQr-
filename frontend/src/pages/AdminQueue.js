import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { api, authHeader } from '../api';


export default function AdminQueue(){
const { dept } = useParams();
const [queue, setQueue] = useState([]);


const token = localStorage.getItem('token');


useEffect(()=>{
let mounted = true;
async function load(){
try{
const r = await api.get(/queue/${dept}/statuslist); // note: backend does not have this endpoint by default; this is a simple placeholder
if(mounted) setQueue(r.data.tokens || []);
}catch(e){
console.error(e);
}
}
load();
const i = setInterval(load, 5000);
return ()=>{ mounted=false; clearInterval(i); }
},[dept]);


async function callNext(){
try{
const r = await api.post(/queue/${dept}/call, {}, authHeader(token));
alert('Called: ' + JSON.stringify(r.data.called));
}catch(e){ console.error(e); alert('Call failed'); }
}


return (
<div className="container">
<h2>Admin Queue — {dept}</h2>
<div className="card">
<button onClick={callNext}>Call Next</button>
<h4>Queue</h4>
<ul>
{queue.length ? queue.map(t => (
<li key={t.tokenNo}>#{t.tokenNo} — {t.patientQr} — {t.status}</li>
)) : <li>No tokens (or backend missing status list endpoint)</li>}
</ul>
</div>
</div>
);
}