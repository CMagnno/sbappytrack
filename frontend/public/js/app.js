document.getElementById('run').addEventListener('click', async () => {
  const code = document.getElementById('code').value;
  
  try {
    const response = await fetch('http://localhost:8000/api/submit', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ code })
    });
    
    const result = await response.json();
    document.getElementById('output').textContent = result.output || result.error;
  } catch (error) {
    document.getElementById('output').textContent = 'Erro ao conectar com a API';
  }
});