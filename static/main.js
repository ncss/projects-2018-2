rightarrow.addEventListener("click", (ev) => {
  ev.preventDefault();
  charitylogo.classList.add("swipe_image_left");
  setTimeout(() => {
    charitylogo.classList.remove("swipe_image_left");
    window.location.replace("/");
  }, 1000);
  return false;
});

leftarrow.addEventListener("click", (ev) => {
  ev.preventDefault();
  charitylogo.classList.add("swipe_image_right");
  setTimeout(() => {
    charitylogo.classList.remove("swipe_image_right");
    window.location.replace("/");
  }, 1000);
  return false;
});

let startPosition = null;
let click = false;

charitylogo.draggable = false;
charitylogo.addEventListener("pointerdown", (ev) =>  {
	startPosition = ev.screenX;
	click = true;
	console.log('pdown');
})

charitylogo.addEventListener("pointerup", (ev) =>  {
	startPosition = null;
	charitylogo.style.transform = null;
	click = false;
	console.log('pup');
})

document.body.addEventListener("pointerleave", (ev) =>  {
	if (ev.pointerType != "touch") {
	startPosition = null;
	charitylogo.style.transform = null;
	click = false;
	console.log(ev);
	console.log('pleave');
	}
})

document.body.addEventListener("touchend", (ev) => {
		startPosition = null;
	charitylogo.style.transform = null;
	click = false;
	console.log('pup');

	
	
})

charitylogo.addEventListener("pointermove", (ev) =>  {
	// Needed (brackets) around your if condition and needed to set startPosition to null
	if (click == true) {
		console.log(startPosition);
		let delta = ev.screenX - startPosition;
		console.log(ev.screenX);
		let rotation = delta * 0.0174;
		charitylogo.style.transform = `rotate(${rotation}deg) translate(${delta}px)`;
		console.log(`rotate(${rotation}deg) translate(${delta}px)`);
	}
});

charitylogo.addEventListener("touchmove", (ev) =>  {
	// Needed (brackets) around your if condition and needed to set startPosition to null
	if (click == true) {
		console.log(ev);
		console.log(startPosition);
		let delta = ev.touches[0].screenX - startPosition;
		console.log(ev.touches[0].screenX);
		let rotation = delta * 0.0174;
		charitylogo.style.transform = `rotate(${rotation}deg) translate(${delta}px)`;
		console.log(`rotate(${rotation}deg) translate(${delta}px)`);
	}
});
