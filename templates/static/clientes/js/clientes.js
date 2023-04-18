

function add_carro() {
    // Pega algum elemento da tela baseado no id
    container = document.getElementById('form-carro')
    // Html a que deseja inserir dentro de form-carro
    html = "<br>  <div class='row'> <div class='col-md'> <input type='text' placeholder='carro' class='form-control' name='carro' > </div> <div class='col-md'><input type='text' placeholder='Placa' class='form-control' name='placa' ></div> <div class='col-md'> <input type='number' placeholder='ano' class='form-control' name='ano'> </div> </div>"
    // Insire dentro do html dentro do container
    container.innerHTML += html
}

function exibir_form(tipo) {
    // Captura os containers
    add_cliente = document.getElementById('adicionar-cliente')
    att_cliente = document.getElementById('att_cliente')

    if (tipo == "1") {
        att_cliente.style.display = "none"
        add_cliente.style.display = "block"

    } else if (tipo == "2") {
        add_cliente.style.display = "none";
        att_cliente.style.display = "block"
    }

}


function dados_cliente() {
    // Captura o id do cliente o qual o usuário selecionou
    cliente = document.getElementById('cliente-select')
    // Captura o valor do elemento pelo name
    csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value
    id_cliente = cliente.value
    data = new FormData()
    data.append('id_cliente', id_cliente)

    // Faça uma requisição para a url abaixo (atualiza_cliente) através do método post e com o cabeçalho e dados abaixo
    // Request
    fetch("/clientes/atualiza_cliente/", {
        method: "POST",
        headers: {
            'X-CSRFToken': csrf_token,
        },
        body: data
        // Response
    }).then(function (response) {
        //Promisse
        // Dados retornados do nosso backend
        return response.json()
    })
        .then(function (jsonData) {

            id = document.getElementById('id')
            id.value = jsonData.cliente_id



            // Mostra o form-att-cliente através do display block
            document.getElementById('form-att-cliente').style.display = 'block'
            // captura o elemento nome
            nome = document.getElementById('nome')
            // insere no elemento nome o value recebido do nosso backend em Json.
            nome.value = jsonData.cliente.nome
            sobrenome = document.getElementById('sobrenome')
            sobrenome.value = jsonData.cliente.sobrenome
            email = document.getElementById('email')
            email.value = jsonData.cliente.email
            cpf = document.getElementById('cpf')
            cpf.value = jsonData.cliente.cpf
            // captura do do elemento div id='carros'
            div_carros = document.getElementById('carros')
            // A cada nova resposta, a div id='carros' é limpa e posteriormente preenchida com o o laço for
            div_carros.innerHTML = ''

            // Percorre todos os carros do cliente retornado do backend
            for (i = 0; i < jsonData['carros'].length; i++) {
                // insere um html dentro da div carros
                div_carros.innerHTML += "\<form action='/clientes/update_carro/" + jsonData['carros'][i]['id'] + "' method='POST'>\
                <div class='row'>\
                        <div class='col-md'>\
                            <input class='form-control' name='carro' type='text' value='" + jsonData['carros'][i]['fields']['carro'] + "'>\
                        </div>\
                        <div class='col-md'>\
                            <input class='form-control' name='placa' type='text' value='" + jsonData['carros'][i]['fields']['placa'] + "'>\
                        </div>\
                        <div class='col-md'>\
                            <input class='form-control' type='text' name='ano' value='" + jsonData['carros'][i]['fields']['ano'] + "' >\
                        </div>\
                        <div class='col-md'>\
                            <input class='btn btn-lg btn-success' type='submit'>\
                        </div>\
                    </form>\
                    <div class='col-md'>\
                        <a href='/clientes/excluir_carro/"+ jsonData['carros'][i]['id'] + "' class='btn btn-lg btn-danger'>EXCLUIR</a>\
                    </div>\
                </div><br>"


            }

        })
}



function update_cliente() {

    id = document.getElementById('id').value
    nome = document.getElementById('nome').value
    sobrenome = document.getElementById('sobrenome').value
    cpf = document.getElementById('cpf').value
    email = document.getElementById('email').value

    fetch('/clientes/update_cliente/' + id,
        {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrf_token,
            },
            body: JSON.stringify(
                {
                    nome: nome,
                    sobrenome: sobrenome,
                    cpf: cpf,
                    email: email,
                }
            ),
        }
    ).then(function (response) {
        return response.json()
    }

    ).then(function (jsonData) {

        if (jsonData.status == '200') {

            nome = jsonData.nome
            sobrenome = jsonData.sobrenome
            email = jsonData.email
            cpf = jsonData.cpf
            console.log('Dados alterados com sucesso')

        } else {
            console.log('Ocorreu algum erro')
        }

    })
}