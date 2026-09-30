# app.py - Sistema de Gestión Documental - Admin Pro
# Ejecutar con: python app.py

import http.server
import socketserver
import webbrowser
from pathlib import Path

html_code = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Gestión Documental | Admin Pro</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
  *{margin:0;padding:0;box-sizing:border-box;font-family:'Poppins',sans-serif}
  body{background:#fdf2f8;min-height:100vh}
 .header{background:linear-gradient(135deg,#7c3aed 0%,#a855f7 50%,#ec4899 100%);color:white;padding:30px;border-radius:0 0 30px 30px;box-shadow:0 10px 30px rgba(124,58,237,.3)}
 .header h1{font-size:28px}.header p{opacity:.9;margin-top:5px}
 .container{max-width:1100px;margin:-20px auto 40px;padding:20px}
 .stats{display:grid;grid-template-columns:repeat(4,1fr);gap:15px;margin-bottom:25px}
 .stat{background:white;padding:20px;border-radius:20px;box-shadow:0 4px 15px rgba(0,0,0,.05);border-left:5px solid #a855f7}
 .stat b{font-size:24px;color:#7c3aed}
 .card{background:white;border-radius:20px;padding:25px;box-shadow:0 8px 25px rgba(124,58,237,.12)}
 .card-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px}
 .btn{background:linear-gradient(135deg,#7c3aed,#ec4899);color:white;border:none;padding:10px 20px;border-radius:12px;cursor:pointer;font-weight:600}
 .btn:hover{opacity:.9;transform:scale(1.02)}
  table{width:100%;border-collapse:collapse}
  th{background:#f5f3ff;color:#6d28d9;text-align:left;padding:12px 15px;font-size:13px;text-transform:uppercase;letter-spacing:.5px}
  td{padding:14px 15px;border-bottom:1px solid #f3e8ff;font-size:14px}
  tr:hover{background:#fdf4ff}
 .rol{padding:5px 12px;border-radius:20px;font-size:12px;font-weight:600;display:inline-block}
 .rol-admin{background:#ede9fe;color:#6d28d9}.rol-archivista{background:#fce7f3;color:#be185d}
 .rol-creador{background:#f3e8ff;color:#7e22ce}.rol-aprobador{background:#ddd6fe;color:#4c1d95}
 .rol-consultor{background:#ffe4e6;color:#9f1239}
 .avatar{width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,#a855f7,#ec4899);color:white;display:inline-flex;align-items:center;justify-content:center;font-weight:700;margin-right:8px;font-size:13px}
  input{padding:8px 12px;border:2px solid #e9d5ff;border-radius:10px;outline:none;width:100%}
  input:focus{border-color:#a855f7}
 .form-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:15px}
</style>
</head>
<body>
<div class="header">
  <h1>✨ Panel Admin - Gestión Documental</h1>
  <p>Control total de roles, usuarios y permisos | Corporación CIB</p>
</div>
<div class="container">
  <div class="stats">
    <div class="stat"><small>Total Usuarios</small><br><b>5</b></div>
    <div class="stat"><small>Documentos</small><br><b>1,248</b></div>
    <div class="stat"><small>Pendientes</small><br><b>23</b></div>
    <div class="stat"><small>Archivados</small><br><b>892</b></div>
  </div>

  <div class="card">
    <div class="card-head">
      <h3 style="color:#6d28d9">👥 Gestión de Roles</h3>
      <button class="btn" onclick="addUser()">+ Nuevo Usuario</button>
    </div>

    <div class="form-grid" id="formArea" style="display:none">
      <input id="nombre" placeholder="Nombre">
      <input id="apellido" placeholder="Apellido">
      <input id="email" placeholder="Email">
    </div>

    <table>
      <thead>
        <tr><th>Usuario</th><th>Nombre y Apellido</th><th>Rol Sistema</th><th>Área</th><th>Permisos</th></tr>
      </thead>
      <tbody id="tbody">
        <tr><td><span class="avatar">AG</span>ana.garcia</td><td>Ana García</td><td><span class="rol rol-admin">Administrador</span></td><td>TI / Sistemas</td><td>Todo</td></tr>
        <tr><td><span class="avatar">CP</span>carlos.perez</td><td>Carlos Pérez</td><td><span class="rol rol-archivista">Archivista</span></td><td>Archivo Central</td><td>Crear, Archivar, Eliminar</td></tr>
        <tr><td><span class="avatar">LM</span>luisa.mendez</td><td>Luisa Méndez</td><td><span class="rol rol-creador">Creador</span></td><td>Contabilidad</td><td>Crear, Subir, Ver</td></tr>
        <tr><td><span class="avatar">JR</span>jorge.rua</td><td>Jorge Rúa</td><td><span class="rol rol-aprobador">Aprobador</span></td><td>Gerencia</td><td>Aprobar, Rechazar, Comentar</td></tr>
        <tr><td><span class="avatar">MT</span>maria.torres</td><td>María Torres</td><td><span class="rol rol-consultor">Consultor</span></td><td>Ventas</td><td>Solo lectura</td></tr>
      </tbody>
    </table>
  </div>
</div>
<script>
function addUser(){
  let n=document.getElementById('nombre').value;
  let a=document.getElementById('apellido').value;
  let e=document.getElementById('email').value;
  if(!n){document.getElementById('formArea').style.display='grid';return;}
  let tbody=document.getElementById('tbody');
  let ini=(n[0]+(a[0]||'')).toUpperCase();
  tbody.innerHTML+=`<tr><td><span class="avatar">${ini}</span>${n.toLowerCase()}.${a.toLowerCase()}</td><td>${n} ${a}</td><td><span class="rol rol-creador">Creador</span></td><td>General</td><td>Crear, Ver</td></tr>`;
  document.getElementById('nombre').value='';document.getElementById('apellido').value='';document.getElementById('email').value='';
}
</script>
</body>
</html>
"""

Path("gestion_documental.html").write_text(html_code, encoding="utf-8")

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler
print(f"✅ Sistema creado: gestion_documental.html")
print(f"🌐 Abriendo en http://localhost:{PORT}/gestion_documental.html")

webbrowser.open(f"http://localhost:{PORT}/gestion_documental.html")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()