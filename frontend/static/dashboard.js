async function carregarDashboard() {
    try {
        const response = await fetch('/api/v1/dashboard/');

        if (!response.ok) {
            throw new Error('Erro ao buscar dados do Dashboard');
        }

        const dados = await response.json();

        // 1. Atualiza os contadores gerais na tela
        document.getElementById('total-clientes').innerText = dados.clientes;
        document.getElementById('total-veiculos').innerText = dados.veiculos;
        document.getElementById('total-funcionarios').innerText = dados.funcionarios;
        document.getElementById('total-ordens').innerText = dados.ordensServico;

        // 2. Preenche a tabela de Ordens de Serviço Pendentes
        const tbody = document.getElementById('tabela-dashboard-pendentes');
        if (tbody && dados.ordensPendentes) {
            tbody.innerHTML = ''; // Limpa a tabela antes de inserir

            dados.ordensPendentes.forEach(ordem => {
                const linha = document.createElement('tr');
                linha.innerHTML = `
                    <td>${ordem.id}</td>
                    <td>${ordem.tipo_lavagem}</td>
                    <td>R$ ${ordem.valor}</td>
                    <td>${ordem.status}</td>
                `;
                tbody.appendChild(linha);
            });
        }

    } catch (erro) {
        console.error('Erro ao carregar Dashboard:', erro);
    }
}

document.addEventListener('DOMContentLoaded', carregarDashboard);

