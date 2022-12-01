
function formatSearchResult(search_result) {
    return `<ul class="list-group" style="width: 20rem;">
                <li class="list-group-item">
                    <img src="${search_result['image_url']}" width=40%><br>
                    <a style="text-decoration: none;" href="${search_result['url']};" target="_blank">${search_result['name']}</a><br>
                    ${search_result['location']}<br>
                    <span>Rating: ${search_result['rating']} </span><br>
                    ${search_result['phone']}<br></li>`;
}

document.querySelector('#user-search').addEventListener('submit', (evt) => {
evt.preventDefault();

let clearResults = document.getElementById('user-search-results');
clearResults.innerHTML = '';

const formInputs = {
    zipcode: document.querySelector("#enter_zip").value,
    holistic: document.querySelector("#holistic").value,
}

const querystring = new URLSearchParams(formInputs).toString();


fetch(`/user_search?${querystring}`)

.then((response) => response.json())
.then((search_results) => {
    for (const search_result of search_results){
        document.querySelector('#user-search-results').insertAdjacentHTML('beforeend', formatSearchResult(search_result))
        document.querySelector('#user-search-results').insertAdjacentHTML('beforeend', "<br>")
    }
}
)})





