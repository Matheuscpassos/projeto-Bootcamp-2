async function buscarCEP() {

    const cep = document.getElementById("cep").value;

    const resposta = await fetch(
        `https://viacep.com.br/ws/${cep}/json/`
    );

    const dados = await resposta.json();

    document.getElementById("resultado").innerHTML = `
        <p><strong>Rua:</strong> ${dados.logradouro}</p>
        <p><strong>Bairro:</strong> ${dados.bairro}</p>
        <p><strong>Cidade:</strong> ${dados.localidade}</p>
        <p><strong>Estado:</strong> ${dados.uf}</p>
    `;
}