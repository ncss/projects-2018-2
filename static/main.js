rightarrow.addEventListener("click", (ev) => {
  ev.preventDefault();
  charitylogo.classList.add("swipe_image_left");
  setTimeout(() => {
    charitylogo.classList.remove("swipe_image_left");
    window.location.replace("/");
  }, 400);
  return false;
});

leftarrow.addEventListener("click", (ev) => {
  ev.preventDefault();
  charitylogo.classList.add("swipe_image_right");
  setTimeout(() => {
    charitylogo.classList.remove("swipe_image_right");
    window.location.replace("/");
  }, 400);
  return false;
});

let startPosition = null;
let click = false;

charitylogo.draggable = false;
charitylogo.addEventListener("pointerdown", (ev) =>  {
	startPosition = ev.screenX;

	click = true;
})

function swipeFinish(delta) {
	console.log(delta)
	if (delta > 250) {
		rightarrow.click();
	} else if (delta < -250 ) {
				leftarrow.click();

	}

}

charitylogo.addEventListener("pointerup", (ev) =>  {
	let delta = ev.screenX - startPosition;
	swipeFinish(delta);
	startPosition = null;
	charitylogo.style.transform = null;
	click = false;

	
	})

charitylogo.addEventListener("pointerleave", (ev) =>  {
	if (ev.pointerType != "touch") {
	startPosition = null;
	charitylogo.style.transform = null;
	click = false;
	}
})

charitylogo.addEventListener("touchend", (ev) => {
	let delta = ev.changedTouches[0].screenX - startPosition;
	swipeFinish(delta);

		startPosition = null;
	charitylogo.style.transform = null;
	click = false;

	
	
})

charitylogo.addEventListener("pointermove", (ev) =>  {
	// Needed (brackets) around your if condition and needed to set startPosition to null
	if (click == true) {
		let delta = ev.screenX - startPosition;
		let rotation = delta * 0.0174;
		charitylogo.style.transform = `rotate(${rotation}deg) translate(${delta}px)`;
	}
});

charitylogo.addEventListener("touchmove", (ev) =>  {
	// Needed (brackets) around your if condition and needed to set startPosition to null
	if (click == true) {
		let delta = ev.touches[0].screenX - startPosition;
		let rotation = delta * 0.0174;
		charitylogo.style.transform = `rotate(${rotation}deg) translate(${delta}px)`;
	}
});
