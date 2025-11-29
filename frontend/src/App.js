import React from 'react';
import { Link } from 'react-router-dom';


export default function App(){
return (
<div className="container">
<header>
<h1>MediQR</h1>
<p>Smart QR healthcare demo</p>
<nav>
<Link to="/">Home</Link> | <Link to="/login">Doctor/Admin</Link>
</nav>
</header>


<main>
<section className="hero">
<h2>Scan a patient's QR or open profile</h2>
<p>Open a QR link like <code>/patient/&lt;qrId&gt;</code> or use a QR scanner page (not included in this simple demo).</p>
<p>Try the admin queue view at <code>/admin/queue/General</code></p>
</section>
</main>


<footer>
<small>Hackathon demo — MediQR</small>
</footer>
</div>
);
}