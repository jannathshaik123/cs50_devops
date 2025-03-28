if (!localStorage.getItem("count")) {
  localStorage.setItem("count", 0);
}

function counter() {
  let count = localStorage.getItem("count");
  count++;
  document.querySelector("h1").innerHTML = count;
  localStorage.setItem("count", count);
}
document.addEventListener("DOMContentLoaded", () => {
  document.querySelector("h1").innerHTML = localStorage.getItem("count");
  // document.querySelector("button").addEventListener('onclick',counter);
  document.querySelector("button").onclick = counter;
});
