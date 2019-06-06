var query2json = function (query) {
    query = query.substring(0, 1) == '?' ? query.substring(1): query;
    return JSON.parse('{"' + decodeURI(query.replace(/&/g, "\",\"").replace(/=/g,"\":\"")) + '"}');
};

var NewConnect = function (options) {

    var self = this;

    self.onconnect = options.onconnect || function (data) {
        console.log("NewsConnect data", data);
        console.log("!!! Please, implement onconnect !!!");
    };

    self.receiveMessage = function receiveMessage(event) {
        if (event.origin == "{{ BASE_URL }}") {
            self.onconnect(event.data);
        }
    };
    window.addEventListener("message", self.receiveMessage, false);

    var frame = document.createElement('iframe');
    frame.src = '{{ BASE_URL }}{% url "account_app_post_message_simple" %}' + options.token + '/';
    frame.style.display = 'none';
    document.body.appendChild(frame);
};
