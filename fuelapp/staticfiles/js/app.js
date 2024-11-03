// Message/Notification timer
document.addEventListener("DOMContentLoaded", function(){
    // Select all elements with an id starting with "message-timer"
    const messages = document.querySelectorAll("[id^='message-timer']");

    messages.forEach(function (message){
        setTimeout(function (){
            message.style.display = "none";
        },5000); // Hide after 5 seconds
    });
});