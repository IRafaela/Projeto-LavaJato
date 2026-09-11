document.addEventListener('DOMContentLoaded', () => {
    carregarFuncionarios();

    // 2. Evento para o formulário (quando clica em "Salvar")
    const form = document.getElementById('form-funcionario');
    if (form) {
        form.addEventListener('submit', salvarFuncionario);
    }
});

// 3. Função para salvar o funcionário
async function salvarFuncionario(e) {
    e.preventDefault(); // Impede o reload da página

    const payload = {
        nome: document.getElementById('nome').value,
        endereco: document.getElementById('endereco').value,
        telefone: document.getElementById('telefone').value,
        salario: parseFloat(document.getElementById('salario').value),
        email: document.getElementById('email').value,
        senha: document.getElementById('senha').value
    };

    try {
        // Altere a URL para o que estiver no seu Swagger (/docs)
        const res = await fetch(`/api/v1/funcionarios/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (res.ok) {
            alert('Funcionário cadastrado!');
            document.getElementById('modal-funcionario').style.display = 'none';
            document.getElementById('form-funcionario').reset();
            carregarFuncionarios(); // Atualiza a tabela
        } else {
            const erro = await res.json();
            alert('Erro: ' + JSON.stringify(erro));
        }
    } catch (error) {
        console.error('Erro:', error);
    }
}

// 4. Função para carregar a lista (exemplo básico)
async function carregarFuncionarios() {
    try {
        const res = await fetch(`/api/v1/funcionarios/`);
        if (res.ok) {
            const dados = await res.json();
            
            const tabela = document.getElementById('tabela-funcionarios');
            if (tabela) {
                tabela.innerHTML = ''; // Limpa a tabela antes de preencher
                
                dados.forEach(func => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td>${func.id}</td>
                        <td>${func.nome}</td>
                        <td>${func.endereco}</td>
                        <td>${func.telefone}</td>
                        <td>R$ ${func.salario}</td>
                        <td>${func.email}</td>
                        <td>***</td>
                    `;
                    tabela.appendChild(tr);
                });
            }
        } else {
            console.error('Erro ao buscar funcionários. Status:', res.status);
        }
    } catch (error) {
        console.error('Erro de conexão ao carregar funcionários:', error);
    }
}
    
  
// 5. Funções de modal (que você já deve ter no código)
function abrirModal() { document.getElementById('modal-funcionario').style.display = 'flex'; }
function fecharModal() { document.getElementById('modal-funcionario').style.display = 'none'; }