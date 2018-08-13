var form = document.querySelector("form");
// var form_data = new FormData(form);
var req = new XMLHttpRequest();

var eyebrow_l = document.getElementById("eyebrow-l");
var eyebrow_r = document.getElementById("eyebrow-r");
var eyes = document.getElementById("eyes");
var mouth = document.getElementById("mouth");

/* Chrome doesn't like flex this hack set the chat body as flex for all but Chrome broswer. */
if (!(navigator.userAgent.indexOf("Chrome") > -1)) {
    document.getElementById("chat-body").style.display = "flex";
}

/*
    ===============
       Functions
    ===============
*/

function send_request(data) {
    req.open("POST", "http://127.0.0.1:5000/message/", true);
    req.send(data);
}

function grandpy_face(expression) {
    console.log("running grandpy_face");
    eyebrow_l.className = "";
    eyebrow_r.className = "";
    eyes.className = "";
    mouth.className = "";

    switch(expression) {
        case 0:
        console.log("grandpy_face 0");
        eyebrow_l.classList.add("eyebrow-l-down");
        eyebrow_r.classList.add("eyebrow-r-down");
        eyes.classList.add("eyes-up-right");
        mouth.classList.add("mouse-close");
        break;
        case 1:
        console.log("grandpy_face 1");
        eyebrow_l.classList.add("eyebrow-l-blink");
        eyebrow_r.classList.add("eyebrow-r-blink");
        eyes.classList.add("big-eyes");
        mouth.classList.add("mouse-blink");
        break;
    }
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

    // var grandpy = document.getElementById("grandpy");

    setTimeout(function(){
        chat_body.appendChild(container);
        container.appendChild(thumbnail);
        
        container.appendChild(granpy_message);
        chat_body.scrollTop = chat_body.scrollHeight;
    }, delay);
}

function write_granpy_responses(response) {
    try {
        var response = JSON.parse(response);

        grandpy_face(0);
        if (response["hello"]) {
            write_message(response["hello"], 500);
        }
        write_message(response["hello"], 500);
        write_message(response["reflexion"], 1000);
        write_message(response["location"]["address"], 2000);
        write_message(response["localize"], 3000);
        init_map(
            response["location"]["latitude"],
            response["location"]["longitude"],
            4000,
        );
        write_message(response["near"] + response["stories"][0]["name"], 5000);
        write_message(response["stories"][0]["extract"], 8000);
        write_message(response["end"], 8500);

        setTimeout(function(){
            dots.classList.remove("visible");
        }, 8400);
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
        grandpy_face(1);
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
        // console.log("req.responseText:" + req.response);
        write_granpy_responses(req.response);
    } else {
        console.error(req.status + " " + req.statusText);
        write_granpy_responses("error");
    }
});

req.addEventListener("error", function () {
    console.error("Erreur réseau");
});




