var form = document.querySelector("form");
// var form_data = new FormData(form);
var req = new XMLHttpRequest();


/*
    ===============
       Functions
    ===============
*/

function send_request(data) {
    req.open("POST", "http://127.0.0.1:5000/message/", true);
    req.send(data);
}

function write_message(message, delay, author='grandpy') {
    var container = document.createElement("div");
    container.setAttribute('class', 'message-container');

    var thumbnail = document.createElement("div");
    thumbnail.setAttribute('class', 'thumbnail thumbnail-' + author);

    var granpy_message = document.createElement("p");
    granpy_message.setAttribute('class', 'message ' + author + '-message');
    granpy_message.textContent = message;

    var chat_body = document.getElementById("chat-body");
    chat_body.style.JustifyContent = "flex-start";

    var dots = document.getElementById("dots");
    dots.classList.add("visible");

    setTimeout(function(){
        chat_body.appendChild(container);
        container.appendChild(thumbnail);
        dots.classList.remove("visible");
        container.appendChild(granpy_message);
        chat_body.scrollTop = chat_body.scrollHeight;
    }, delay);
}

function write_granpy_responses(response) {
    try {
        var response = JSON.parse(response);

        write_message(response["reflexion"], 1000);
        write_message(response["location"]["address"], 2000);
        write_message(response["localize"], 3000);
        init_map(
            response["location"]["latitude"],
            response["location"]["longitude"],
            4000,
        );
        write_message(response["stories"][0]["name"], 5000);
        write_message(response["stories"][0]["extract"], 6000);
    }
    catch(error) {
        var confusion_responses = [
            "Euh... Qui êtes-vous ?",
            "Infirmière ! Au secours !!",
            "Qu'est-ce que je disais déjà ?",
            "Granpy a besoin de repos là...",
            "Ouh... Je sais plus, tout est flou dans ma tête",
            "Je ne me souviens... de rien.",
        ]
        write_message(confusion_responses[Math.floor(Math.random() * confusion_responses.length)]);
    }
}

function init_map(latitude, longitude, delay) {
    var location = {lat: latitude, lng: longitude};
    var map_message = document.createElement("p");
    map_message.setAttribute('class', 'map');

    var chat_body = document.getElementById("chat-body");

    setTimeout(function(){
        document.getElementById("chat-body").appendChild(map_message);
        var map = new google.maps.Map(
            map_message, {zoom: 12, center: location});
        var marker = new google.maps.Marker({position: location, map: map});
        chat_body.style.justifyContent = "flex-start";
    }, delay);
}


/*
    =============================
       Event listeners on form
    =============================
*/

form.addEventListener("submit", function (e) {
    var form_data = new FormData(form);
    e.preventDefault();
    write_message(message.value, 0, 'user');
    console.log("Form data:", form_data);
    send_request(form_data);
});

form.addEventListener('keypress', function(e) {
    var form_data = new FormData(form);
    console.log("Keypress action detected");
    if (e.keyCode === 13) {
        console.log("Press <ENTER> action detected");
        write_message(message.value, 0, 'user');
        console.log("data:", form_data);
        send_request(form_data);
        document.getElementById("message").value = "";
    }
});


/*
    ================================
       Event listeners on request
    ================================
*/

req.addEventListener("load", function () {
    if (req.status >= 200 && req.status < 400) {
        console.log("req.responseText:" + req.response);
        write_granpy_responses(req.response);
    } else {
        console.error(req.status + " " + req.statusText);
        write_granpy_responses("error");
    }
});

req.addEventListener("error", function () {
    console.error("Erreur réseau");
});




