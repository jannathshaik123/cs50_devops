let count = 0;
function counter() {
  count++;
  document.querySelector("h1").innerHTML = count;

  if (count % 10 === 0) {
    alert(`Counter is ${count}`);
  }
}
document.addEventListener("DOMContentLoaded", () => {
  // document.querySelector("button").addEventListener('onclick',counter);
  document.querySelector("button").onclick = counter;
});
