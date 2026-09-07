const API_USUARIOS = '/api/v1/usuarios';

function $(id) {
    return document.getElementById(id);
}

function abrirModal() {
    const modal = $('modal-usuario');

    if (modal) {
        modal.style.display = 'flex';
    }
}

function fecharModal() {
    const modal = $('modal-usuario');

    if (modal) {
        modal.style.display = 'none';
    }
}

async function carregarUsuarios() {
    try {
        const resposta = await fetch(`${API_USUARIOS}/`, {
            credentials: 'include'
        });

        if (!resposta.ok) {
            throw new Error(`Erro ${resposta.status}`);
        }

        const usuarios = await resposta.json();
        const tabela = $('tabela-usuarios');

        if (!tabela) {
            return;
        }

        tabela.innerHTML = '';

        usuarios.forEach(usuario => {
            const linha = document.createElement('tr');

            linha.innerHTML = `
                <td>${usuario.id ?? ''}</td>
                <td>${usuario.nome ?? ''}</td>
                <td>${usuario.sobrenome ?? ''}</td>
                <td>${usuario.email ?? ''}</td>
                <td>${usuario.eh_admin ? 'Sim' : 'Não'}</td>
            `;

            tabela.appendChild(linha);
        });
    } catch (erro) {
        console.error('Erro ao carregar usuários:', erro);
        alert('Não foi possível carregar os usuários.');
    }
}

async function criarUsuario(evento) {
    evento.preventDefault();

    const usuario = {
        nome: $('nome').value,
        sobrenome: $('sobrenome').value,
        email: $('email').value,
        senha: $('senha').value,
        eh_admin: $('eh_admin').checked
    };

    try {
        const resposta = await fetch(`${API_USUARIOS}/criar_usuario`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify(usuario)
        });

        if (!resposta.ok) {
            throw new Error(await resposta.text());
        }

        $('form-usuario').reset();
        fecharModal();
        await carregarUsuarios();

        alert('Usuário cadastrado com sucesso!');
    } catch (erro) {
        console.error('Erro ao cadastrar usuário:', erro);
        alert('Não foi possível cadastrar o usuário.');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    carregarUsuarios();

    const formulario = $('form-usuario');

    if (formulario) {
        formulario.addEventListener('submit', criarUsuario);
    }
});

window.addEventListener('click', evento => {
    const modal = $('modal-usuario');

    if (evento.target === modal) {
        fecharModal();
    }
});