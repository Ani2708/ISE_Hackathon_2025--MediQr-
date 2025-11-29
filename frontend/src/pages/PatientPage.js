import React, { useEffect, useState } from 'react';
}
load();
},[qrId]);


if(!patient) return <div className="container"><p>Loading...</p></div>;


return (
<div className="container">
<h2>Patient Profile {publicView ? '(Emergency view)' : ''}</h2>
<div className="card">
<p><strong>Name:</strong> {patient.name}</p>
{patient.dob && <p><strong>DOB:</strong> {new Date(patient.dob).toLocaleDateString()}</p>}
<p><strong>Blood Group:</strong> {patient.bloodGroup}</p>
<p><strong>Allergies:</strong> {patient.allergies?.join(', ')}</p>
<p><strong>Chronic:</strong> {patient.chronicConditions?.join(', ')}</p>
<p><strong>Emergency Contact:</strong> {patient.contacts?.emergency}</p>
</div>


<section>
<h3>Actions</h3>
<button onClick={async ()=>{
// enqueue at General
try{
const r = await api.post('/queue/General/enqueue', { qrId });
alert(Token ${r.data.tokenNo} — est wait ${r.data.estWait} min);
}catch(e){ console.error(e); alert('Failed to enqueue'); }
}}>Enter Hospital (Generate Token)</button>


<label style={{ display: 'block', marginTop: 12 }}>
Upload prescription image:
<input type="file" id="presFile" />
</label>
<button style={{ marginTop: 8 }} onClick={async ()=>{
const f = document.getElementById('presFile').files[0];
if(!f) return alert('Choose file');
const form = new FormData(); form.append('image', f);
try{
const r = await api.post(/prescriptions/${qrId}/upload, form, { headers: { 'Content-Type': 'multipart/form-data' } });
alert('Uploaded. Parsed items: ' + JSON.stringify(r.data.prescription.items));
}catch(e){ console.error(e); alert('Upload failed') }
}}>Upload Prescription</button>


<button style={{ marginLeft: 12 }} onClick={async ()=>{
try{
const r = await api.post(/prescriptions/${qrId}/predict/diabetes, { features: { age: 45, bmi: 27, sugar: 140, bp: 120 } });
alert('Diabetes score: ' + JSON.stringify(r.data.score || r.data));
}catch(e){ console.error(e); alert('Prediction error'); }
}}>Get Diabetes Risk</button>


<div style={{ marginTop: 16 }}>
<h4>Prescriptions</h4>
{patient.prescriptions?.length ? (
<ul>
{patient.prescriptions.map(p => (
<li key={p.id}>{new Date(p.date).toLocaleString()} — {p.items?.map(i=>i.name).join(', ')}</li>
))}
</ul>
) : <p>No prescriptions</p>}
</div>


</section>


</div>
);
}