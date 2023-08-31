function clearSearchTerm() {
    document.getElementById("AddQueryTextbox").value = "";
}

function setRequestOptions(data, method) {
    return requestOptions = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    };
};

function updateSearches(searchterm) {
    const SearchTermsSelect = document.getElementById("SearchTerms");
    SearchTermsSelect.innerHTML = "";
    searchterm.forEach(function (searchterm) {
        const coption = document.createElement("option");
        coption.value = searchterm;
        coption.textContent = searchterm;
        SearchTermsSelect.appendChild(coption);
    });
};
function fetchAndSetSearches(cname) {
    fetch("/v1/queries/" + cname)
        .then(response => response.json())
        .then(data => {
            const searches = Object.values(data.saved_searches);
            updateSearches(searches);
        })
        .catch(error => {
            console.error("Error in fetching saved searches:", error);
        });
};

function AddNewSearchTerm() {
    let newSearch = document.getElementById("AddQueryTextbox").value;
    const cname = document.getElementById("ChannelName").value;
    const addButton = document.getElementById("AddQueryButton");
    // console.log(newSearch);
    const requestOptions = setRequestOptions({
        "channel_name": cname, "queries": [
            newSearch
        ]
    }, "PUT");

    fetch("/v1/queries/" + cname, requestOptions)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            fetchAndSetSearches(cname);
        })
        .catch(error => {
            console.log(error);
        })

    // document.getElementById("AddQueryTextbox").value = "";
};
function DeleteSearchTerm() {
    let searchtodelete = document.getElementById("SearchTerms").value;
    const cname = document.getElementById("ChannelName").value;
    const deleteButton = document.getElementById("DelQueryButton");
    // console.log(newSearch);
    const requestOptions = setRequestOptions({
        "channel_name": cname, "queries": [
            searchtodelete
        ]
    }, "DELETE");

    fetch("/v1/queries/" + cname, requestOptions)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            fetchAndSetSearches(cname);
        })
        .catch(error => {
            console.log(error);
        })
};


document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("SelectQueryForm").addEventListener("submit", function (event) {
        event.preventDefault();
    });
    document.getElementById("SearchTerms").addEventListener("change", function (event) {
        let cname = event.target.value;
    });
    document.getElementById("AddQueryButton").addEventListener("click", function (event) {
        let newCname = event.target.value;
        // console.log(newCname);
    });
});