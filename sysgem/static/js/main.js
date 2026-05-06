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
        orgTableBody.innerHTML = '<tr><td colspan="5" class="text-center text-muted p-5 animate__animated animate__fadeIn">Nenhuma organização encontrada na nuvem</td></tr>';
        return;
    }

    data.forEach((org, index) => {
        const row = document.createElement('tr');
        row.className = 'animate__animated animate__fadeInUp';
        row.style.animationDelay = `${index * 0.1}s`;

        row.innerHTML = `
            <td class="align-middle fw-bold text-primary">#${org.numero}</td>
            <td class="align-middle"><span class="h6 mb-0">${org.nome}</span></td>
            <td class="align-middle"><span class="badge-schema"><i class="bi bi-hdd-network me-1"></i>${org.schema}</span></td>
            <td class="align-middle text-muted small"><i class="bi bi-calendar3 me-1"></i>${new Date(org.criado_em).toLocaleString()}</td>
            <td class="text-end align-middle">
                <button class="btn btn-sm btn-primary shadow-sm me-2" onclick="acessarOrg('${org.schema}')">
                    <i class="bi bi-rocket-takeoff me-1"></i> Acessar
                </button>
                <button class="btn btn-sm btn-outline-danger shadow-sm" onclick="confirmarExclusao(${org.numero}, '${org.nome}')">
                    <i class="bi bi-trash3"></i>
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

    if (!nome) {
        nomeInput.classList.add('animate__animated', 'animate__shakeX', 'is-invalid');
        setTimeout(() => nomeInput.classList.remove('animate__animated', 'animate__shakeX'), 500);
        return;
    }

    showLoading(true);
    try {
        const res = await fetch('/api/organizacoes/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nome })
        });

        const result = await res.json();

        if (result.ok) {
            // Success Animation
            const card = nomeInput.closest('.card');
            card.classList.add('animate__animated', 'animate__pulse');
            setTimeout(() => card.classList.remove('animate__animated', 'animate__pulse'), 1000);

            const nomeCriado = result.data.nome;
            showToast('Nuvem Sincronizada', `Organização "${nomeCriado}" implantada com sucesso!`, 'success');
            nomeInput.value = '';
            nomeInput.classList.remove('is-invalid');
            carregarOrganizacoes();
        } else {
            showToast('Falha na Implantação', result.erro, 'danger');
            nomeInput.classList.add('is-invalid');
        }
    } catch (error) {
        showToast('Erro Crítico', 'Falha ao conectar com o serviço de nuvem', 'danger');
    } finally {
        showLoading(false);
    }
});

// Real-time validation
document.getElementById('nome').addEventListener('input', debounce(async (e) => {
    const nome = e.target.value.trim();
    const feedback = document.getElementById('validationFeedback');

    if (nome.length < 3) {
        feedback.innerHTML = '';
        e.target.classList.remove('is-valid', 'is-invalid');
        return;
    }

    try {
        const res = await fetch(`/api/organizacoes/validar-nome?nome=${encodeURIComponent(nome)}`);
        const result = await res.json();

        if (result.ok && result.disponivel) {
            e.target.classList.add('is-valid');
            e.target.classList.remove('is-invalid');
            feedback.innerHTML = '<span class="text-success"><i class="bi bi-check-all"></i> Nome disponível na nuvem</span>';
        } else {
            e.target.classList.add('is-invalid');
            e.target.classList.remove('is-valid');
            feedback.innerHTML = '<span class="text-danger"><i class="bi bi-exclamation-triangle"></i> Nome já utilizado ou inválido</span>';
        }
    } catch (e) {}
}, 500));

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

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
    window.location.href = `/${schema}/inicio`;
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
