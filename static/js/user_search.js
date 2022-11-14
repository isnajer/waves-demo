

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
        document.querySelector('#user-search-results').insertAdjacentHTML('beforeend', JSON.stringify(search_result))
        // document.querySelector('#user-search-results').insertAdjacentHTML('beforeend', formatSearchResult(re))
        document.querySelector('#user-search-results').insertAdjacentHTML('beforeend', "<br><br>")
    }
}
)})





