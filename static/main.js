rightarrow.addEventListener("click", (ev) => {
  ev.preventDefault();
  charitylogo.classList.add("swipe_image_left");
  setTimeout(() => {
    charitylogo.classList.remove("swipe_image_left");
  }, 2000);
  return false;
});

leftarrow.addEventListener("click", (ev) => {
  ev.preventDefault();
  charitylogo.classList.add("swipe_image_right");
  setTimeout(() => {
    charitylogo.classList.remove("swipe_image_right");
  }, 2000);
  return false;
});
