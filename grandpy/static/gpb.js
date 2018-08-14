var form = document.querySelector("form");
var req = new XMLHttpRequest();

var eyebrow_l = document.getElementById("eyebrow-l");
var eyebrow_r = document.getElementById("eyebrow-r");
var eyes = document.getElementById("eyes");
var mouth = document.getElementById("mouth");

/* Chrome doesn't like flex this hack set the chat body as flex for all but Chrome broswer. */
if (!(navigator.userAgent.indexOf("Chrome") > -1)) {
    document.getElementById("chat-body").style.display = "flex";
}

// window.onresize = function(event) {
//     ...
// };
function resize() {
    console.log("screen.height:", window.innerHeight);
    var wh = window.innerHeight
    var ww = window.innerWidth

    if (wh > ww) {
        document.getElementById("chat-body").style.height = wh - 400 + "px";
    } else {
        document.getElementById("chat-body").style.height = wh / 2 - 150 + "px";
    }
}



/*
    ===============
       Functions
    ===============
*/

function send_request(data) {
    req.open("POST", window.location.protocol + "//" + window.location.host + "/message/", true);
    req.send(data);
}

function grandpy_face(expression) {
    console.log("running grandpy_face");
    eyebrow_l.className = "";
    eyebrow_r.className = "";
    eyes.className = "";
    mouth.className = "";

    switch(expression) {
        case 0: // Welcome face
        console.log("Grandpy face 0");
        eyes.classList.add("eyes-blink");
        break;

        case 1: // Thinking
        console.log("Grandpy face 1");
        eyebrow_l.classList.add("eyebrow-l-down");
        eyebrow_r.classList.add("eyebrow-r-down");
        eyes.classList.add("eyes-up-right");
        mouth.classList.add("mouth-close");
        break;

        case 2: // 
        console.log("Grandpy face 2");
        eyebrow_l.classList.add("eyebrow-l-blink");
        eyebrow_r.classList.add("eyebrow-r-blink");
        eyes.classList.add("big-eyes");
        mouth.classList.add("mouth-blink");
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

        grandpy_face(1);

        if (response["quit"]) {
            write_message(response["quit"], 500);
        }

        else {
            if (response["hello"]) {
                write_message(response["hello"], 500);
            }
            write_message(response["reflexion"], 1000);
            write_message(response["location"]["address"], 2000);
            write_message(response["localize"], 3000);
            init_map(
                response["location"]["latitude"],
                response["location"]["longitude"],
                4000,
            );
            /* get a random place */
            story_number = Math.floor(Math.random() * response["stories"].length) + 1

            write_message(response["near"] + response["stories"][story_number]["name"], 5000);
            write_message(response["stories"][story_number]["extract"], 8000);
            write_message(response["end"], 8500);
    
            setTimeout(function(){
                dots.classList.remove("visible");
            }, 8400);

            setTimeout(function(){
                grandpy_face(0);
            }, 8500);
        }
    }

    catch(error) {
        var confusion_responses = [
            "Euh... Qui êtes-vous ?",
            "Infirmière ! Au secours !!",
            "Qu'est-ce que je disais déjà ?",
            "Granpy a besoin de repos là...",
            "Ouh... Je sais plus, tout est flou dans ma tête",
            "Je ne me souviens... de rien.",
            "Je me sens pas très bien, peut être que j'ai besoin d'un rafraîchissement F5...",
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
        grandpy_face(2);
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
    document.getElementById("message").value = "";
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
        write_granpy_responses(req.response);
    } else {
        console.error(req.status + " " + req.statusText);
        write_granpy_responses("error");
    }
    resize();
    console.log('load');
});

req.addEventListener("error", function () {
    var off_responses = [
        "GrandPy se sent comme... déconnecté du réseau.",
        "Je me sens comme... déconnecté du réseau.",
        "Pffiuuu, je suis pas connecté aujourd'hui... Repasse plus tard.",
        "Je me sens déconnecté, peut être qu'avec un petit rafraîchissement F5...",
    ]
    
    console.error("Erreur réseau");
    write_message(off_responses[Math.floor(Math.random() * off_responses.length)]);

});

window.addEventListener('resize', function(){
    this.setTimeout(resize(), 1000);
});

window.addEventListener('load', resize());



