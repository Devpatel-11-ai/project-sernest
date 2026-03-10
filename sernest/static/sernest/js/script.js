document.addEventListener("DOMContentLoaded", function(){
// Filter Function
function filterEmployees() {
    const input = document.getElementById("searchInput").value.toLowerCase();
    const rows = document.querySelectorAll("#employeeTable tbody tr");

    rows.forEach(row => {
        const text = row.innerText.toLowerCase();
        if (text.includes(input)) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    });
}

const input = document.getElementById("category-search");
const results = document.getElementById("search-results");

let selectedIndex = -1;

const categories = [];

document.querySelectorAll(".category-card").forEach(card => {

    const nameElement = card.querySelector(".cat-title");
    const iconElement = card.querySelector(".cat-icon");

    if(nameElement){

        categories.push({
            name: nameElement.innerText,
            icon: iconElement ? iconElement.innerText : "🔧",
            url: card.href
        });

    }

});

function highlight(text, search){
    const regex = new RegExp(`(${search})`, "gi");
    return text.replace(regex, `<span class="highlight">$1</span>`);
}
input.addEventListener("input", function(){
    const value = this.value.toLowerCase();
    results.innerHTML = "";
    if(!value){
     results.classList.remove("show");
     return;
    }
    
   const filtered = categories.filter(cat => {
    const name = cat.name.toLowerCase();
    return name.includes(value) ||
    value.includes(name) ||
    name.startsWith(value);
});
    
    filtered.slice(0,8).forEach((cat,index)=>{
        const div = document.createElement("div");
        div.classList.add("search-item");
        div.innerHTML = `
        <span class="search-icon">${cat.icon || "🔧"}</span>
        <span class="search-text">${highlight(cat.name,value)}</span>
        `;
        
        div.addEventListener("click",()=>{
            window.location.href = cat.url;
        });
        
        results.appendChild(div);
    });
    results.classList.add("show");
    selectedIndex = -1;
});

input.addEventListener("keydown",(e)=>{
    const items = document.querySelectorAll(".search-item");

    if(e.key==="ArrowDown"){
        selectedIndex++;
        if(selectedIndex >= items.length) selectedIndex=0;
        updateSelection(items);
    }
    
    if(e.key==="ArrowUp"){
        selectedIndex--;
        if(selectedIndex<0) selectedIndex=items.length-1;
        updateSelection(items);
    }
    
    if(e.key==="Enter"){
        if(selectedIndex>=0){
            items[selectedIndex].click();
        }
    }

});

function updateSelection(items){
    items.forEach(i=>i.classList.remove("active"));

    if(items[selectedIndex]){
        items[selectedIndex].classList.add("active");
    }
}

document.addEventListener("DOMContentLoaded", function(){
    const searchBtn = document.getElementById("search-btn");
    searchBtn.addEventListener("click", function(){

        const service = document.getElementById("category-search").value.trim();
        const city = document.getElementById("location-search").value.trim();

        if(service === ""){
            alert("Please enter a service");
            return;
        }
        let url = "/categories/?service=" + encodeURIComponent(service);

        if(city !== ""){
            url += "&city=" + encodeURIComponent(city);
        }
        window.location.href = url;
    });
});
});