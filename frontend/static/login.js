document.addEventListener("DOMContentLoaded", () => {
   
    
    const loginForm = document.getElementById("loginForm");
    const linkEsqueciSenha = document.getElementById("linkEsqueciSenha");

    // 1. Lógica do formulário de login
    if (loginForm) {
        loginForm.addEventListener("submit", async (event) => {
            event.preventDefault();

            const usuario = document.getElementById("usuario").value;
            const senha = document.getElementById("senha").value;

            // O OAuth2PasswordRequestForm do FastAPI espera os dados como URL-encoded
            const formData = new URLSearchParams();
            formData.append("username", usuario);
            formData.append("password", senha);

            try {
                const response = await fetch('/api/v1/auth/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    body: formData
                });

                const resultado = await response.json();

                if (response.ok) {
                    alert("Login realizado com sucesso!");
                    localStorage.setItem("token", resultado.access_token);
                    window.location.href = "/dashboard"; 
                } else {
                    alert("Erro no login: " + (resultado.detail || "Verifique suas credenciais."));
                }
            } catch (error) {
                console.error("Erro na requisição:", error);
                alert("Erro de conexão com o servidor.");
            }
        });
    }

    
    if (linkEsqueciSenha) {
        linkEsqueciSenha.addEventListener("click", async (event) => {
            event.preventDefault(); // Evita que a página recarregue pelo link '#'

            const email = prompt("Digite o seu e-mail cadastrado:");
            if (!email) return;

            const nova_senha = prompt("Digite a sua nova senha:");
            if (!nova_senha) return;

            try {
                const response = await fetch('/api/v1/auth/recuperar-senha', {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        email: email,
                        nova_senha: nova_senha
                    })
                });

                const resultado = await response.json();

                if (response.ok) {
                    alert("Senha alterada com sucesso! Faça login com a nova senha.");
                } else {
                    alert("Erro: " + (resultado.detail || "Não foi possível alterar a senha."));
                }
            } catch (error) {
                console.error("Erro na requisição:", error);
                alert("Erro de conexão com o servidor.");
            }
        });
    }
});