
        document.addEventListener('DOMContentLoaded', () => {
            carregarClientes();
            document.getElementById('form-cliente').addEventListener('submit', salvarCliente);
        });
        function abrirModal() { document.getElementById('modal-cliente').style.display = 'flex'; }
        function fecharModal() { document.getElementById('modal-cliente').style.display = 'none'; }

        async function carregarClientes() {
            try {
                const res = await fetch('/api/v1/clientes/');
                const clientes = await res.json();
                const tabela = document.getElementById('tabela-clientes');
                tabela.innerHTML = '';
                clientes.forEach(c => {
                    tabela.innerHTML += `<tr><td>${c.id}</td><td><strong>${c.nome}</strong></td><td>${c.email}</td><td>${c.telefone}</td></tr>`;
                });
            } catch (erro) { console.error('Erro ao carregar clientes:', erro); }
        }

        async function salvarCliente(e) {
            e.preventDefault();
            const payload = {
                nome: document.getElementById('nome').value,
                telefone: document.getElementById('telefone').value,
                endereco: document.getElementById('endereco').value || null,
                cpf: document.getElementById('cpf').value || null
            };
            try {
                const res = await fetch('/api/v1/clientes/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                if (res.ok) { alert('Cliente cadastrado!'); fecharModal(); carregarClientes(); document.getElementById('form-cliente').reset(); }
                else { alert('Erro ao cadastrar cliente.'); }
            } catch (erro) { console.error('Erro na requisição:', erro); }
        }
    