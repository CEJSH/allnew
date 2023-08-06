import image0 from './img/0.jpeg';
import image1 from './img/1.jpeg';
import image2 from './img/2.jpeg';


const images = [
    image0,
    image1,
    image2
];

const chosenImage = images[Math.floor(Math.random() * images.length)];

const bgImage = document.createElement("img");

bgImage.src = `${chosenImage}`;

document.body.appendChild(bgImage);