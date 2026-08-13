const grid = document.querySelector("#shirtGrid");
const template = document.querySelector("#shirtTemplate");

fetch("assets/shirts/catalog.json")
  .then(response => response.ok ? response.json() : Promise.reject(response.status))
  .then(products => products.forEach((product, index) => {
    const fragment = template.content.cloneNode(true);
    const card = fragment.querySelector(".shirt-card");
    const front = fragment.querySelector(".front");
    const back = fragment.querySelector(".back");
    const loading = index < 2 ? "eager" : "lazy";
    front.src = `assets/shirts/${product.slug}-front.svg`;
    back.src = `assets/shirts/${product.slug}-back.svg`;
    front.alt = `${product.name} shirt front`;
    back.alt = `${product.name} shirt back`;
    front.loading = loading;
    back.loading = loading;
    card.querySelector(".edition").textContent = `MW-${String(index + 1).padStart(2, "0")} / ${product.term}`;
    card.querySelector("h2").textContent = product.name;
    card.querySelector(".subline").textContent = product.subline;
    card.querySelector(".price").textContent = `$${product.price}.00`;
    card.querySelector(".buy").href = `checkout?item=${encodeURIComponent(product.slug)}`;
    grid.append(fragment);
  }))
  .catch(() => { grid.innerHTML = "<p>Collection unavailable.</p>"; });
