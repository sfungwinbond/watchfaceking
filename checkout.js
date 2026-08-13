const params = new URLSearchParams(location.search);
const requested = params.get("item");
let products = [];
let selected;

const money = value => new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(value);

function render() {
  const slug = document.querySelector("#productSelect").value;
  selected = products.find(product => product.slug === slug) || products[0];
  document.querySelector("#frontImage").src = `assets/shirts/${selected.slug}-front.svg`;
  document.querySelector("#backImage").src = `assets/shirts/${selected.slug}-back.svg`;
  document.querySelector("#productName").textContent = selected.name;
  document.querySelector("#term").textContent = selected.subline;
  document.querySelector("#unitPrice").textContent = money(selected.price);
  updateTotal();
  history.replaceState(null, "", `checkout?item=${encodeURIComponent(selected.slug)}`);
}

function updateTotal() {
  if (!selected) return;
  const total = selected.price * Number(document.querySelector("#quantity").value);
  document.querySelector("#subtotal").textContent = money(total);
  document.querySelector("#total").textContent = money(total);
}

fetch("assets/shirts/catalog.json")
  .then(response => response.ok ? response.json() : Promise.reject(response.status))
  .then(data => {
    products = data;
    const select = document.querySelector("#productSelect");
    products.forEach(product => select.add(new Option(`${product.name} — ${money(product.price)}`, product.slug)));
    select.value = products.some(product => product.slug === requested) ? requested : products[0].slug;
    select.addEventListener("change", render);
    document.querySelector("#quantity").addEventListener("change", updateTotal);
    render();
  });

document.querySelector("#checkoutForm").addEventListener("submit", event => {
  event.preventDefault();
  const size = document.querySelector("#size").value;
  const quantity = document.querySelector("#quantity").value;
  document.querySelector("#confirmationCopy").textContent = `${quantity} × ${selected.name}, size ${size}. No payment was taken.`;
  document.querySelector("#confirmation").showModal();
});
