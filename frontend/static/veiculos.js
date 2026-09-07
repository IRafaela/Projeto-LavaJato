
        document.addEventListener('DOMContentLoaded', () => {
            carregarVeiculos();
            document.getElementById('form-veiculo').addEventListener('submit', salvarVeiculo);
        });
        function abrirModal() { document.getElementById('modal-veiculo').style.display = 'flex'; }
        function fecharModal() { document.getElementById('modal-veiculo').style.display = 'none'; }

        async function carregarVeiculos() {
            const res = await fetch('/api/v1/veiculos/');
            const veiculos = await res.json();
            const tabela = document.getElementById('tabela-veiculos');
            tabela.innerHTML = '';
            veiculos.forEach(v => {
                tabela.innerHTML += `<tr><td>${v.id}</td><td><span class="car-plate">${v.placa}</span></td><td>${v.modelo}</td><td>${v.marca}</td><td>${v.cor}</td><td>ID: ${v.cliente_id}</td></tr>`;
            });
        }

        async function salvarVeiculo(e) {
            e.preventDefault();
            const payload = {
                placa: document.getElementById('placa').value,
                modelo: document.getElementById('modelo').value,
                marca: document.getElementById('marca').value,
                cor: document.getElementById('cor').value,
                cliente_id: parseInt(document.getElementById('cliente_id').value)
            };
            const res = await fetch('/api/v1/veiculos/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (res.ok) { alert('Veículo salvo!'); fecharModal(); carregarVeiculos(); document.getElementById('form-veiculo').reset(); }
        }
    