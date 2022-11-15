
function formatSearchResult(search_result) {
    return `${search_result['name']},
            ${search_result['location']},
            ${search_result['rating']},
            ${search_result['phone']},
            <img src="${search_result['image_url']}">`;
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
        // document.querySelector('#user-search-results').insertAdjacentHTML('beforeend', JSON.stringify(search_result))
        document.querySelector('#user-search-results').insertAdjacentHTML('beforeend', formatSearchResult(search_result))
        document.querySelector('#user-search-results').insertAdjacentHTML('beforeend', "<br><br>")
    }
}
)})





