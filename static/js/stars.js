var stars = document.getElementById('stars')
var height = $('#stars').height()
var height_max = height*0.8
var height_min = -0.2*height
var width = $('#stars').width()

function randomDistance (max, min) {
    var distance = Math.floor(Math.random() * (max - min + 1) + min)
    return distance
}



// generate stars
for (var j=0;j<15;j++) {
    var newStar = document.createElement("div")
    newStar.className = "star"
    newStar.style.top = randomDistance(height_max,height_min) + 'px'
    newStar.style.left = randomDistance(width, 0) + 'px'
    stars.appendChild(newStar)
}

//random time
var star = document.getElementsByClassName('star')

for (var i = 0, len = star.length; i < len; i++)
{
    star[i].style.animationDelay = i % 6 == 0 ? '0s' : i * 0.8 + 's'
}

console.log(height,width)