function getColour() {
    document.body.style.backgroundColor = document.cookie;
}
function defaultColour() {
    document.cookie = "ivory";
    document.body.style.backgroundColor = "ivory";

}
function greenColour() {
    document.cookie = "green";
    document.body.style.backgroundColor = "green";
}
function blueColour() {
    document.cookie = "blue";
    document.body.style.backgroundColor = "blue";
}

