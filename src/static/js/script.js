document.addEventListener('DOMContentLoaded', function() {
    initSession();
});

let currentClientId; // Variable global para almacenar el clientId actual

function show_addClient() {
    $('#newClientModal').removeClass('hidden');
  };

function close_addClient() {
    $('#newClientModal').addClass('hidden');
  };

function show_deleteClient(id) {
    $('#deleteModal').removeClass('hidden');
    let client_div = document.getElementById(`client-${id}`);
    let client_name = client_div.getAttribute('name');
    currentClientId = id
    $('#deleteClientName').text(client_name);
  };

function close_deleteClient() {
    $('#deleteModal').addClass('hidden');
  };


function show_qrcode(id) {
    $('#qrcodeModal').removeClass('hidden');
    qrcode(id);
  };


function close_qrcode() {
    $('#qrcodeModal').addClass('hidden');
  };

function initSession(){
    fetch('/api/session', {
        method: 'GET'
    })
    .then(response => {
        if (response.ok) {
            console.log("Web works corretly");
            renderClients()
        } 
    })
}

function renderClients() {
    fetch('/api/wireguard/client', {
        method: 'GET', 
        mode: 'cors'
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } 
    })
    .then(clients => {
    let clientHtml = '';
    for (let client of clients) {
      clientHtml += `
        <div class="bg-gray-700 rounded-lg p-4 flex items-center justify-between dark:bg-gray-700" id="client-${client.id}" name="${client.name}">
                    <div class="flex items-center">
                        <div class="bg-gray-600 rounded-full p-2 mr-4 dark:bg-gray-600">
                            <i class="fas fa-user text-white text-2xl"></i>
                        </div>
                        <div>
                            <div class="text-lg font-semibold">${client.name}</div>
                            <div class="text-gray-400 dark:text-gray-400">${client.address}</div>
                        </div>
                    </div>
                    <div class="flex items-center space-x-2">
                        <label class="switch">
                            <input id="check-${client.id}" onclick="enable('${client.id}')" type="checkbox" ${client.enabled ? 'checked' : ''}>
                            <span class="slider round"></span>
                        </label>
                        <button onclick="show_qrcode('${client.id}')"  class="bg-gray-600 p-2 rounded-lg dark:bg-gray-600">
                            <i class="fas fa-qrcode text-white"></i>
                        </button>
                        <button onclick="download('${client.id}')" class="bg-gray-600 p-2 rounded-lg dark:bg-gray-600">
                            <i class="fas fa-download text-white"></i>
                        </button>
                        <button onclick="show_deleteClient('${client.id}')" class="bg-gray-600 p-2 rounded-lg dark:bg-gray-600" >
                            <i class="fas fa-trash text-white"></i>
                        </button>
                    </div>
                </div>
      `;
    }
    $('#clientContainer').html(clientHtml);
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
    });
}


function createClient() {
    let name = $('#clientName').val();
    if (name) {
        fetch(`/api/wireguard/client/${encodeURIComponent(name)}`, {
            method: 'POST',
        })
        .then(response => {
            if (response.ok) {
                renderClients();
            } 
        })
      
      $('#newClientModal').addClass('hidden');
      $('#clientName').val('');
    }
  };

// Añadir event listeners a los botones de trash
function deleteClient() {
    currentClientId 
    $(`#client-${currentClientId}`).remove();

    fetch(`/api/wireguard/client/${encodeURIComponent(currentClientId)}`, {
        method: 'DELETE'
    });
    close_deleteClient();
  };

function enable(id){
    let checkbox = document.getElementById(`check-${id}`);
    let state
    if (checkbox.checked) {
        state = '1'
    } else {
        state = '0'
    }
    fetch(`/api/wireguard/client/${encodeURIComponent(id)}/enable/${encodeURIComponent(state)}`, {
        method: 'POST'
    });
}

function download(id) {
    const a = document.createElement('a');
    a.href = `/api/wireguard/client/${encodeURIComponent(id)}/configuration`;
    a.download = ''; // Deja vacío si el servidor gestiona el nombre del archivo
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

function qrcode(id){
    fetch(`/api/wireguard/client/${encodeURIComponent(id)}/qrcode`)
    .then(response => response.blob())
    .then(blob => {
        const imgURL = URL.createObjectURL(blob);
        document.getElementById('qrcodeImage').src = imgURL;
    })
    .catch(error => console.error('Error al cargar la imagen:', error));
}