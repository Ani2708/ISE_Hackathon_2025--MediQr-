import React, { useEffect } from 'react';
import { Html5Qrcode } from 'html5-qrcode';


export default function QRScanner({ onScan }){
useEffect(()=>{
const scanner = new Html5Qrcode('qr-reader');
scanner.start({ facingMode: 'environment' }, { fps: 10, qrbox: 250 }, (decoded)=>{
onScan(decoded);
scanner.stop().catch(()=>{});
}, (err)=>{})
.catch(err => console.error(err));
return ()=>{ scanner.stop().catch(()=>{}); }
}, [onScan]);


return (
<div id="qr-reader" style={{ width: '320px', height: '320px' }}></div>
);
}