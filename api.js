async function buscarCEP(cep) {

    const resposta = await fetch(
        `https://viacep.com.br/ws/${cep}/json/`
    );

    return await resposta.json();
}

module.exports = buscarCEP;