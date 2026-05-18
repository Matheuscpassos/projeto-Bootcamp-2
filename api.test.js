const buscarCEP = require('./api');

global.fetch = jest.fn(() =>
    Promise.resolve({
        json: () =>
            Promise.resolve({
                localidade: 'São Paulo',
                uf: 'SP'
            })
    })
);

test('deve retornar cidade e estado do CEP', async () => {

    const dados = await buscarCEP('01001000');

    expect(dados.localidade).toBe('São Paulo');

    expect(dados.uf).toBe('SP');
});