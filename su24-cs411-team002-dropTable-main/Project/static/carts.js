const budgetInput = document.getElementById('budgetInput');
const budgetIndicator = document.getElementById('budgetIndicator');
const rows = document.querySelectorAll('#cartTableBody tr');

function updatePermissions() {
  const budget = parseFloat(budgetInput.value) || 0;

  rows.forEach(row => {
    const costElem = row.querySelector('.cart-cost span');
    const cost = parseFloat(costElem.textContent) || 0;

    if (cost > budget) {
      costElem.classList.remove('under-budget-cost');
      costElem.classList.add('over-budget-cost');
    } else {
      costElem.classList.remove('over-budget-cost');
      costElem.classList.add('under-budget-cost');
    }
  });

  if (Array.from(rows).some(row => parseFloat(row.querySelector('.cart-cost span').textContent) > budget)) {
    budgetIndicator.classList.remove('under-budget');
    budgetIndicator.classList.add('over-budget');
  } else {
    budgetIndicator.classList.remove('over-budget');
    budgetIndicator.classList.add('under-budget');
  }
}

budgetInput.addEventListener('input', updatePermissions);

// Initial update
updatePermissions();
