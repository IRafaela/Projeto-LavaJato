document.addEventListener('DOMContentLoaded', carregarCaixaHoje);

async function carregarCaixaComFiltro() {
    const dataSelecionada = document.getElementById('dataRelatorio').value;

    const url = dataSelecionada
        ? `/api/v1/caixa/?data=${encodeURIComponent(dataSelecionada)}`
        : '/api/v1/caixa/';

    try {
        const resposta = await fetch(url);
        if (!resposta.ok) {
            throw new Error(`Erro ${resposta.status}`);
        }

        const dados = await resposta.json();
        const transacoes = Array.isArray(dados)
            ? dados
            : dados.transacoes || dados.data || [];

        renderizarTransacoes(transacoes);

    } catch (erro) {
        console.error("Erro ao filtrar o caixa:", erro);
    }
}

async function carregarCaixaHoje() {
    document.getElementById('dataRelatorio').value = '';
    await carregarCaixaComFiltro();
}

function renderizarTransacoes(transacoes) {
    let dinheiro = 0;
    let pix = 0;
    let cartao = 0;
    let saidas = 0;
    const tabela = document.getElementById('tabela-caixa');

    if (tabela) {
        tabela.innerHTML = '';
    }

    transacoes.forEach(transacao => {
        const valor = Number(transacao.valor) || 0;
        const tipo = String(transacao.tipo || '').toLowerCase();
        const forma = normalizarFormaPagamento(transacao.forma_pagamento);

        if (tipo === 'entrada') {
            if (forma === 'dinheiro') dinheiro += valor;
            if (forma === 'pix') pix += valor;
            if (['cartao', 'credito', 'debito'].includes(forma)) {
                cartao += valor;
            }
        }

        if (tipo === 'saida') saidas += valor;

        if (tabela) {
            const linha = document.createElement('tr');
            linha.innerHTML = `
                <td>${transacao.id ?? ''}</td>
                <td>${tipo.toUpperCase()}</td>
                <td>${transacao.descricao || '-'}</td>
                <td>${formatarMoeda(valor)}</td>
                <td>${transacao.forma_pagamento || '-'}</td>
                <td>${transacao.data_hora ? new Date(transacao.data_hora).toLocaleString('pt-BR') : '-'}</td>
            `;
            tabela.appendChild(linha);
        }
    });

    atualizarTexto('total-dinheiro', formatarMoeda(dinheiro));
    atualizarTexto('total-pix', formatarMoeda(pix));
    atualizarTexto('total-cartao', formatarMoeda(cartao));
    atualizarTexto('total-saidas', formatarMoeda(saidas));
    atualizarTexto('saldo-atual', formatarMoeda(dinheiro + pix + cartao - saidas));
}

function normalizarFormaPagamento(forma) {
    return String(forma || '')
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .toLowerCase()
        .trim();
}

function formatarMoeda(valor) {
    return Number(valor).toLocaleString('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    });
}

function atualizarTexto(id, valor) {
    const elemento = document.getElementById(id);

    if (elemento) {
        elemento.textContent = valor;
    }
}