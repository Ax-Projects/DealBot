fetchAndSetChannels();
function setRequestOptions(data, method) {
    return requestOptions = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    };
};

function updateChannels(keys) {
    const channelSelect = document.getElementById("ChannelName");
    channelSelect.innerHTML = "";
    keys.forEach(function (key) {
        const coption = document.createElement("option");
        coption.value = key;
        coption.textContent = key;
        channelSelect.appendChild(coption);
    });
};
function fetchAndSetChannels() {
    fetch("/v1/queries/")
        .then(response => response.json())
        .then(data => {
            const keys = Object.keys(data.saved_searches);
            updateChannels(keys);
        })
        .catch(error => {
            console.error("Error in fetching saved channels:", error);
        });
};
function deleteWholeChannel() {
    const cname = document.getElementById("ChannelName").value;
    console.log(cname);
    const requestOptions = setRequestOptions({ "channel_name": cname }, "DELETE");

    fetch("/v1/queries/" + cname, requestOptions)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            fetchAndSetChannels();
        })
        .catch(error => {
            console.log(error);
        })
};
function AddNewChannel() {
    let newCname = document.getElementById("AddChannelTextbox").value;
    const addButton = document.getElementById("AddChannelButton");
    console.log(newCname);
    const requestOptions = setRequestOptions({ "channel_name": newCname }, "POST");

    fetch("/v1/queries/", requestOptions)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            fetchAndSetChannels();
        })
        .catch(error => {
            console.log(error);
        })
    document.getElementById("AddChannelTextbox").value = "";
};

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("SelectChannelForm").addEventListener("submit", function (event) {
        event.preventDefault();
    });
    document.getElementById("ChannelName").addEventListener("change", function (event) {
        let cname = event.target.value;
        fetchAndSetSearches(cname)
    });
    document.getElementById("AddChannelTextbox").addEventListener("change", function (event) {
        let newCname = event.target.value;
        // console.log(newCname);
    });
});