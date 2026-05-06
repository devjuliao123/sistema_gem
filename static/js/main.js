const orgForm = document.getElementById('orgForm');
const orgTableBody = document.getElementById('orgTableBody');
const loadingOverlay = document.getElementById('loadingOverlay');
const deleteModal = new bootstrap.Modal(document.getElementById('deleteModal'));
const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
const toastElement = document.getElementById('liveToast');
const toast = new bootstrap.Toast(toastElement);

let orgToDelete = null;

async function carregarOrganizacoes() {
    showLoading(true);
    try {
        const res = await fetch('/api/organizacoes/');
        const result = await res.json();

        if (result.ok) {
            renderTable(result.data);
        } else {
            showToast('Erro', result.erro, 'danger');
        }
    } catch (error) {
        showToast('Erro', 'Falha ao carregar organizações', 'danger');
    } finally {
        showLoading(false);
    }
}

function renderTable(data) {
    orgTableBody.innerHTML = '';

    if (data.length === 0) {
        orgTableBody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">Nenhuma organização encontrada</td></tr>';
        return;
    }

    data.forEach(org => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${org.numero}</td>
            <td><strong>${org.nome}</strong></td>
            <td><code>${org.schema}</code></td>
            <td>${new Date(org.criado_em).toLocaleString()}</td>
            <td class="text-end">
                <button class="btn btn-sm btn-outline-primary me-1" onclick="acessarOrg('${org.schema}')">
                    <i class="bi bi-box-arrow-in-right"></i> Acessar
                </button>
                <button class="btn btn-sm btn-outline-danger" onclick="confirmarExclusao(${org.numero}, '${org.nome}')">
                    <i class="bi bi-trash"></i>
                </button>
            </td>
        `;
        orgTableBody.appendChild(row);
    });
}

orgForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const nomeInput = document.getElementById('nome');
    const nome = nomeInput.value.trim();

    if (!nome) return;

    showLoading(true);
    try {
        const res = await fetch('/api/organizacoes/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nome })
        });

        const result = await res.json();

        if (result.ok) {
            showToast('Sucesso', `Organização "${nome}" criada com sucesso!`, 'success');
            nomeInput.value = '';
            carregarOrganizacoes();
        } else {
            showToast('Erro', result.erro, 'danger');
        }
    } catch (error) {
        showToast('Erro', 'Falha ao criar organização', 'danger');
    } finally {
        showLoading(false);
    }
});

function confirmarExclusao(numero, nome) {
    orgToDelete = numero;
    document.getElementById('deleteOrgName').innerText = nome;
    deleteModal.show();
}

confirmDeleteBtn.addEventListener('click', async () => {
    if (!orgToDelete) return;

    deleteModal.hide();
    showLoading(true);

    try {
        const res = await fetch(`/api/organizacoes/${orgToDelete}`, {
            method: 'DELETE'
        });

        const result = await res.json();

        if (result.ok) {
            showToast('Sucesso', 'Organização excluída com sucesso', 'success');
            carregarOrganizacoes();
        } else {
            showToast('Erro', result.erro, 'danger');
        }
    } catch (error) {
        showToast('Erro', 'Falha ao excluir organização', 'danger');
    } finally {
        showLoading(false);
        orgToDelete = null;
    }
});

function acessarOrg(schema) {
    alert(`Acessando organização: ${schema} (Placeholder)`);
}

function showLoading(show) {
    loadingOverlay.style.display = show ? 'flex' : 'none';
}

function showToast(title, message, type) {
    document.getElementById('toastTitle').innerText = title;
    document.getElementById('toastBody').innerText = message;

    toastElement.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.show();
}

// Initial load
carregarOrganizacoes();
