// File: static/script.js

// Fungsi efek visual singkat saat form diisi
function highlightForm() {
    const formInputs = document.querySelectorAll('#predictionForm input');
    formInputs.forEach(input => {
        input.style.backgroundColor = '#e0f2fe';
        setTimeout(() => {
            input.style.backgroundColor = '#f8fafc';
        }, 500);
    });
}

function fillHealthySample() {
    document.getElementById('nama_perusahaan').value = 'PT Indofood Makmur Sejahtera Tbk';
    document.getElementById('roa_c').value = 0.5480;
    document.getElementById('net_income_to_assets').value = 0.8390;
    document.getElementById('debt_ratio').value = 0.0820;
    document.getElementById('net_worth_to_assets').value = 0.9180;
    document.getElementById('current_ratio').value = 0.0172;
    document.getElementById('quick_ratio').value = 0.0118;
    document.getElementById('operating_gross_margin').value = 0.6210;
    document.getElementById('cash_flow_to_assets').value = 0.6620;
    
    highlightForm();
}

function fillBankruptSample() {
    document.getElementById('nama_perusahaan').value = 'PT Mitra Properti Pailit Tbk';
    document.getElementById('roa_c').value = 0.3520;
    document.getElementById('net_income_to_assets').value = 0.6750;
    document.getElementById('debt_ratio').value = 0.2450;
    document.getElementById('net_worth_to_assets').value = 0.7550;
    document.getElementById('current_ratio').value = 0.0042;
    document.getElementById('quick_ratio').value = 0.0019;
    document.getElementById('operating_gross_margin').value = 0.5540;
    document.getElementById('cash_flow_to_assets').value = 0.5840;
    
    highlightForm();
}

function confirmDelete(companyName) {
    return confirm(`⚠️ Hapus Data\n\nApakah Anda yakin ingin menghapus data prediksi untuk "${companyName}" dari database? Tindakan ini tidak dapat dibatalkan.`);
}

function filterTable() {
    const input = document.getElementById('searchInput');
    if (!input) return;
    const filter = input.value.toLowerCase();
    const table = document.getElementById('historyTable');
    const tr = table.getElementsByTagName('tr');

    for (let i = 1; i < tr.length; i++) {
        const tdName = tr[i].getElementsByTagName('td')[1];
        if (tdName) {
            const txtValue = tdName.textContent || tdName.innerText;
            if (txtValue.toLowerCase().indexOf(filter) > -1) {
                tr[i].style.display = '';
                tr[i].style.animation = 'fadeIn 0.3s ease-out';
            } else {
                tr[i].style.display = 'none';
            }
        }
    }
}