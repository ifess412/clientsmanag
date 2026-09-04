document.addEventListener('DOMContentLoaded', function() {
    const numInput = document.getElementById('id_num');

    // Перевіряємо, чи є поле на сторінці, чи воно порожнє і чи має атрибут data-model
    if (numInput && !numInput.value && numInput.dataset.model) {
        const modelName = numInput.dataset.model; // Отримуємо значення з data-model

        // Передаємо назву моделі як GET-параметр (?model=...)
        fetch(`/finances/ajax/get-next-doc-number/?model=${modelName}`)
            .then(response => {
                if (!response.ok) throw new Error('Мережева помилка');
                return response.json();
            })
            .then(data => {
                if (data.next_number) {
                    numInput.value = data.next_number;
                }
            })
            .catch(error => console.error('Помилка отримання номера документа:', error));
    }
});


const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))


// Додаємо автоматичний перарахунок значень полів для форми додавання ліцензії
// Отримуємо ПОСИЛАННЯ НА DOM-ЕЛЕМЕНТИ (всегда ищем как элементы)
const nomenclatureSelect = document.getElementById('id_nomenclature');
const priceInput = document.getElementById('id_price');
const devSelect = document.getElementById('id_developer');
const devdiscountInput = document.getElementById('id_devdiscount');
const devpriceInput = document.getElementById('id_devprice');
const agdiscountInput = document.getElementById('id_agdiscount');
const agpriceInput = document.getElementById('id_agprice');
const taxSelect = document.getElementById('id_taxes');
const taxdiscountInput = document.getElementById('id_taxdiscount');
const taxpriceInput = document.getElementById('id_taxprice');

// Функция безопасного получения числового значения из любого инпута
function getInputValue(element) {
    if (!devSelect) return 0; // ГЛАВНОЕ УСЛОВИЕ: если devSelect нет, принудительно возвращаем 0 для скидок разработчика
    return element ? (Number(element.value) || 0) : 0;
}

// Определение функции
function calculateprice(a, b) {
    let price = a;
    let discount = b/100;
    let total = (price * discount).toFixed(2); // "54.95" (рядок)
    let totalNum = +total; // Перетворення назад у число -> 54.95
    return totalNum; // Возвращает произведение двух переменных
}

// Определение функции
function setvalues(p, dd, ad, td) {
    let price = p;
    let devdiscount = dd;
    let taxdiscount = td;
    let agdiscount = 100 - taxdiscount - devdiscount;
    let devprice = calculateprice(price, devdiscount);
    let taxprice = calculateprice(price, taxdiscount);
    let agprice = price - taxprice - devprice;

    // Записываем значения в инпуты только если эти инпуты физически существуют на странице
    if (devdiscountInput) devdiscountInput.value = devdiscount;
    if (devpriceInput) devpriceInput.value = devprice;
    if (agdiscountInput) agdiscountInput.value = agdiscount;
    if (agpriceInput) agpriceInput.value = agprice;
    if (taxdiscountInput) taxdiscountInput.value = taxdiscount;
    if (taxpriceInput) taxpriceInput.value = taxprice;
}

if (nomenclatureSelect) {
    nomenclatureSelect.addEventListener('change', function() {
      let productId = this.value;
      if (productId) {
                  fetch(`/finances/ajax/get-price/?id=${productId}`)
                      .then(response => response.json())
                      .then(data => {
                          let price = data.price;
                          let devdiscount = getInputValue(devdiscountInput);
                          let taxdiscount = getInputValue(taxdiscountInput);
                          let agdiscount = 100 - taxdiscount - devdiscount;
                          setvalues(price, devdiscount, agdiscount, taxdiscount);
                          if (priceInput) priceInput.value = price;
                      })
                      .catch(error => console.error('Помилка:', error));
              }
    });
}

if (devSelect) {
  devSelect.addEventListener('change', function() {
    let partnetId = this.value;
    if (partnetId) {
                fetch(`/finances/ajax/get-discount/?id=${partnetId}`)
                    .then(response => response.json())
                    .then(data => {
                        let price = priceInput ? priceInput.value : 0;
                        let devdiscount = data.price;
                        let taxdiscount = getInputValue(taxdiscountInput);
                        let agdiscount = 100 - taxdiscount - devdiscount;
                        setvalues(price, devdiscount, agdiscount, taxdiscount)
                    })
                    .catch(error => console.error('Помилка:', error));
            }
  });
}

if (taxSelect) {
  taxSelect.addEventListener('change', function() {
    let partnetId = this.value;
    if (partnetId) {
                fetch(`/finances/ajax/get-discount/?id=${partnetId}`)
                    .then(response => response.json())
                    .then(data => {
                        let price = priceInput ? priceInput.value : 0;
                        let devdiscount = getInputValue(devdiscountInput);
                        let taxdiscount = data.price;
                        let agdiscount = 100 - taxdiscount - devdiscount;
                        setvalues(price, devdiscount, agdiscount, taxdiscount)
                    })
                    .catch(error => console.error('Помилка:', error));
            }
  });
}

if (priceInput) {
  priceInput.addEventListener('change', function() {
    let price = this.value;
    let devdiscount = getInputValue(devdiscountInput);
    let taxdiscount = getInputValue(taxdiscountInput);
    let agdiscount = 100 - taxdiscount - devdiscount;
    setvalues(price, devdiscount, agdiscount, taxdiscount)
  });
}

// Слушатели событий вешаем только в том случае, если элементы существуют на странице
if (devdiscountInput && devSelect) {
  devdiscountInput.addEventListener('input', function() {
    let price = priceInput ? priceInput.value : 0;
    let devdiscount = this.value;
    let taxdiscount = getInputValue(taxdiscountInput);
    let agdiscount = 100 - taxdiscount - devdiscount;
    setvalues(price, devdiscount, agdiscount, taxdiscount)
  });
}

if (agdiscountInput) {
  agdiscountInput.addEventListener('input', function() {
    let price = priceInput ? priceInput.value : 0;
    let agdiscount = this.value;
    let taxdiscount = getInputValue(taxdiscountInput);
    let devdiscount = getInputValue(devdiscountInput);
    // Если devSelect нет, devdiscount принудительно станет 0 внутри функции getInputValue
    if (!devSelect) {
        devdiscount = 0;
    } else {
        devdiscount = 100 - taxdiscount - agdiscount;
    }
    setvalues(price, devdiscount, agdiscount, taxdiscount)
  });
}

if (taxdiscountInput) {
  taxdiscountInput.addEventListener('input', function() {
    let price = priceInput ? priceInput.value : 0;
    let devdiscount = getInputValue(devdiscountInput);
    let taxdiscount = this.value;
    let agdiscount = 100 - taxdiscount - devdiscount;
    setvalues(price, devdiscount, agdiscount, taxdiscount)
  });
}
