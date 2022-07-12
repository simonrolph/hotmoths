'use strict';


// shuffling
function shuffle() {
  console.log("test");
  var container = document.getElementById("tindercards");
  var elementsArray = Array.prototype.slice.call(container.getElementsByClassName('tinder--card'));
    elementsArray.forEach(function(element){
    container.removeChild(element);
  })
  shuffleArray(elementsArray);
  elementsArray.forEach(function(element){
  container.appendChild(element);
})
}

function shuffleArray(array) {
    for (var i = array.length-1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
    return array;
}

shuffle();

const nelements = document.getElementById("tindercards").childElementCount;

for (var i=10; i < nelements;i++ ) {
  console.log("test");
  document.getElementById("tindercards").removeChild(document.getElementById("tindercards").lastElementChild);
}

// Get the modal
var modal = document.getElementById("myModal");

var modal2 = document.getElementById("titleModal");
modal2.style.display = "block";

function closetitle() {
  modal2.style.display = "none";
}

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

var tinderContainer = document.querySelector('.tinder');
var allCards = document.querySelectorAll('.tinder--card');
var nope = document.getElementById('nope');
var love = document.getElementById('love');

function initCards(card, index) {
  var newCards = document.querySelectorAll('.tinder--card:not(.removed)');

  newCards.forEach(function (card, index) {
    card.style.zIndex = allCards.length - index;
    card.style.transform = 'scale(' + (20 - index) / 20 + ') translateY(-' + 30 * index + 'px)';
    card.style.opacity = (10 - index) / 10;
  });
  
  tinderContainer.classList.add('loaded');
}

initCards();

allCards.forEach(function (el) {
  var hammertime = new Hammer(el);

  hammertime.on('pan', function (event) {
    el.classList.add('moving');
  });

  hammertime.on('pan', function (event) {
    if (event.deltaX === 0) return;
    if (event.center.x === 0 && event.center.y === 0) return;

    tinderContainer.classList.toggle('tinder_love', event.deltaX > 0);
    tinderContainer.classList.toggle('tinder_nope', event.deltaX < 0);

    var xMulti = event.deltaX * 0.03;
    var yMulti = event.deltaY / 80;
    var rotate = xMulti * yMulti;

    event.target.style.transform = 'translate(' + event.deltaX + 'px, ' + event.deltaY + 'px) rotate(' + rotate + 'deg)';
  });

  hammertime.on('panend', function (event) {
    
    el.classList.remove('moving');
    tinderContainer.classList.remove('tinder_love');
    tinderContainer.classList.remove('tinder_nope');

    var moveOutWidth = document.body.clientWidth;
    var keep = Math.abs(event.deltaX) < 80 || Math.abs(event.velocityX) < 0.5;

    event.target.classList.toggle('removed', !keep);

    if (keep) {
      event.target.style.transform = '';
    } else {

      if (event.deltaX>0){
        console.log("love")
        if(Math.random() < 0.5){
          modal.style.display = "block";
        }
      } else {
        console.log("nope")
        //modal.style.display = "block";
      }

      var endX = Math.max(Math.abs(event.velocityX) * moveOutWidth, moveOutWidth);
      var toX = event.deltaX > 0 ? endX : -endX;
      var endY = Math.abs(event.velocityY) * moveOutWidth;
      var toY = event.deltaY > 0 ? endY : -endY;
      var xMulti = event.deltaX * 0.03;
      var yMulti = event.deltaY / 80;
      var rotate = xMulti * yMulti;

      event.target.style.transform = 'translate(' + toX + 'px, ' + (toY + event.deltaY) + 'px) rotate(' + rotate + 'deg)';
      initCards();
    }
  });
});

function createButtonListener(love) {
  return function (event) {
    var cards = document.querySelectorAll('.tinder--card:not(.removed)');
    var moveOutWidth = document.body.clientWidth * 1.5;

    if (!cards.length) return false;

    var card = cards[0];

    card.classList.add('removed');

    if (love) {
      if(Math.random() < 0.5){
        modal.style.display = "block";
      }
      card.style.transform = 'translate(' + moveOutWidth + 'px, -100px) rotate(-30deg)';
    } else {
      //modal.style.display = "block";
      card.style.transform = 'translate(-' + moveOutWidth + 'px, -100px) rotate(30deg)';
    }

    initCards();

    event.preventDefault();
  };
}

var nopeListener = createButtonListener(false);
var loveListener = createButtonListener(true);

nope.addEventListener('click', nopeListener);
love.addEventListener('click', loveListener);




// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}


// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}



// function to calculate distance
//https://stackoverflow.com/questions/18883601/function-to-calculate-distance-between-two-coordinates
function distance(lat1, lon1, lat2, lon2, unit) {
  var radlat1 = Math.PI * lat1/180
  var radlat2 = Math.PI * lat2/180
  var theta = lon1-lon2
  var radtheta = Math.PI * theta/180
  var dist = Math.sin(radlat1) * Math.sin(radlat2) + Math.cos(radlat1) * Math.cos(radlat2) * Math.cos(radtheta);
  dist = Math.acos(dist)
  dist = dist * 180/Math.PI
  dist = dist * 60 * 1.1515
  if (unit=="K") { dist = dist * 1.609344 }
  if (unit=="N") { dist = dist * 0.8684 }
  return dist
}



if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition(getPosition);
}

async function getData(url) {
  try {
      let res = await fetch(url);
      return await res.json();
  } catch (error) {
      console.log(error);
  }
}

function getPosition(position) {
  // get location
  var lat = position.coords.latitude;
  var lng = position.coords.longitude;

  async function getDist(species,class_i) {
    let species_nearby = await getData('https://api.inaturalist.org/v1/observations?taxon_name='+ species+'&lat=' + lat + '&lng=' + lng + '&radius=100&per_page=15');
    const distances = [];
  
    for (const sp in species_nearby.results){
      let location = species_nearby.results[sp].location.split(',');
      distances.push(distance(lat,lng,Number(location[0]),Number(location[1]),"K"));
    }
    console.log(document.getElementsByClassName("moth-dist-1")[class_i].innerHTML)
    document.getElementsByClassName("moth-dist-1")[class_i].innerHTML = Math.round(Math.min(...distances)); 
    //document.getElementById("locationtext").setAttribute('href', "https://www.inaturalist.org/observations?q="+species+"&lat=",lat,"&lng="+lng);
  }; 

  for (const i in Array.from(Array(document.getElementsByClassName("sci-name").length).keys())) {
    console.log(i);
    console.log(document.getElementsByClassName("sci-name")[i].innerHTML);
    getDist(document.getElementsByClassName("sci-name")[i].innerHTML,i);
  }
  

  
}

  




