const params = new URLSearchParams(window.location.search);
var video = null; 

function bodyonload() {
    setupVideo();
    invokeOSD();
}

function setupVideo() {
    video = document.createElement('video');
    video.id = 'video';
//    video.height = 720;
    video.controls = true;
    video.autoplay = true;
    video.muted = true;
    video.loop = true;
    video.ontimeupdate = function() {updatePlayerCurrentTime()};
    video.ondurationchange = function() {updatePlayerDuration()};

    source = document.createElement('source');
    source.src = params.get('src');
    source.type = params.get('type') || 'video/mp4';

    video.appendChild(source);
    document.getElementById('videoDiv').append(video);
}

function updatePlayerCurrentTime() {
    let player_currentTime = document.getElementById('player_currentTime');
    if (player_currentTime) {
        player_currentTime.innerHTML = secondsToHHMMSS(video.currentTime);

        let player_status = document.getElementById('player_status');
        player_status.innerHTML = video.paused ? "pause" : "playing";
    }
}

function updatePlayerDuration() {
    player_duration = document.getElementById('player_duration');
    if (player_duration)
        player_duration.innerHTML = ' / ' + secondsToHHMMSS(video.duration);
}

function secondsToHHMMSS(seconds){
    hours = Math.floor(seconds / 3600);
    minutes = Math.floor(seconds / 60) % 60;
    seconds = seconds % 60;

    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals
    return `${padStart(hours)}:${padStart(minutes)}:${padStart(seconds, 2)}s`;
}

function padStart(number, decimalPlace){
    decimalPlace = decimalPlace || 0;
    startPad = decimalPlace ? 5 : 2;
    return number.toFixed(decimalPlace).toString().padStart(startPad,'0');
}

function invokeOSD(){
    osd = document.getElementById('informationDiv');
    osd.innerHTML = 'Source: ' + params.get('src');

    inElement = document.createElement('div');
    inElement.id = 'player_status';
    if (video) 
        inElement.innerHTML = video.paused ? "pause" : "playing";
    osd.append(inElement);

    inElement = document.createElement('div');
    osd_playerPosition = inElement;
    osd.append(inElement);

    inElement = document.createElement('span');
    inElement.id = 'player_currentTime';
    if (video) 
        inElement.innerHTML = secondsToHHMMSS(video.currentTime);
    osd_playerPosition.append(inElement);

    inElement = document.createElement('span');
    inElement.id = 'player_duration';
    if (video) 
        inElement.innerHTML = " / " + secondsToHHMMSS(video.duration);
    osd_playerPosition.append(inElement);
}
