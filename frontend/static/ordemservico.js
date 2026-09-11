let ordemSelecionada = null;
let enviandoOrdem = false;

document.addEventListener('DOMContentLoaded', async () => {
    await excluirOrdensEntreguesHoje();
    await listarOrdens();

    const formulario = document.getElementById('form-ordem');

    if (formulario) {
        formulario.addEventListener('submit', criarOrdem);
    }
});

async function excluirOrdensEntreguesHoje() {
    try {
        const resposta = await fetch(
            '/api/v1/ordens-servico/limpar-entregues-hoje',
            {
                method: 'DELETE',
                headers: {
                    'Accept': 'application/json'
                }
            }
        );

        const texto = await resposta.text();
        const resultado = texto ? JSON.parse(texto) : {};

        if (!resposta.ok) {
            throw new Error(
                resultado.detail || `Erro HTTP ${resposta.status}`
            );
        }

        console.log(
            `Ordens antigas removidas: ${resultado.quantidade ?? 0}`
        );
    } catch (erro) {
        console.error('Erro ao limpar ordens entregues:', erro);
    }
}


function abrirModal() {
    document.getElementById('modal-ordem').style.display = 'flex';
}

function fecharModal() {
    document.getElementById('modal-ordem').style.display = 'none';
}

function abrirModalEntrega(id) {
    ordemSelecionada = id;
    document.getElementById('forma_pagamento').value = '';
    document.getElementById('modal-entrega').style.display = 'flex';
}

function fecharModalEntrega() {
    document.getElementById('modal-entrega').style.display = 'none';
    ordemSelecionada = null;
}

async function listarOrdens() {
    try {
        const resposta = await fetch('/api/v1/ordens-servico');

        if (!resposta.ok) {
            throw new Error(await resposta.text());
        }

        const ordens = await resposta.json();
        const tabela = document.getElementById('tabela-ordens');

        if (!tabela) {
            return;
        }

        tabela.innerHTML = '';

        ordens.forEach(ordem => {
            const linha = document.createElement('tr');

            linha.innerHTML = `
                <td>${ordem.id}</td>
                <td>${ordem.tipo_lavagem}</td>
                <td>R$ ${Number(ordem.valor).toFixed(2)}</td>
                <td>${ordem.veiculo_id}</td>
                <td>${ordem.funcionario_id}</td>
                <td>
                    <button
                        type="button"
                        class="btn btn-salvar"
                        onclick="abrirModalEntrega(${ordem.id})">
                        Entregar
                    </button>
                </td>
            `;

            tabela.appendChild(linha);
        });
    } catch (erro) {
        console.error('Erro ao carregar ordens:', erro);
        alert('Não foi possível carregar as ordens.');
    }
}

async function criarOrdem(evento) {
    evento.preventDefault();

    if (enviandoOrdem) {
        return;
    }

    enviandoOrdem = true;
    const botaoEnviar = evento.submitter;

    if (botaoEnviar) {
        botaoEnviar.disabled = true;
    }

    const dados = {
        tipo_lavagem: document.getElementById('tipo_lavagem').value,
        valor: Number(document.getElementById('valor').value),
        veiculo_id: Number(document.getElementById('veiculo_id').value),
        funcionario_id: document.getElementById('funcionario_id').value ? Number(document.getElementById('funcionario_id').value) : null
    
    };

    try {
        const resposta = await fetch('/api/v1/ordens-servico', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dados)
        });

        if (!resposta.ok) {
            const erro = await resposta.json().catch(() => ({}));
            throw new Error(erro.detail || `Erro HTTP ${resposta.status}`);
        }

        document.getElementById('form-ordem').reset();
        fecharModal();
        await listarOrdens();

        alert('Ordem criada com sucesso!');
    } catch (erro) {
        console.error('Erro ao criar ordem:', erro);
        alert(erro.message || 'Não foi possível criar a ordem.');
    } finally {
        enviandoOrdem = false;

        if (botaoEnviar) {
            botaoEnviar.disabled = false;
        }
    }
}

async function confirmarEntrega() {
    const formaPagamento = document.getElementById(
        'forma_pagamento'
    ).value;

    if (!formaPagamento) {
        alert('Selecione a forma de pagamento.');
        return;
    }

    try {
        const resposta = await fetch(
            `/api/v1/ordens-servico/${ordemSelecionada}/entrega`,
            {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    forma_pagamento: formaPagamento
                })
            }
        );

        if (!resposta.ok) {
            throw new Error(await resposta.text());
        }

        fecharModalEntrega();
        await listarOrdens();

        alert('Ordem entregue e lançada no caixa!');
    } catch (erro) {
        console.error('Erro ao entregar ordem:', erro);
        alert('Não foi possível entregar a ordem.');
    }
}

window.addEventListener('click', evento => {
    if (evento.target === document.getElementById('modal-ordem')) {
        fecharModal();
    }

    if (evento.target === document.getElementById('modal-entrega')) {
        fecharModalEntrega();
    }
});